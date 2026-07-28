#!/usr/bin/env python3
"""Validate Relution machine-readable documentation offline."""

from __future__ import annotations

import importlib
import sys
from pathlib import Path

SCRIPT_ROOT = Path(__file__).resolve().parent
if str(SCRIPT_ROOT) not in sys.path:
    sys.path.insert(0, str(SCRIPT_ROOT))

_bindings = importlib.import_module("machine_docs_bindings")
_catalog = importlib.import_module("machine_docs_catalog")
_change_plan = importlib.import_module("machine_docs_change_plan")
_common = importlib.import_module("machine_docs_common")
_coordinator = importlib.import_module("machine_docs_coordinator")
main = _coordinator.main
_parse_args = _coordinator.parse_args
_validate_all = _coordinator.validate_all

API_BINDING_FIELDS = _common.API_BINDING_FIELDS
APPROVAL_LEVELS = _common.APPROVAL_LEVELS
ASSERTION_KEYS = _common.ASSERTION_KEYS
ASSERTION_OPERATORS = _common.ASSERTION_OPERATORS
ASSERTION_SOURCES = _common.ASSERTION_SOURCES
AUDIT_EVIDENCE_SOURCES = _common.AUDIT_EVIDENCE_SOURCES
AUDIT_PLAN_KEYS = _common.AUDIT_PLAN_KEYS
AUDIT_PLAN_MODES = _common.AUDIT_PLAN_MODES
AUTHORIZATION_KEYS = _common.AUTHORIZATION_KEYS
BINDING_ROLES = _common.BINDING_ROLES
BINDING_ROLE_METHODS = _common.BINDING_ROLE_METHODS
CHANGE_KEYS = _common.CHANGE_KEYS
CHANGE_PLAN_CONTRACT_KEYS = _common.CHANGE_PLAN_CONTRACT_KEYS
CHANGE_PLAN_OPERATION_KEYS = _common.CHANGE_PLAN_OPERATION_KEYS
CHANGE_PLAN_ROOT_KEYS = _common.CHANGE_PLAN_ROOT_KEYS
CHANGE_PLAN_TARGET_KEYS = _common.CHANGE_PLAN_TARGET_KEYS
CLIENT_OPERATION_SURFACE = _common.CLIENT_OPERATION_SURFACE
CONCEPT_ID = _common.CONCEPT_ID
CONCEPT_RECORD_KEYS = _common.CONCEPT_RECORD_KEYS
CONCEPT_TOP_LEVEL_KEYS = _common.CONCEPT_TOP_LEVEL_KEYS
DATE = _common.DATE
DEFAULT_BINDINGS = _common.DEFAULT_BINDINGS
DEFAULT_CATALOG = _common.DEFAULT_CATALOG
DEFAULT_CHANGE_PLAN = _common.DEFAULT_CHANGE_PLAN
DEFAULT_MANIFEST = _common.DEFAULT_MANIFEST
EVIDENCE_CLASSES = _common.EVIDENCE_CLASSES
FUNCTIONAL_CHECK_RESULTS = _common.FUNCTIONAL_CHECK_RESULTS
HTTP_METHOD = _common.HTTP_METHOD
IMPACT_KEYS = _common.IMPACT_KEYS
MANIFEST_KEYS = _common.MANIFEST_KEYS
MAX_APPROVAL_CLOCK_SKEW = _common.MAX_APPROVAL_CLOCK_SKEW
MAX_IMMEDIATE_APPROVAL_AGE = _common.MAX_IMMEDIATE_APPROVAL_AGE
MUTATING_BINDING_ROLES = _common.MUTATING_BINDING_ROLES
NON_MUTATING_METHODS = _common.NON_MUTATING_METHODS
OPERATION_KEY = _common.OPERATION_KEY
OPERATION_SURFACES = _common.OPERATION_SURFACES
PLAN_OPERATION_ROLES = _common.PLAN_OPERATION_ROLES
PLAN_ROLE_BINDING_ROLES = _common.PLAN_ROLE_BINDING_ROLES
PUBLIC_API_KEYS = _common.PUBLIC_API_KEYS
PUBLIC_API_OPERATION_KEYS = _common.PUBLIC_API_OPERATION_KEYS
READ_LIKE_METHODS = _common.READ_LIKE_METHODS
READ_ONLY_BINDING_ROLES = _common.READ_ONLY_BINDING_ROLES
REGISTRY_DOCUMENT_TYPES = _common.REGISTRY_DOCUMENT_TYPES
RELATED_KINDS = _common.RELATED_KINDS
REPOSITORY_ROOT = _common.REPOSITORY_ROOT
REQUEST_KEYS = _common.REQUEST_KEYS
REQUIRED_AUDIT_MATCH_FIELDS = _common.REQUIRED_AUDIT_MATCH_FIELDS
RESOURCE_KEYS = _common.RESOURCE_KEYS
RESOURCE_SCOPES = _common.RESOURCE_SCOPES
RESULT_ENUMS = _common.RESULT_ENUMS
RESULT_KEYS = _common.RESULT_KEYS
RISK_TIERS = _common.RISK_TIERS
ROLLBACK_EXECUTION_MODES = _common.ROLLBACK_EXECUTION_MODES
ROLLBACK_KEYS = _common.ROLLBACK_KEYS
ROLLBACK_STRATEGIES = _common.ROLLBACK_STRATEGIES
SCHEMA_VERSION = _common.SCHEMA_VERSION
SCOPE_KINDS = _common.SCOPE_KINDS
SCOPE_LOCATIONS = _common.SCOPE_LOCATIONS
SHA256 = _common.SHA256
STATIC_EVIDENCE_CLASSES = _common.STATIC_EVIDENCE_CLASSES
TARGET_BINDING_CONTRACT_KEYS = _common.TARGET_BINDING_CONTRACT_KEYS
TARGET_BINDING_RECORD_KEYS = _common.TARGET_BINDING_RECORD_KEYS
TARGET_BINDING_ROOT_KEYS = _common.TARGET_BINDING_ROOT_KEYS
TARGET_BINDING_TARGET_KEYS = _common.TARGET_BINDING_TARGET_KEYS
TARGET_OPERATION_BINDING_KEYS = _common.TARGET_OPERATION_BINDING_KEYS
TARGET_SCOPE_BINDING_KEYS = _common.TARGET_SCOPE_BINDING_KEYS
VERIFICATION_KEYS = _common.VERIFICATION_KEYS

