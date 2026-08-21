from __future__ import annotations

import copy
import hashlib
import http.client
import importlib.util
import json
import os
import subprocess
import sys
import tempfile
import threading
import unittest
from pathlib import Path

REPOSITORY_ROOT = Path(__file__).resolve().parents[1]
SCRIPT_ROOT = REPOSITORY_ROOT / "scripts"
for path in (REPOSITORY_ROOT, SCRIPT_ROOT):
    if str(path) not in sys.path:
        sys.path.insert(0, str(path))

from machine_docs_change_plan_lifecycle import _rollback_basics
from university_runtime.io import atomic_write_json, load_json_beneath, strict_load_json
from university_runtime.plan import build_execution_plan, validate_execution_plan
from university_runtime.target import validate_target_context

from campusweave import service


def _load_validator():
    spec = importlib.util.spec_from_file_location(
        "validate_machine_docs", SCRIPT_ROOT / "validate_machine_docs.py"
    )
    assert spec and spec.loader
    module = importlib.util.module_from_spec(spec)
    spec.loader.exec_module(module)
    return module


class OfflinePlanTests(unittest.TestCase):
    def test_reference_profile_compiles_to_an_unbound_deterministic_plan(self) -> None:
        response = service.reference_response()
        profile = response["profile"]
        digest = hashlib.sha256(
            (REPOSITORY_ROOT / "docs/relution/packages/university/desired-state.json").read_bytes()
        ).hexdigest()
        first = build_execution_plan(profile, digest)
        self.assertEqual(first, build_execution_plan(profile, digest))
        self.assertEqual(validate_execution_plan(first, profile, digest), [])
        self.assertFalse(first["execution_authorized"])
        self.assertFalse(first["network_capable"])
        self.assertFalse(first["mutation_capable"])
        self.assertTrue(all(step["state"] == "unbound" for step in first["steps"]))

    def test_revoked_or_stale_bindings_remain_non_mutating(self) -> None:
        response = service.reference_response()
        profile = response["profile"]
        digest = hashlib.sha256((REPOSITORY_ROOT / "docs/relution/packages/university/desired-state.json").read_bytes()).hexdigest()
        plan = build_execution_plan(profile, digest)
        revoked = copy.deepcopy(plan)
        revoked["execution_authorized"] = True
        revoked["mutation_capable"] = True
        revoked["steps"][0]["operation_bindings"] = ["POST /devices"]
        errors = validate_execution_plan(revoked, profile, digest)
        self.assertTrue(any("execution_authorized" in error for error in errors))
        self.assertTrue(any("operation_bindings" in error for error in errors))
        template = json.loads((REPOSITORY_ROOT / "docs/relution/templates/university-runtime-target.json").read_text())
        template["context_status"] = "stale"
        self.assertTrue(any("stale target contexts" in error for error in validate_target_context(template, REPOSITORY_ROOT / "docs/relution/templates/university-runtime-target.json", profile, REPOSITORY_ROOT / "docs/relution/packages/university/desired-state.json")))

        credential_bearing = copy.deepcopy(template)
        credential_bearing["context_status"] = "template"
        credential_bearing["target"]["client_secret"] = "must-not-enter-a-plan"
        credential_errors = validate_target_context(
            credential_bearing,
            REPOSITORY_ROOT / "docs/relution/templates/university-runtime-target.json",
            profile,
            REPOSITORY_ROOT / "docs/relution/packages/university/desired-state.json",
        )
        self.assertTrue(any("credential-bearing" in error for error in credential_errors))

        terminal = copy.deepcopy(plan)
        terminal["plan_status"] = "verified"
        terminal["execution_authorized"] = True
        terminal_errors = validate_execution_plan(terminal, profile, digest)
        self.assertTrue(any("execution_authorized" in error for error in terminal_errors))

        rollback_errors: list[str] = []
        _rollback_basics(
            {
                "available": True,
                "execution_mode": "not-a-mode",
                "strategy": "restore prior values",
                "prior_values_captured": True,
                "irreversibility_acknowledged": False,
                "recovery_owner": "operator",
                "recovery_window": "immediate",
            },
            Path("inline-change-plan.json"),
            rollback_errors,
        )
        self.assertTrue(any("$.rollback.execution_mode" in error for error in rollback_errors))

    def test_private_artifacts_reject_ambiguous_input_and_never_overwrite(self) -> None:
        with tempfile.TemporaryDirectory() as directory:
            path = Path(directory) / "plan.json"
            atomic_write_json(path, {"safe": True})
            with self.assertRaisesRegex(ValueError, "already exists"):
                atomic_write_json(path, {"safe": False})
            duplicate = Path(directory) / "duplicate.json"
            duplicate.write_text('{"a": 1, "a": 2}', encoding="utf-8")
            with self.assertRaisesRegex(ValueError, "duplicate JSON key"):
                strict_load_json(duplicate)

    def test_artifact_paths_reject_traversal_and_symlinks_before_reading(self) -> None:
        with tempfile.TemporaryDirectory() as directory:
            root = Path(directory) / "private"
            root.mkdir(mode=0o700)
            outside = Path(directory) / "outside.json"
            outside.write_text('{"secret":"no"}', encoding="utf-8")
            (root / "linked.json").symlink_to(outside)
            with self.assertRaisesRegex(ValueError, "traversal-free"):
                load_json_beneath(root, "../outside.json")
            with self.assertRaisesRegex(ValueError, "without following symlinks"):
                load_json_beneath(root, "linked.json")


