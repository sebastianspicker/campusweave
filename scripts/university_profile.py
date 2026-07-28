#!/usr/bin/env python3
"""Validate an inert, institution-neutral university Relution profile."""

from __future__ import annotations

import argparse
import importlib
import sys
from pathlib import Path
from typing import Iterable

SCRIPT_ROOT = Path(__file__).resolve().parent
if str(SCRIPT_ROOT) not in sys.path:
    sys.path.insert(0, str(SCRIPT_ROOT))

_constants = importlib.import_module("university_profile_constants")
_helpers = importlib.import_module("university_profile_helpers")
_validation = importlib.import_module("university_profile_validation")

ASSIGNMENT_KEYS = _constants.ASSIGNMENT_KEYS
BINDING_ROLES = _constants.BINDING_ROLES
BYOD_ALLOWED_CAPABILITIES = _constants.BYOD_ALLOWED_CAPABILITIES
BYOD_PROHIBITIONS = _constants.BYOD_PROHIBITIONS
COHORT_KEYS = _constants.COHORT_KEYS
COMMIT_BOUNDARY_KEYS = _constants.COMMIT_BOUNDARY_KEYS
CONCRETE_PLATFORMS = _constants.CONCRETE_PLATFORMS
CONTROL_KEYS = _constants.CONTROL_KEYS
DEFAULT_MANIFEST = _constants.DEFAULT_MANIFEST
DEFAULT_PACKAGE = _constants.DEFAULT_PACKAGE
DEPARTMENT_RULE_KEYS = _constants.DEPARTMENT_RULE_KEYS
EMAIL = _constants.EMAIL
FORBIDDEN_KEYS = _constants.FORBIDDEN_KEYS
FORBIDDEN_NORMALIZED_KEYS = _constants.FORBIDDEN_NORMALIZED_KEYS
GATE_KEYS = _constants.GATE_KEYS
GROUP_KEYS = _constants.GROUP_KEYS
ID_PATTERNS = _constants.ID_PATTERNS
INTENT_SETTING_CONTRACTS = _constants.INTENT_SETTING_CONTRACTS
INTENT_SETTING_KEYS = _constants.INTENT_SETTING_KEYS
LAYER_KEYS = _constants.LAYER_KEYS
LOCATION_KEYS = _constants.LOCATION_KEYS
MAX_DOCUMENT_BYTES = _constants.MAX_DOCUMENT_BYTES
MODELS = _constants.MODELS
MUTATION_BINDING_ROLES = _constants.MUTATION_BINDING_ROLES
NON_PROMOTION_RINGS = _constants.NON_PROMOTION_RINGS
ORG_KEYS = _constants.ORG_KEYS
PACKAGE_KEYS = _constants.PACKAGE_KEYS
PLATFORMS = _constants.PLATFORMS
POLICY_KEYS = _constants.POLICY_KEYS
PROMOTION_CHAIN = _constants.PROMOTION_CHAIN
PROVENANCE_KEYS = _constants.PROVENANCE_KEYS
REPOSITORY_ROOT = _constants.REPOSITORY_ROOT
REQUIRED_GROUP_DIMENSIONS = _constants.REQUIRED_GROUP_DIMENSIONS
REQUIRED_WORKFLOW_SUFFIXES = _constants.REQUIRED_WORKFLOW_SUFFIXES
RING_KEYS = _constants.RING_KEYS
RING_MACHINE_RULES = _constants.RING_MACHINE_RULES
ROOT_KEYS = _constants.ROOT_KEYS
SECRET_TEXT = _constants.SECRET_TEXT
SOURCE_KEYS = _constants.SOURCE_KEYS
UNRESOLVED_KEYS = _constants.UNRESOLVED_KEYS
URL = _constants.URL
UUID = _constants.UUID
WORKFLOW_KEYS = _constants.WORKFLOW_KEYS
WORKFLOW_MINIMUM_ROLES_BY_SUFFIX = _constants.WORKFLOW_MINIMUM_ROLES_BY_SUFFIX
add = _helpers.add
array = _helpers.array
concept_ids_from_manifest = _helpers.concept_ids_from_manifest
exact_keys = _helpers.exact_keys
load_json = _helpers.load_json
mapping = _helpers.mapping
records = _helpers.records
require_reference = _helpers.require_reference
require_references = _helpers.require_references
scan_commit_boundary = _helpers.scan_commit_boundary
string_list = _helpers.string_list
validate_acyclic = _helpers.validate_acyclic
validate_package = _validation.validate_package


