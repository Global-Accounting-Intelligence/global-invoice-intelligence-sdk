# Phase 6Q — SDK CI Validation Gates

**Status:** CI hardening record. Advisory. Implements the Phase 6P remaining-risk
recommendation (R1/F3). Not a redesign, not a new architecture phase.
**Date:** 2026-06-23.

---

## 1. Branch name

`phase-6q-sdk-ci-validation-gates`

(`main` was not modified. All work is confined to this branch's working tree.)

## 2. Scope

Add minimal CI validation gates so the checks Phase 6P ran **manually** are enforced
**automatically** on every pull request and on pushes to `main`. The checks themselves are
unchanged: JSON/schema/example contract validation, the Python SDK test, and the JavaScript
SDK test.

In scope:

- one GitHub Actions workflow (`.github/workflows/sdk-validation.yml`);
- one small, dependency-light validation script (`tools/validate_sdk_contracts.py`) that
  consolidates the schema/example consistency check Phase 6P performed inline (§5 command #9
  of the 6P report);
- this verification note.

Explicitly **out of scope** (per task hard rules): modifying `main`; private-Core logic;
provider-specific runtime dependencies; secrets/credentials/API keys; BYOK / managed-processing
orchestration; changes to the public/private boundary; product-strategy rewrites; fake tests;
claiming coverage for checks not actually run.

## 3. Files changed

| File | Change | Notes |
|------|--------|-------|
| `.github/workflows/sdk-validation.yml` | **added** | CI workflow with three jobs. |
| `tools/validate_sdk_contracts.py` | **added** | Consolidates the 6P schema/example/JSON/OpenAPI checks into one runnable script. |
| `docs/verification/phase-6q-sdk-ci-validation-gates.md` | **added** | This report. |

No existing source, schema, example, OpenAPI, SDK, or governance file was modified. The
existing repo tools (`tools/validate_invoice_schema.py`, `tools/validate_material_schema.py`)
were left unchanged and are invoked by CI as-is.

## 4. CI checks added

`.github/workflows/sdk-validation.yml` triggers on `pull_request` and `push` to `main`, with
three independent jobs:

1. **`contracts` (Schemas & examples)** — Python 3.10; installs `jsonschema` + `pyyaml`; runs:
   - `python tools/validate_invoice_schema.py` (existing repo tool),
   - `python tools/validate_material_schema.py` (existing repo tool),
   - `python tools/validate_sdk_contracts.py` (new) — JSON well-formedness across
     `schemas/` + `examples/`, JSON Schema meta-validation of the 16 active schemas, validation
     of the 11 mapped active example sets against their active schema, and OpenAPI YAML
     well-formedness for both `openapi/*.yaml` files.
2. **`python-sdk` (Python SDK tests)** — Python 3.10; installs `pytest` + `httpx`; runs
   `python -m pytest -q` in `sdk/python/` (the exact 6P invocation).
3. **`javascript-sdk` (JavaScript SDK tests)** — Node 20; runs `npm test` in `sdk/javascript/`
   (which is `node tests/client.test.js`, the script the repo declares).

Stable actions only: `actions/checkout@v4`, `actions/setup-python@v5`, `actions/setup-node@v4`.
`permissions: contents: read` (least privilege). No secrets are referenced.

## 5. Why a new script (Step 4 decision)

The two existing tools only assert key-presence on two example files; they do **not** perform
the JSON Schema meta-validation or the example→schema validation that Phase 6P ran inline
(6P §5 command #9). Rather than leave that proven check un-enforceable, it is captured in one
explicit, maintainable script with no private-Core or provider dependency. The script:

- parses every JSON file under `schemas/` + `examples/` (39 files) for well-formedness;
- meta-validates the 16 **active** schemas (`schemas/*.schema.json`) if `jsonschema` is present;
- validates the clearly-mapped **active** examples (11 mapped sets) against their schema;
- treats retired / reference-only artifacts as parse-only and prints explicit skip lines:
  `schemas/v0_4/*`, `examples/v0_4_api_examples/*`, and the unbound raw input
  `examples/invoices/invoice_with_qr_payload.json` (6P observation O1);
- parses both `openapi/*.yaml` files if `pyyaml` is present;
- exits non-zero on any real error and prints a clear summary.

The example→schema mappings are listed explicitly in the script (no auto-guessing), matching
the bindings confirmed in 6P.

## 6. Local commands run

All commands executed against this branch's working tree (Linux sandbox: Node `v22.x`,
Python `3.10.12`). `pytest`/`httpx` were absent and installed to run the declared tests, as in
Phase 6P.

| # | Command | Purpose |
|---|---------|---------|
| 1 | `git rev-parse --abbrev-ref HEAD` / `git status --short` | branch + clean-tree baseline |
| 2 | `python3 tools/validate_invoice_schema.py` | existing repo tool |
| 3 | `python3 tools/validate_material_schema.py` | existing repo tool |
| 4 | `python3 tools/validate_sdk_contracts.py` | new contract gate (happy path) |
| 5 | negative test: copy repo, break one example + one schema, re-run the script | confirm the gate fails (exit 1) on real defects |
| 6 | `cd sdk/python && python3 -m pytest -q` | Python SDK test |
| 7 | `cd sdk/javascript && npm test` | JavaScript SDK test |
| 8 | `python3 -c "import yaml; yaml.safe_load(open('.github/workflows/sdk-validation.yml'))"` | workflow YAML well-formedness |

## 7. Results

- **Branch/state:** on `phase-6q-sdk-ci-validation-gates`; working tree clean before edits.
- **`validate_invoice_schema.py`:** PASS ("Invoice example basic validation passed.").
- **`validate_material_schema.py`:** PASS ("Material example basic validation passed.").
- **`validate_sdk_contracts.py` (happy path):** PASS, exit 0 — 39/39 JSON parsed,
  16/16 active schemas meta-validated, 11/11 mapped example sets validated, 2 OpenAPI files
  parsed; retired/unbound artifacts correctly skipped.
- **`validate_sdk_contracts.py` (negative test):** correctly FAILED with exit 1, reporting the
  broken schema and the broken example — confirming the gate is real, not a no-op. Repo copy
  discarded; no repo files were changed by the test.
- **Python SDK test:** PASS (`1 passed`).
- **JavaScript SDK test:** PASS (prints `true`, exit 0).
- **Workflow YAML:** parses cleanly; jobs = `contracts`, `python-sdk`, `javascript-sdk`;
  triggers = `pull_request` + `push` to `main`.

Note: under the sandbox's `jsonschema 3.2.0`, meta-validation emits a `DeprecationWarning`
because that old release does not bundle the draft-2020-12 metaschema and falls back to the
latest known draft. CI installs current `jsonschema` (4.x), which has the 2020-12 metaschema
and validates without the warning. Result (PASS) is identical in both cases.

## 8. Limitations

- The CI jobs were validated by running the **same commands locally** and by parsing the
  workflow YAML; the GitHub-hosted run itself cannot be exercised from this environment, so the
  first real CI run will occur when the branch/PR is pushed.
- The `contracts` gate covers the JSON/schema/example/OpenAPI surface. It does **not** perform
  deep OpenAPI semantic linting (e.g. Spectral) or `$ref`-resolved cross-document validation —
  out of scope for this minimal hardening pass.
- Example→schema coverage equals the explicit mappings (the same set 6P validated). The one
  unbound raw input (`invoice_with_qr_payload.json`) remains intentionally un-validated.
- The Python test job installs `httpx` + `pytest` directly (matching 6P and the declared
  `pyproject.toml` runtime dep); there is no separate dev-dependency group to install from.

## 9. Remaining risks

- **R1 (resolved by this change):** Phase 6P R1/F3 (no CI). The 6P checks are now enforced on
  PRs and on pushes to `main`. Residual: the gate only protects what is mapped; a brand-new
  example with no mapping would be JSON-parsed but not schema-validated until a mapping is added.
- **R2 (low, unchanged from 6P):** SDK client parity (JS client lacks `send_feedback`). Not a
  contract violation; not addressed here. Backlog item.
- **R3 (low, unchanged from 6P):** `invoice_with_qr_payload.json` has no schema binding;
  remains parse-only until `/normalize` input contracts are formalized. *Post-MVP.*
- **R4 (process):** schema/example mappings live in `tools/validate_sdk_contracts.py` and must
  be extended when new bound contracts/examples are added; otherwise new examples escape schema
  validation. Cheap to maintain; called out so it is not forgotten.
- **R5 (informational, unchanged from 6P):** B2 and DD-3 remain open per the repo's own status
  docs. This phase does not close them.
- **Boundary note (unchanged):** BYOK / managed-processing / mode selection are not implemented
  in this public repo and are therefore confirmed by boundary analysis, not by CI tests. CI does
  not — and must not — add such logic.

## 10. Final recommendation

**PASS — ready for commit on `phase-6q-sdk-ci-validation-gates`.**

The change is additive and minimal: one workflow, one validation script, one report. It
enforces exactly the checks Phase 6P proved manually, fails on real defects (verified by a
negative test), runs only repository-supported commands, and adds no private-Core logic, no
provider runtime dependency, and no secrets. `main` is untouched and the public/private
boundary is unchanged. Merge via PR (do not push to `main` directly); the workflow will execute
on the PR itself.
