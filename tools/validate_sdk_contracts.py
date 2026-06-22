#!/usr/bin/env python3
"""Validate the public SDK contract surface (schemas + examples).

This script enforces, in one place, the schema/example consistency checks that
Phase 6P verified manually (see docs/verification/phase-6p-sdk-live-verification-b2-dd3.md,
command #9). It is intentionally minimal and has no dependency on the private
Core or any provider API.

What it checks
--------------
1. JSON well-formedness of every JSON file under schemas/ and examples/.
2. JSON Schema meta-validation of the active schemas (schemas/*.schema.json),
   if the `jsonschema` package is available.
3. Validation of clearly-mapped active examples against their active schema,
   if `jsonschema` is available.
4. OpenAPI YAML well-formedness (openapi/openapi.yaml + openapi/openapi_v0_4.yaml),
   if `pyyaml` is available.

Scope / boundary
----------------
- Retired / reference-only artifacts (schemas/v0_4/*, examples/v0_4_api_examples/*,
  openapi/openapi_v0_4.yaml) are JSON/YAML-parsed only. They are NOT meta-validated
  as active and their examples are NOT bound to active schemas.
- examples/invoices/invoice_with_qr_payload.json is an intentional raw `/normalize`
  input with no schema binding (Phase 6P observation O1); it is parsed but not
  validated against a schema.

Exit codes
----------
0  all checks that could run passed.
1  one or more real errors (bad JSON, invalid schema, example failed validation,
   malformed OpenAPI YAML).

Run from the repository root:
    python3 tools/validate_sdk_contracts.py
"""
from __future__ import annotations

import json
import sys
from pathlib import Path

REPO_ROOT = Path(__file__).resolve().parent.parent

# --- Active example -> active schema mappings (single-object examples). --------
# Keep these explicit. Only add a mapping when the binding is clear.
EXAMPLE_TO_SCHEMA = {
    "examples/invoices/invoice_normalized.json": "schemas/invoice.schema.json",
    "examples/invoices/invoice_with_po.json": "schemas/invoice.schema.json",
    "examples/invoices/invoice_without_po.json": "schemas/invoice.schema.json",
    "examples/match_results/green_match.json": "schemas/match_result.schema.json",
    "examples/match_results/yellow_match.json": "schemas/match_result.schema.json",
    "examples/match_results/red_match.json": "schemas/match_result.schema.json",
    "examples/materials/material_with_aliases.json": "schemas/material.schema.json",
    "examples/feedback/accepted_match.json": "schemas/feedback.schema.json",
    "examples/feedback/corrected_match.json": "schemas/feedback.schema.json",
    "examples/feedback/rejected_match.json": "schemas/feedback.schema.json",
}

# Array examples: each list item validates against the mapped schema.
ARRAY_EXAMPLE_TO_SCHEMA = {
    "examples/materials/material_master.json": "schemas/material.schema.json",
}

# Reference-only / unbound — parsed but deliberately NOT schema-validated.
REFERENCE_ONLY_NOTE = {
    "examples/invoices/invoice_with_qr_payload.json": "raw /normalize input, no schema binding (O1)",
}


def rel(p: Path) -> str:
    return p.relative_to(REPO_ROOT).as_posix()


def load_json(path: Path):
    return json.loads(path.read_text(encoding="utf-8"))


