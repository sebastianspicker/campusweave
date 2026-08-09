"""Public strict JSON snapshot API."""

from strict_json_checks import (
    MAX_JSON_BYTES,
    DuplicateKey,
    decode_strict_json,
    load_strict_json,
    read_json_snapshot,
)

__all__ = [
    "MAX_JSON_BYTES",
    "DuplicateKey",
    "decode_strict_json",
    "load_strict_json",
    "read_json_snapshot",
]