class ServiceBoundaryTests(unittest.TestCase):
    def test_relution_destination_is_pinned_and_token_stays_off_the_environment(self) -> None:
        helper = SCRIPT_ROOT / "relution_curl.zsh"
        with tempfile.TemporaryDirectory() as directory:
            fake_curl = Path(directory) / "curl"
            fake_curl.write_text("#!/bin/sh\n[ -z \"$RELUTION_API_TOKEN\" ] || exit 44\ncat | grep -F 'X-User-Access-Token: private-token' >/dev/null\n", encoding="utf-8")
            fake_curl.chmod(0o755)
            environment = {**os.environ, "PATH": f"{directory}:{os.environ['PATH']}"}
            command = f"source {helper}; RELUTION_API_TOKEN=private-token; RELUTION_API_SERVER=https://relution.example/api; relution_curl --request GET https://relution.example/api/devices"
            self.assertEqual(
                subprocess.run(["zsh", "-fc", command], check=False, env=environment).returncode,
                0,
            )
            blocked = command.replace("https://relution.example/api/devices", "https://other.example/api/devices")
            self.assertNotEqual(
                subprocess.run(["zsh", "-fc", blocked], check=False, env=environment).returncode,
                0,
            )

    def test_loopback_service_rejects_untrusted_origins_and_ambiguous_json(self) -> None:
        server = service.ThreadingHTTPServer(("127.0.0.1", 0), service.CampusWeaveHandler)
        thread = threading.Thread(target=server.serve_forever, daemon=True)
        thread.start()
        try:
            def request(method: str, path: str, *, body: bytes | None = None, headers=None):
                connection = http.client.HTTPConnection("127.0.0.1", server.server_port, timeout=3)
                try:
                    connection.request(method, path, body=body, headers=headers or {})
                    response = connection.getresponse()
                    return response.status, dict(response.getheaders()), response.read()
                finally:
                    connection.close()

            allowed = {"Host": "localhost:8766", "Origin": "http://localhost:8766"}
            status, headers, body = request("GET", "/api/v1/health", headers=allowed)
            self.assertEqual((status, json.loads(body)), (200, {"mode": "offline_planning_only", "status": "ok"}))
            self.assertEqual(headers["Cache-Control"], "no-store")
            self.assertEqual(request("GET", "/api/v1/reference", headers={"Host": "evil.invalid"})[0], 403)
            self.assertEqual(
                request(
                    "POST",
                    "/api/v1/compile-profile",
                    body=b'{"profile":{},"profile":{}}',
                    headers={**allowed, "Content-Type": "application/json"},
                )[0],
                400,
            )
        finally:
            server.shutdown()
            server.server_close()
            thread.join(timeout=3)


class MachineDocumentationTests(unittest.TestCase):
    def test_checked_in_machine_docs_validate_and_reject_ambiguous_json(self) -> None:
        validator = _load_validator()
        self.assertEqual(validator.main([]), 0)
        with tempfile.TemporaryDirectory() as directory:
            path = Path(directory) / "broken.json"
            path.write_text('{"status":"generated","status":"not_generated"}', encoding="utf-8")
            with self.assertRaisesRegex(validator.ValidationFailure, "duplicate JSON key"):
                validator.load_json(path)


if __name__ == "__main__":
    unittest.main()