def main() -> int:
    errors: list[str] = []
    notes: list[str] = []

    print("== SDK contract validation ==")
    print(f"repo root: {REPO_ROOT}")

    # --- 1. JSON well-formedness across the contract surface. -----------------
    json_files = sorted(
        list((REPO_ROOT / "schemas").rglob("*.json"))
        + list((REPO_ROOT / "examples").rglob("*.json"))
    )
    parsed = 0
    for jf in json_files:
        try:
            load_json(jf)
            parsed += 1
        except Exception as exc:  # noqa: BLE001 - report any parse failure
            errors.append(f"JSON parse failed: {rel(jf)}: {exc}")
    print(f"[json] parsed {parsed}/{len(json_files)} JSON files under schemas/ + examples/")

    # --- 2 & 3. jsonschema-dependent checks. ----------------------------------
    try:
        from jsonschema import validate
        from jsonschema.validators import validator_for
        have_jsonschema = True
    except ImportError:
        have_jsonschema = False
        notes.append("jsonschema not installed -> skipped meta-validation and example validation")
        print("[schema] WARNING: jsonschema not installed; skipping meta + example validation")

    if have_jsonschema:
        # Active schemas = schemas/*.schema.json (NOT schemas/v0_4/*).
        active_schemas = sorted((REPO_ROOT / "schemas").glob("*.schema.json"))
        meta_ok = 0
        for sf in active_schemas:
            try:
                schema = load_json(sf)
                validator_for(schema).check_schema(schema)
                meta_ok += 1
            except Exception as exc:  # noqa: BLE001
                errors.append(f"schema meta-validation failed: {rel(sf)}: {exc}")
        print(f"[schema] meta-validated {meta_ok}/{len(active_schemas)} active schemas")

        # Mapped single-object examples.
        validated = 0
        for ex_rel, sch_rel in EXAMPLE_TO_SCHEMA.items():
            ex_path = REPO_ROOT / ex_rel
            sch_path = REPO_ROOT / sch_rel
            try:
                validate(load_json(ex_path), load_json(sch_path))
                validated += 1
            except Exception as exc:  # noqa: BLE001
                errors.append(f"example failed validation: {ex_rel} -> {sch_rel}: {exc}")

        # Mapped array examples (validate each item).
        for ex_rel, sch_rel in ARRAY_EXAMPLE_TO_SCHEMA.items():
            ex_path = REPO_ROOT / ex_rel
            sch_path = REPO_ROOT / sch_rel
            try:
                schema = load_json(sch_path)
                data = load_json(ex_path)
                if not isinstance(data, list):
                    errors.append(f"expected JSON array: {ex_rel}")
                    continue
                for i, item in enumerate(data):
                    validate(item, schema)
                validated += 1
            except Exception as exc:  # noqa: BLE001
                errors.append(f"array example failed validation: {ex_rel} -> {sch_rel}: {exc}")

        total_mapped = len(EXAMPLE_TO_SCHEMA) + len(ARRAY_EXAMPLE_TO_SCHEMA)
        print(f"[schema] validated {validated}/{total_mapped} mapped example sets against active schemas")

    for ref_rel, why in REFERENCE_ONLY_NOTE.items():
        if (REPO_ROOT / ref_rel).exists():
            print(f"[skip ] {ref_rel}: {why}")
    if (REPO_ROOT / "schemas" / "v0_4").is_dir():
        print("[skip ] schemas/v0_4/*: retired / reference-only (parsed only, not meta-validated)")
    if (REPO_ROOT / "examples" / "v0_4_api_examples").is_dir():
        print("[skip ] examples/v0_4_api_examples/*: retired / reference-only (parsed only)")

    # --- 4. OpenAPI YAML well-formedness. -------------------------------------
    openapi_files = [
        REPO_ROOT / "openapi" / "openapi.yaml",
        REPO_ROOT / "openapi" / "openapi_v0_4.yaml",
    ]
    try:
        import yaml
        have_yaml = True
    except ImportError:
        have_yaml = False
        notes.append("pyyaml not installed -> skipped OpenAPI YAML parse")
        print("[yaml ] WARNING: pyyaml not installed; skipping OpenAPI YAML parse")

    if have_yaml:
        yaml_ok = 0
        for yf in openapi_files:
            if not yf.exists():
                continue
            try:
                yaml.safe_load(yf.read_text(encoding="utf-8"))
                yaml_ok += 1
            except Exception as exc:  # noqa: BLE001
                errors.append(f"OpenAPI YAML parse failed: {rel(yf)}: {exc}")
        print(f"[yaml ] parsed {yaml_ok} OpenAPI file(s)")

    # --- Summary. -------------------------------------------------------------
    print("-" * 60)
    if notes:
        for n in notes:
            print(f"NOTE: {n}")
    if errors:
        print(f"FAILED with {len(errors)} error(s):")
        for e in errors:
            print(f"  - {e}")
        return 1
    print("PASS: all contract checks that could run passed.")
    return 0


if __name__ == "__main__":
    sys.exit(main())
