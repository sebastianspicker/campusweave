from __future__ import annotations

import os
import shlex
import subprocess
import sys
import tempfile
import textwrap
import unittest
from pathlib import Path


REPOSITORY_ROOT = Path(__file__).resolve().parents[1]
HELPER = REPOSITORY_ROOT / "scripts" / "relution_curl.zsh"
DUMMY_TOKEN = "dummy-relution-token-for-pipe-test"
SERVER = "https://mdm.example.invalid/relution"
ALLOWED_URL = f"{SERVER}/api/test"


class RelutionCurlHelperTests(unittest.TestCase):
    def run_helper(
        self,
        *arguments: str,
        path: str | None = None,
        prefix: str = "",
        token_exported: bool = False,
        token: str = DUMMY_TOKEN,
    ) -> subprocess.CompletedProcess[str]:
        environment = os.environ.copy()
        if path is not None:
            environment["PATH"] = f"{path}{os.pathsep}{environment['PATH']}"
        token_setup = (
            f"RELUTION_API_TOKEN={shlex.quote(token)}; export RELUTION_API_TOKEN; "
            if token_exported
            else (
                "typeset -g +x RELUTION_API_TOKEN; "
                f"RELUTION_API_TOKEN={shlex.quote(token)}; "
            )
        )
        shell_program = (
            prefix
            + f"source {shlex.quote(str(HELPER))}; "
            + token_setup
            + f"RELUTION_API_SERVER={shlex.quote(SERVER)}; "
            + "relution_curl "
            + " ".join(shlex.quote(argument) for argument in arguments)
        )
        return subprocess.run(
            ["zsh", "-fc", shell_program],
            env=environment,
            check=False,
            capture_output=True,
            text=True,
        )

    def test_zsh_syntax(self) -> None:
        result = subprocess.run(
            ["zsh", "-n", str(HELPER)],
            check=False,
            capture_output=True,
            text=True,
        )
        self.assertEqual(result.returncode, 0, result.stderr)

    def test_execution_defines_no_program_behavior(self) -> None:
        result = subprocess.run(
            ["zsh", str(HELPER)],
            check=False,
            capture_output=True,
            text=True,
        )
        self.assertEqual(result.returncode, 0, result.stderr)
        self.assertEqual(result.stdout, "")
        self.assertEqual(result.stderr, "")

    def test_allowed_get_uses_pinned_pipe_authentication(self) -> None:
        with tempfile.TemporaryDirectory() as temporary_directory:
            temporary_path = Path(temporary_directory)
            fake_curl = temporary_path / "curl"
            fake_curl.write_text(
                textwrap.dedent(
                    f"""\
                    #!{sys.executable}
                    import os
                    import stat
                    import sys

                    token = {DUMMY_TOKEN!r}
                    assert stat.S_ISFIFO(os.fstat(0).st_mode), "curl stdin is not a pipe"
                    assert sys.stdin.read() == f'header = "X-User-Access-Token: {{token}}"\\n'
                    assert sys.argv[1:8] == ["--disable", "--config", "-", "--globoff", "--noproxy", "*", "--fail-with-body"]
                    assert sys.argv[8:] == [
                        "--silent", "--show-error", "--connect-timeout", "10",
                        "--max-time", "60", "--request", "GET", "--header",
                        "Accept: application/json", {ALLOWED_URL!r},
                    ]
                    assert all(token not in argument for argument in sys.argv)
                    assert all(token not in value for value in os.environ.values())
                    print("pipe-auth-ok")
                    """
                ),
                encoding="utf-8",
            )
            fake_curl.chmod(0o755)

            result = self.run_helper(
                "--fail-with-body",
                "--silent",
                "--show-error",
                "--connect-timeout",
                "10",
                "--max-time",
                "60",
                "--request",
                "GET",
                "--header",
                "Accept: application/json",
                ALLOWED_URL,
                path=str(temporary_path),
            )

            self.assertEqual(result.returncode, 0, result.stderr)
            self.assertEqual(result.stdout.strip(), "pipe-auth-ok")

    def test_builtin_print_bypasses_hostile_alias_and_function(self) -> None:
        with tempfile.TemporaryDirectory() as temporary_directory:
            temporary_path = Path(temporary_directory)
            fake_curl = temporary_path / "curl"
            fake_curl.write_text(
                textwrap.dedent(
                    f"""\
                    #!{sys.executable}
                    import sys

                    token = {DUMMY_TOKEN!r}
                    assert sys.stdin.read() == f'header = "X-User-Access-Token: {{token}}"\\n'
                    print("pipe-auth-ok")
                    """
                ),
                encoding="utf-8",
            )
            fake_curl.chmod(0o755)

            for prefix in (
                "alias print='print -u2 alias-intercepted'; ",
                "function print() { builtin print -r -- function-intercepted >&2; }; ",
            ):
                with self.subTest(prefix=prefix):
                    result = self.run_helper(
                        ALLOWED_URL,
                        path=str(temporary_path),
                        prefix=prefix,
                    )

                    self.assertEqual(result.returncode, 0, result.stderr)
                    self.assertEqual(result.stdout.strip(), "pipe-auth-ok")
                    self.assertNotIn("intercepted", result.stderr)

    def test_config_escapes_token_backslashes_and_quotes(self) -> None:
        token = 'token\\with"quote'
        with tempfile.TemporaryDirectory() as temporary_directory:
            temporary_path = Path(temporary_directory)
            fake_curl = temporary_path / "curl"
            fake_curl.write_text(
                textwrap.dedent(
                    f"""\
                    #!{sys.executable}
                    import os
                    import sys

                    token = {token!r}
                    escaped = token.replace("\\\\", "\\\\\\\\").replace('"', '\\\\"')
                    assert sys.stdin.read() == f'header = "X-User-Access-Token: {{escaped}}"\\n'
                    assert all(token not in argument for argument in sys.argv)
                    assert all(token not in value for value in os.environ.values())
                    print("escaped-pipe-auth-ok")
                    """
                ),
                encoding="utf-8",
            )
            fake_curl.chmod(0o755)

            result = self.run_helper(
                ALLOWED_URL,
                path=str(temporary_path),
                token=token,
            )

            self.assertEqual(result.returncode, 0, result.stderr)
            self.assertEqual(result.stdout.strip(), "escaped-pipe-auth-ok")

    def test_exported_token_is_rejected_before_curl_invocation(self) -> None:
        with tempfile.TemporaryDirectory() as temporary_directory:
            temporary_path = Path(temporary_directory)
            fake_curl = temporary_path / "curl"
            fake_curl.write_text(
                f"#!{sys.executable}\nimport sys\nsys.exit(77)\n",
                encoding="utf-8",
            )
            fake_curl.chmod(0o755)

            result = self.run_helper(
                ALLOWED_URL,
                path=str(temporary_path),
                token_exported=True,
            )

            self.assertEqual(result.returncode, 2)
            self.assertIn("unexported shell variable", result.stderr)
            self.assertNotIn(DUMMY_TOKEN, result.stderr)

    def test_curl_exit_status_propagates(self) -> None:
        with tempfile.TemporaryDirectory() as temporary_directory:
            temporary_path = Path(temporary_directory)
            fake_curl = temporary_path / "curl"
            fake_curl.write_text(
                f"#!{sys.executable}\nimport sys\nsys.exit(37)\n",
                encoding="utf-8",
            )
            fake_curl.chmod(0o755)

            result = self.run_helper(ALLOWED_URL, path=str(temporary_path))

            self.assertEqual(result.returncode, 37)

    def test_allowed_patch_with_runbook_evidence_outputs(self) -> None:
        with tempfile.TemporaryDirectory() as temporary_directory:
            temporary_path = Path(temporary_directory)
            fake_curl = temporary_path / "curl"
            fake_curl.write_text(
                f"#!{sys.executable}\nimport sys\nprint('|'.join(sys.argv[1:]))\n",
                encoding="utf-8",
            )
            fake_curl.chmod(0o755)
            request_file = temporary_path / "request.json"
            request_file.write_text("{}", encoding="utf-8")
            response_file = temporary_path / "response.json"
            headers_file = temporary_path / "response.headers"

            result = self.run_helper(
                "--request",
                "PATCH",
                "--header",
                "Accept: application/json",
                "--header",
                "Content-Type: application/json",
                "--data-binary",
                f"@{request_file}",
                "--dump-header",
                str(headers_file),
                "--output",
                str(response_file),
                "--write-out",
                "%{http_code}",
                ALLOWED_URL,
                path=str(temporary_path),
            )

            self.assertEqual(result.returncode, 0, result.stderr)
            self.assertIn(f"--data-binary|@{request_file}", result.stdout)
            self.assertIn(f"--dump-header|{headers_file}|--output|{response_file}", result.stdout)
            self.assertIn(f"--write-out|%{{http_code}}|{ALLOWED_URL}", result.stdout)

    def test_all_documented_request_methods_are_allowed(self) -> None:
        with tempfile.TemporaryDirectory() as temporary_directory:
            temporary_path = Path(temporary_directory)
            fake_curl = temporary_path / "curl"
            fake_curl.write_text(
                f"#!{sys.executable}\nimport sys\nprint('|'.join(sys.argv[1:]))\n",
                encoding="utf-8",
            )
            fake_curl.chmod(0o755)

            for method in ("GET", "POST", "PUT", "DELETE"):
                with self.subTest(method=method):
                    result = self.run_helper(
                        "--request", method, ALLOWED_URL, path=str(temporary_path)
                    )
                    self.assertEqual(result.returncode, 0, result.stderr)
                    self.assertIn(f"--request|{method}|{ALLOWED_URL}", result.stdout)

    def test_rejects_unsafe_options_and_ambiguous_short_bundles(self) -> None:
        unsafe_options = (
            "-vk",
            "--verbose",
            "--trace-ascii=-",
            "--location",
            "--insecure",
            "--proxy",
            "--resolve",
            "--libcurl=/private/tmp/curl.c",
            "--output=/private/tmp/response",
            "--config=alternate-config",
            "--header=X-User-Access-Token: replacement",
            "--user=operator:password",
            "--url=https://other.example.invalid/api/test",
        )
        for unsafe_option in unsafe_options:
            with self.subTest(option=unsafe_option):
                result = self.run_helper(unsafe_option, ALLOWED_URL)
                self.assertEqual(result.returncode, 2)
                self.assertIn("rejected", result.stderr)
                self.assertNotIn(DUMMY_TOKEN, result.stderr)

    def test_rejects_invalid_urls_and_multiple_destinations(self) -> None:
        invalid_urls = (
            "http://mdm.example.invalid/relution/api/test",
            "https://other.example.invalid/relution/api/test",
            "https://mdm.example.invalid/api/test",
            "https://mdm.example.invalid/relution/../api/test",
            "https://mdm.example.invalid/relution/%2e%2e/api/test",
            "https://mdm.example.invalid/relution/api/test#fragment",
            ALLOWED_URL,
            "https://mdm.example.invalid/relution/api/second",
        )
        if invalid_urls[-2] == ALLOWED_URL:
            result = self.run_helper(*invalid_urls[-2:])
            self.assertEqual(result.returncode, 2)
            self.assertIn("exactly one request URL", result.stderr)

        for invalid_url in invalid_urls[:-2]:
            with self.subTest(url=invalid_url):
                result = self.run_helper(invalid_url)
                self.assertEqual(result.returncode, 2)
                self.assertIn("Relution curl", result.stderr)

    def test_rejects_missing_server_and_disallowed_request_shapes(self) -> None:
        for arguments in (
            ("--request", "OPTIONS", ALLOWED_URL),
            ("--data-binary", "@-", ALLOWED_URL),
            ("--data-binary", "request.json", ALLOWED_URL),
            ("--header", "Authorization: Bearer replacement", ALLOWED_URL),
            ("--header", f"Accept: {DUMMY_TOKEN}", ALLOWED_URL),
            ("--connect-timeout=10", ALLOWED_URL),
        ):
            with self.subTest(arguments=arguments):
                result = self.run_helper(*arguments)
                self.assertEqual(result.returncode, 2)
                self.assertIn("Relution curl", result.stderr)

    def test_rejects_unsafe_evidence_output_forms(self) -> None:
        for arguments in (
            ("--output", "-", ALLOWED_URL),
            ("--dump-header", "-", ALLOWED_URL),
            ("--output=/private/tmp/response", ALLOWED_URL),
            ("--write-out", "%{url_effective}", ALLOWED_URL),
            ("--write-out=%{http_code}", ALLOWED_URL),
        ):
            with self.subTest(arguments=arguments):
                result = self.run_helper(*arguments)
                self.assertEqual(result.returncode, 2)
                self.assertIn("Relution curl", result.stderr)

        shell_program = (
            f"source {shlex.quote(str(HELPER))}; "
            "typeset -g +x RELUTION_API_TOKEN; "
            f"RELUTION_API_TOKEN={shlex.quote(DUMMY_TOKEN)}; "
            f"relution_curl {shlex.quote(ALLOWED_URL)}"
        )
        result = subprocess.run(
            ["zsh", "-fc", shell_program],
            check=False,
            capture_output=True,
            text=True,
        )
        self.assertEqual(result.returncode, 2)
        self.assertIn("RELUTION_API_SERVER", result.stderr)


if __name__ == "__main__":
    unittest.main()