binding_role_index = _bindings.binding_role_index
schema_refs = _catalog.schema_refs
request_body_media_types = importlib.import_module(
    "machine_docs_catalog_operations"
).request_body_media_types
validate_operation_reference = importlib.import_module(
    "machine_docs_catalog_operations"
).validate_operation_reference
_support = importlib.import_module("machine_docs_common_support")
catalog_digest = _support.catalog_digest
error = _support.error
expect_list = _support.expect_list
expect_mapping = _support.expect_mapping
nested_references = _support.nested_references
parse_timestamp = _support.parse_timestamp
pointer_exists = _support.pointer_exists
relative = _support.relative
require_exact_keys = _support.require_exact_keys
validate_https_url = _support.validate_https_url
validate_string_array = _support.validate_string_array
manifest_registry_paths = importlib.import_module(
    "machine_docs_coordinator_manifest"
).manifest_registry_paths


def validate_catalog(*args: object, **kwargs: object) -> object:
    """Preserve the historical validator module API."""
    return _catalog.validate_catalog(*args, **kwargs)


def validate_bindings(*args: object, **kwargs: object) -> object:
    """Preserve the historical validator module API."""
    return _bindings.validate_bindings(*args, **kwargs)


def parse_args(*args: object, **kwargs: object) -> object:
    """Preserve the historical validator module API."""
    return _parse_args(*args, **kwargs)


def validate_all(*args: object, **kwargs: object) -> object:
    """Preserve the historical validator module API."""
    return _validate_all(*args, **kwargs)


