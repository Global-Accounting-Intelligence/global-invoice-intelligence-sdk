# Phase 7C — SDK Public Contract Drift Verification (match-result field names)

**Status:** Verification record. Advisory. Confirms the public match-result contract
matches the Planning Phase 7B / ADR-0016 canonical field names. Not a redesign, not a
new architecture phase.
**Date:** 2026-06-23.

---

## 1. Branch name

`phase-7c-sdk-public-contract-drift-verification`

(`main` was not modified. No Core repository or planning/governance repository changes.
All work is confined to this branch's working tree, and this run added documentation only —
no schema, example, test, or tool changes were required.)

## 2. Scope

Verify (and correct only if necessary) public SDK contract drift for **match-result field
names** following Planning Phase 7B / ADR-0016.

Canonical public/customer-facing match-result fields:

- `confidence_score`
- `status_color`
- `explanation`

Short forms that are **not** canonical public contract fields unless explicitly introduced
later through Change Control and versioning:

- `confidence` (as the top-level match-result field)
- `color`
- `reason`

In scope: the active public contract surface — `schemas/match_result.schema.json`,
`examples/match_results/*`, the OpenAPI `MatchResult` binding, the Python/JavaScript SDK
sources and tests, the validation tools, and current (non-`v0_4`) developer docs.

Explicitly **out of scope** (per task hard rules): modifying Core or planning/governance
repos; changing runtime matching logic; OCR; LLM calls; BYOK; provider routing; ERPNext
push; secrets/credentials/`.env`/API keys/provider config; breaking public schema changes
beyond correcting drift back to the already-approved canonical names; pricing, extraction
strategy, customer modes, or product scope. This record does **not** declare B2, DD-3, DD-5,
or any deferred decision closed.

## 3. Files inspected

| File / area | Why inspected | Finding |
|---|---|---|
| `schemas/match_result.schema.json` | Canonical active match-result schema | Uses `confidence_score`, `status_color`, `explanation`. **Canonical — no drift.** |
| `examples/match_results/{green,yellow,red}_match.json` | Active examples validated by CI | All three use `confidence_score`, `status_color`, `explanation`. **No drift.** |
| `openapi/openapi.yaml` (`MatchResult`) | Public OpenAPI binding | `MatchResult` `$ref`s `schemas/match_result.schema.json`; no inline short-form fields. **No drift.** |
| `sdk/python/global_invoice_intelligence/models.py`, `client.py`, `tests/test_client.py` | Python SDK surface | No match-result field references; `models.py` is a placeholder. **No drift.** |
| `sdk/javascript/src/*.js`, `tests/client.test.js` | JavaScript SDK surface | No match-result short-form field references. **No drift.** |
| `tools/validate_sdk_contracts.py` | Contract validation tool | Maps the three `match_results` examples to `schemas/match_result.schema.json`; treats `schemas/v0_4/*` and `examples/v0_4_api_examples/*` as retired/reference-only (parsed only). **No drift.** |
| `docs/API_OVERVIEW.md` | Current developer doc | "Response Philosophy" prose bullet list (`confidence`, `status color`, `explanation`, …) — conceptual prose, not JSON field definitions. **Harmless prose; not changed.** |
| `schemas/correction.schema.json`, `schemas/feedback.schema.json`, `examples/feedback/*` | Adjacent entities containing `reason` | `reason` here is a **correction/feedback** field, a different entity — not a match-result property. **Not drift; not changed.** |
| `schemas/v0_4/*`, `examples/v0_4_api_examples/*`, `docs/v0_4_reference/*`, `openapi/openapi_v0_4.yaml` | Retired v0.4 reference surface | Contain historical `confidence`/`color`/`reason`. **Intentionally frozen retired reference; not changed** (see §6). |

## 4. Drift found?

**No drift in the active public contract surface.**

The canonical match-result fields `confidence_score`, `status_color`, and `explanation` are
already used consistently across the active schema, the three active examples, the OpenAPI
`MatchResult` binding, and both SDKs. No active schema, example, generated type, or test uses
`confidence` (as the top-level field), `color`, or `reason` as a match-result JSON property.

### Distinguishing legitimate matches from drift

The repo-wide search for `confidence`, `color`, and `reason` returned hits that are **not**
match-result drift:

- **Nested per-entry `confidence`** in `match_result.schema.json` and the active examples —
  `evidence[].confidence` and `improvement_suggestions[].confidence` — are intentional,
  documented per-entry fields on the 0–100 integer scale (ADR-0008 / DC-4), deliberately
  distinct from the top-level `confidence_score`. These are canonical, not short-form drift.
- **`correction.reason` / `feedback.reason`** are fields on the correction/feedback entities,
  not on the match result.
- **`schemas/v0_4/*` and `*_v0_4*` reference material** is the retired v0.4 surface (see §6).

## 5. Exact corrections

None. No schema, example, test, tool, or current-doc file was modified. The only file added
is this verification report.

## 6. What was intentionally not changed

- **Retired v0.4 reference surface** — `schemas/v0_4/material_match_result.schema.json`
  (`confidence`/`color`/`reason`), `examples/v0_4_api_examples/match_materials_response.json`,
  `docs/v0_4_reference/API_Spec_v0_4.md`, and related v0.4 files. Per `CLAUDE.md`,
  `schemas/v0_4/*` stays retired / reference-only; `validate_sdk_contracts.py` parses but does
  not meta-validate them. Rewriting frozen historical reference to the current canonical names
  would misrepresent history and is out of scope for a drift-correction task.
- **`correction.reason` / `feedback.reason`** — legitimate fields on different entities; not
  match-result properties.
- **`docs/API_OVERVIEW.md` "Response Philosophy" prose** — a conceptual bullet list, not a
  contract/JSON field definition. It does not create contract ambiguity (no backticks, no
  JSON), so per the "do not change harmless prose" rule it was left as-is.
- **Nested per-entry `confidence`** in the active match-result schema/examples — canonical
  documented fields (ADR-0008), not short-form drift.

## 7. Test commands and results

Run from repo root (mirrors `.github/workflows/sdk-validation.yml`):

| Command | Result |
|---|---|
| `python tools/validate_invoice_schema.py` | PASS — "Invoice example basic validation passed." |
| `python tools/validate_material_schema.py` | PASS — "Material example basic validation passed." |
| `python tools/validate_sdk_contracts.py` | PASS — 39/39 JSON parsed; 16/16 active schemas meta-validated; 11/11 mapped example sets validated; `v0_4/*` skipped as retired/reference-only. |
| `cd sdk/python && python -m pytest -q` | PASS — 1 passed. |
| `cd sdk/javascript && npm test` | NOT RUN LOCALLY — `npm` is not installed or not available in PATH on this workstation. To be verified by GitHub Actions SDK validation. |

(`validate_sdk_contracts.py` emits a non-fatal `DeprecationWarning` about the `$schema`
metaschema lookup; this is pre-existing, unrelated to match-result fields, and does not affect
the PASS result.)

## 8. Final recommendation

No code change is required. The SDK public match-result contract already conforms to the
Planning Phase 7B / ADR-0016 canonical field names (`confidence_score`, `status_color`,
`explanation`). Acceptance criteria are met: the active schema/examples/tests use the canonical
fields, no active surface uses the short forms as match-result properties, existing SDK
validation passes, and no Core/planning-repo or scope (provider/OCR/LLM/BYOK/ERP) changes were
introduced. Merge this verification record as the audit trail; close Phase 7C as **verified, no
drift**. This record does not close B2, DD-3, DD-5, or any deferred decision.