__all__ = (
    "ASSIGNMENT_KEYS", "BINDING_ROLES", "BYOD_ALLOWED_CAPABILITIES", "BYOD_PROHIBITIONS",
    "COHORT_KEYS", "COMMIT_BOUNDARY_KEYS", "CONCRETE_PLATFORMS", "CONTROL_KEYS",
    "DEFAULT_MANIFEST", "DEFAULT_PACKAGE", "DEPARTMENT_RULE_KEYS", "EMAIL", "FORBIDDEN_KEYS",
    "FORBIDDEN_NORMALIZED_KEYS", "GATE_KEYS", "GROUP_KEYS", "ID_PATTERNS",
    "INTENT_SETTING_CONTRACTS", "INTENT_SETTING_KEYS", "LAYER_KEYS", "LOCATION_KEYS",
    "MAX_DOCUMENT_BYTES", "MODELS", "MUTATION_BINDING_ROLES", "NON_PROMOTION_RINGS",
    "ORG_KEYS", "PACKAGE_KEYS", "PLATFORMS", "POLICY_KEYS", "PROMOTION_CHAIN",
    "PROVENANCE_KEYS", "REPOSITORY_ROOT", "REQUIRED_GROUP_DIMENSIONS",
    "REQUIRED_WORKFLOW_SUFFIXES", "RING_KEYS", "RING_MACHINE_RULES", "ROOT_KEYS",
    "SECRET_TEXT", "SOURCE_KEYS", "UNRESOLVED_KEYS", "URL", "UUID", "WORKFLOW_KEYS",
    "WORKFLOW_MINIMUM_ROLES_BY_SUFFIX", "add", "array", "concept_ids_from_manifest",
    "exact_keys", "load_json", "main", "mapping", "parse_args", "records",
    "require_reference", "require_references", "scan_commit_boundary", "string_list",
    "validate_acyclic", "validate_package",
)


def parse_args(argv: Iterable[str] | None = None) -> argparse.Namespace:
    """Parse offline profile-validation arguments."""
    parser = argparse.ArgumentParser(
        description=(
            "Validate the non-executable Reference University Relution desired-state "
            "package."
        )
    )
    parser.add_argument("--package", type=Path, default=DEFAULT_PACKAGE)
    parser.add_argument("--manifest", type=Path, default=DEFAULT_MANIFEST)
    return parser.parse_args(argv)


def main(argv: Iterable[str] | None = None) -> int:
    """Validate the requested offline profile and report its result."""
    args = parse_args(argv)
    bootstrap_errors: list[str] = []
    concept_ids = concept_ids_from_manifest(args.manifest, bootstrap_errors)
    try:
        document = load_json(args.package)
    except ValueError as exc:
        bootstrap_errors.append(str(exc))
        document = None
    errors = bootstrap_errors + (
        validate_package(document, concept_ids) if document is not None else []
    )
    if errors:
        for item in sorted(set(errors)):
            print(f"error: {args.package}:{item}", file=sys.stderr)
        print(f"validation failed: {len(set(errors))} error(s)", file=sys.stderr)
        return 1
    print(
        "valid: Reference University offline desired state is non-executable, reference-closed, "
        "target-contract blocked, and free of forbidden target/contact/credential patterns"
    )
    return 0


if __name__ == "__main__":
    raise SystemExit(main())