ValidationFailure = _common.ValidationFailure
load_json = _common.load_json
validate_catalog_freshness = _common.validate_catalog_freshness
validate_schema_references = _common.validate_schema_references
operation_key = _catalog.operation_key
validate_concept_registry = _catalog.validate_concept_registry
validate_public_api_registry = _catalog.validate_public_api_registry
validate_change_plan = _change_plan.validate_change_plan


__all__ = (
    "API_BINDING_FIELDS", "APPROVAL_LEVELS", "ASSERTION_KEYS", "ASSERTION_OPERATORS",
    "ASSERTION_SOURCES", "AUDIT_EVIDENCE_SOURCES", "AUDIT_PLAN_KEYS", "AUDIT_PLAN_MODES",
    "AUTHORIZATION_KEYS", "BINDING_ROLES", "BINDING_ROLE_METHODS", "CHANGE_KEYS",
    "CHANGE_PLAN_CONTRACT_KEYS", "CHANGE_PLAN_OPERATION_KEYS", "CHANGE_PLAN_ROOT_KEYS",
    "CHANGE_PLAN_TARGET_KEYS", "CLIENT_OPERATION_SURFACE", "CONCEPT_ID", "CONCEPT_RECORD_KEYS",
    "CONCEPT_TOP_LEVEL_KEYS", "DATE", "DEFAULT_BINDINGS", "DEFAULT_CATALOG",
    "DEFAULT_CHANGE_PLAN", "DEFAULT_MANIFEST", "EVIDENCE_CLASSES", "FUNCTIONAL_CHECK_RESULTS",
    "HTTP_METHOD", "IMPACT_KEYS", "MANIFEST_KEYS", "MAX_APPROVAL_CLOCK_SKEW",
    "MAX_IMMEDIATE_APPROVAL_AGE", "MUTATING_BINDING_ROLES", "NON_MUTATING_METHODS",
    "OPERATION_KEY", "OPERATION_SURFACES", "PLAN_OPERATION_ROLES", "PLAN_ROLE_BINDING_ROLES",
    "PUBLIC_API_KEYS", "PUBLIC_API_OPERATION_KEYS", "READ_LIKE_METHODS", "READ_ONLY_BINDING_ROLES",
    "REGISTRY_DOCUMENT_TYPES", "RELATED_KINDS", "REPOSITORY_ROOT", "REQUEST_KEYS",
    "REQUIRED_AUDIT_MATCH_FIELDS", "RESOURCE_KEYS", "RESOURCE_SCOPES", "RESULT_ENUMS",
    "RESULT_KEYS", "RISK_TIERS", "ROLLBACK_EXECUTION_MODES", "ROLLBACK_KEYS",
    "ROLLBACK_STRATEGIES", "SCHEMA_VERSION", "SCOPE_KINDS", "SCOPE_LOCATIONS", "SHA256",
    "STATIC_EVIDENCE_CLASSES", "TARGET_BINDING_CONTRACT_KEYS", "TARGET_BINDING_RECORD_KEYS",
    "TARGET_BINDING_ROOT_KEYS", "TARGET_BINDING_TARGET_KEYS", "TARGET_OPERATION_BINDING_KEYS",
    "TARGET_SCOPE_BINDING_KEYS", "VERIFICATION_KEYS", "ValidationFailure", "binding_role_index",
    "catalog_digest", "error", "expect_list", "expect_mapping", "load_json", "main",
    "manifest_registry_paths", "nested_references", "operation_key", "parse_args",
    "parse_timestamp",
    "pointer_exists", "relative", "request_body_media_types", "require_exact_keys", "schema_refs",
    "validate_all", "validate_bindings", "validate_catalog", "validate_catalog_freshness",
    "validate_change_plan", "validate_concept_registry", "validate_https_url",
    "validate_operation_reference", "validate_public_api_registry", "validate_schema_references",
    "validate_string_array",
)


if __name__ == "__main__":
    raise SystemExit(main())
