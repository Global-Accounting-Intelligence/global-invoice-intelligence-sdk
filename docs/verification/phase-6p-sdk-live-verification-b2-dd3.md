# Phase 6P — SDK Live Verification (B2 / DD-3)

**Status:** Verification record. Advisory. Closes no blocker and no Deferred Decision.
**Date:** 2026-06-22.
**Verifier scope:** Strict live verification pass after the B2/DD-3 acceptance-review
package was merged into `main`. This is **not** a redesign or a new architecture phase.

---

## 1. Branch name

`phase-6p-sdk-live-verification-b2-dd3`

(`main` was not modified. All work is confined to this branch's working tree.)

## 2. Repository name

`global-invoice-intelligence-sdk` (public SDK repository).

## 3. Scope

Verify that the public SDK repository is internally consistent, safe to expose publicly,
and aligned with the approved Global Accounting Intelligence governance, canonical
schema, BYOK, managed-processing, and Trust Engine boundaries. Concretely:

- repository inventory (source, examples, tests, docs, schemas/contracts, CI/config);
- consistency of docs, examples, exported APIs, schemas, and tests against the approved
  principles (canonical-standard ownership, managed-processing primary, BYOK no-silent-
  fallback, future local/enterprise mode, simple customer modes, explainable Trust Engine,
  "not an ERP/OCR/accounting system", public-only surface);
- live execution of the checks the repository actually supports;
- fixing only real, evidenced issues with no scope expansion;
- recording the result with traceable evidence.

Out of scope (per task hard rules): product-strategy rewrites, moving architecture
decisions, new commercial modes, new dependencies, private-core logic, secrets/credentials,
deletion of approved documentation.

## 4. Files inspected

Governance / boundary:
- `CLAUDE.md`, `AGENTS.md`, `.github/pull_request_template.md`
- `docs/architecture/sdk-documentation-map.md`, `docs/architecture/sdk-module-map.md`
- `README.md`, `PUBLIC_REPO_SAFETY_CHECK.md`, `.env.example`, `.gitignore`

Contracts / schemas:
- `openapi/openapi.yaml` (active), `openapi/openapi_v0_4.yaml` (reference-only)
- all 16 active `schemas/*.schema.json`
- `schemas/v0_4/*` (confirmed retired / reference-only; not validated as active)

SDK clients / tests:
- `sdk/python/` (`pyproject.toml`, `global_invoice_intelligence/{__init__,client,errors,models,webhooks}.py`, `tests/test_client.py`)
- `sdk/javascript/` (`package.json`, `src/{index,client,errors,webhooks}.js`, `tests/client.test.js`)

Examples / tools / connectors:
- `examples/invoices/*`, `examples/match_results/*`, `examples/materials/*`, `examples/feedback/*`
- `tools/validate_invoice_schema.py`, `tools/validate_material_schema.py`, `tools/sample_webhook_receiver.py`
- `connectors/erpnext/*` (config, README, `src/*.py`), `connectors/odoo-starter/*`, `connectors/generic-rest/*`

Developer docs:
- `docs/API_OVERVIEW.md`, `docs/AUTHENTICATION.md`, `docs/DATA_PRIVACY_FOR_DEVELOPERS.md`,
  `docs/GETTING_STARTED.md`, `docs/SDK_Contract_Gap_Report_v1.md`,
  `docs/SDK_A1_OpenAPI_Alignment_Decision_Record_v1.md`

## 5. Commands run

All commands executed in a Linux sandbox against the repository working tree, using the
package managers and runners the repo actually declares (no invented commands).

| # | Command | Purpose |
|---|---------|---------|
| 1 | `git rev-parse --abbrev-ref HEAD` / `git status --porcelain` / `git log --oneline` | branch + state baseline |
| 2 | `git diff --ignore-all-space` + `file` + CRLF count | classify pre-existing working-tree changes |
| 3 | `node --version`; `python3 --version`; import checks for `pytest`, `jsonschema`, `pyyaml`, `httpx` | tooling availability |
| 4 | `node tests/client.test.js` (= `npm test`) | JavaScript SDK test |
| 5 | `pip install pytest httpx --break-system-packages` | install declared/dev test deps in sandbox |
| 6 | `python3 -m pytest -q` (in `sdk/python/`) | Python SDK test |
| 7 | `python3 tools/validate_invoice_schema.py` / `validate_material_schema.py` | repo validation tools |
| 8 | `python3 -c "import yaml; yaml.safe_load(...)"` on both OpenAPI files | OpenAPI YAML well-formedness |
| 9 | Python `jsonschema` script: parse all 44 JSON files; meta-validate 16 active schemas; validate examples against mapped schemas | schema/example consistency |
| 10 | `grep` scans for BYOK/managed/mode, secrets, private-internal leakage, ERPNext auto-post, v0_4 retirement | boundary checks |

No CI runner was executed because **no CI workflow exists** (see §7, finding F3).

## 6. Results of each command

- **Branch/state:** On `phase-6p-sdk-live-verification-b2-dd3`. Two files showed as modified
  at start: `docs/SDK_A1_OpenAPI_Alignment_Decision_Record_v1.md` and
  `docs/SDK_Contract_Gap_Report_v1.md`.
- **Pre-existing change classification:** `git diff --ignore-all-space` returned empty and
  `file` reported CRLF terminators on the working copies vs. 0 CRLF in `HEAD`. The changes
  were **pure CRLF line-ending churn with zero content change** — not part of this
  verification. Normalized back to LF; both files are now byte-identical to `HEAD`.
- **Tooling:** Node `v22.22.3`; Python `3.10.12`; `jsonschema 3.2.0` and `pyyaml` present;
  `pytest` and `httpx` absent → installed into the sandbox to run the declared tests.
- **JavaScript SDK test:** PASS (prints `true`, exit 0).
- **Python SDK test:** PASS (`1 passed`).
- **Validation tools:** both PASS ("Invoice example basic validation passed.",
  "Material example basic validation passed.").
- **OpenAPI YAML:** both `openapi.yaml` and `openapi_v0_4.yaml` parse cleanly.
- **JSON/schema scan:** 44 JSON files parse with 0 errors; all 16 active schemas pass
  Draft meta-validation. Before fixes, example→schema validation surfaced the issues in §7.
  After fixes: **all mapped examples validate OK** and **no active schema is missing
  `$schema`**.
- **Boundary scans:** `.env.example` contains placeholders only; `PUBLIC_REPO_SAFETY_CHECK.md`
  reports 0 secrets; no real secret patterns matched; no positive leakage of private
  internals (trust/matching weights, scoring formulas, cross-tenant, raw prompts, hidden
  reasoning); ERPNext connector is a stub returning `not_implemented` (no auto-post /
  `docstatus=1` / submit); `schemas/v0_4/*` and `openapi_v0_4.yaml` consistently marked
  retired / reference-only.

## 7. Issues found

**F1 — Stale match-result examples vs. hardened schema (real defect).**
`schemas/match_result.schema.json` was hardened (commits `974739a` A5 evidence, `bca037a`
A6 improvement_suggestions): `evidence` must be an **array** of structured provenance
entries, and `improvement_suggestions[]` items require
`{kind, target_field, status, review_only, confidence, evidence}` with
`additionalProperties:false`. The three examples did not conform:
- `examples/match_results/{green,yellow,red}_match.json` had `"evidence": {}` (object, not array).
- `examples/match_results/yellow_match.json` had `improvement_suggestions[0] = {"type","value"}`
  (old shape; missing all required fields).
The OpenAPI component `MatchResult` is bound to `../schemas/match_result.schema.json`
(`openapi/openapi.yaml` line 351–352), confirming the schema is the authoritative contract,
so the **examples** are the side that must conform (per `AGENTS.md`: never rewrite contracts
to fit code/examples).

**F2 — One active schema missing `$schema` (real, minor inconsistency).**
`schemas/invoice_line.schema.json` was the only active schema with no `$schema` keyword; the
other 15 all declare `https://json-schema.org/draft/2020-12/schema`. It is a standalone
component (not `$ref`'d by other schemas; `invoice.schema.json` uses its own inline
`$defs/invoice_line`), so this is a self-consistency gap only.

**F3 — No CI workflow present (gap / risk, not a regression).**
`.github/` contains only `pull_request_template.md`; there is **no `.github/workflows/`
directory**. The schema validation, example validation, and SDK tests that exist are not run
automatically on PRs. This is why the "CI command mismatch" allowed-fix category is not
applicable — there is no CI to mismatch.

**F4 — Pre-existing CRLF churn in two docs files (housekeeping).** See §6; normalized.

**Observations (no change made — not defects):**
- O1: `examples/invoices/invoice_with_qr_payload.json` (`{"qr_payload":"FAKE_DEMO_QR_PAYLOAD"}`)
  is a fake **raw input** for `POST /v1/invoices/normalize`, intentionally a different shape
  from a normalized invoice; no contract binds it to `invoice.schema.json`. Correct as-is,
  but it is the one example folder member with no schema binding (see Remaining risks R3).
- O2: SDK client parity gap — the Python client exposes `match_invoice` **and**
  `send_feedback`; the JavaScript client exposes only `matchInvoice`. Both are
  hand-maintained starters; not a contract violation. Logged as a risk, not fixed (fixing
  would expand surface beyond verification scope).

## 8. Fixes made

1. `examples/match_results/green_match.json` — `evidence` rewritten as a one-entry array
   (`method:"deterministic"`, `source_fields:["supplier_item_code"]`, `confidence:98`,
   public-safe `summary`); `improvement_suggestions` left `[]`.
2. `examples/match_results/yellow_match.json` — `evidence` as array
   (`method:"ai_assisted"`, `confidence:78`); `improvement_suggestions[0]` rewritten to the
   hardened shape (`kind:"add_alias"`, `target_field`, `proposed_value`, `status:"proposed"`,
   `review_only:true`, `confidence:78`, `evidence:[...]`, `summary`).
3. `examples/match_results/red_match.json` — `evidence` as array (`method:"ai_assisted"`,
   `confidence:40`); `improvement_suggestions` left `[]`.
4. `schemas/invoice_line.schema.json` — added
   `"$schema": "https://json-schema.org/draft/2020-12/schema"` (additive only; no
   constraint/behavior change).
5. `docs/SDK_A1_OpenAPI_Alignment_Decision_Record_v1.md`,
   `docs/SDK_Contract_Gap_Report_v1.md` — line endings normalized back to LF to remove
   pre-existing CRLF churn; now byte-identical to `HEAD` (no content change).

All edits preserved LF line endings. All example content is fake and public-safe (provenance
/ support text only): no matching/trust weights, scoring formulas, ranking, learning
internals, raw prompts, or hidden reasoning. Post-fix, every mapped example validates and
all SDK tests / validation tools pass.

## 9. Remaining risks

- **R1 (medium):** No CI (F3). The existing checks (JSON parse, schema meta-validation,
  example↔schema validation, both SDK tests, both validation tools) are not enforced on PRs,
  so future drift of the kind found in F1 can re-enter `main` undetected. Recommend a
  minimal CI workflow running exactly the §5 commands. *Future scope — not added here
  (would exceed verification scope and the "no new config beyond fixes" intent).*
- **R2 (low):** SDK client parity (O2) — JS client lacks `send_feedback` / any
  material-score call present on the Python side. Track as a developer-ergonomics backlog
  item; intentionally not changed.
- **R3 (low):** `invoice_with_qr_payload.json` (O1) has no schema binding or validation tool
  coverage. Consider a raw-input schema or a short note when `/normalize` input contracts
  are formalized. *Post-MVP — depends on normalize input-contract work, not owned here.*
- **R4 (process):** `.git/index.lock` was held by another process during the session, so
  `git add/commit/checkout` could not run from the sandbox. Staging/committing must be done
  by the user in their environment (see §“readiness” in the chat summary).
- **R5 (informational):** B2 (Core/SDK contract alignment) and DD-3 (public JSON-Schema
  hardening) remain **open** per the repo's own status notes
  (`docs/architecture/sdk-module-map.md` §Status, `sdk-documentation-map.md` §Status). This
  verification does not close either, consistent with those documents.

## 10. Public/private boundary confirmation

**Confirmed — boundary holds.** No private-core leakage was found in any scanned file:
no trust/matching weights, scoring/ranking formulas, learning internals, tenant
knowledge-graph internals, cross-tenant data, raw prompts, hidden reasoning, or raw provider
responses. Schema descriptions repeatedly and explicitly prohibit encoding such internals
(e.g. `match_result.schema.json` `evidence`/`improvement_suggestions` descriptions). The
example content added in §8 is provenance/support text only. `.env.example` and connector
config examples contain placeholders only; `PUBLIC_REPO_SAFETY_CHECK.md` reports 0 secrets.
The SDK presents itself as public I/O contracts, clients, examples, validation, and connector
starters — not as an ERP, OCR tool, accounting system, or the private Core. ERPNext push is
documented draft-only ("Create draft Purchase Invoice after user approval") and the connector
source performs no auto-post (`not_implemented` stub). PO/UOM/tax remain optional in
`invoice_line.schema.json` (nullable, not required). `schemas/v0_4/*` and `openapi_v0_4.yaml`
remain retired / reference-only.

## 11. BYOK fallback confirmation

**Confirmed — no silent-fallback path exists in this repository.** The public SDK does
**not** implement, reference, or expose BYOK, managed-processing selection, processing-mode
choice (Auto-Economy / Auto-Balanced / Auto-Highest Accuracy / Premium Critical), or any
provider-key orchestration: a full-repo scan for `byok|managed[- ]process|silent|fall[- ]?back`
matched only governance prose forbidding *silent contract rewrites* — never a runtime
fallback. Authentication is a single tenant-scoped API-key model
(`Authorization: Bearer` + `X-Tenant-ID`). Because mode selection and provider-key handling
live in the private Core / planning repo, the "BYOK must report failure and never silently
fall back to GAI-managed processing" guarantee is **not testable in this repo** and must be
enforced where that logic resides. No violation is present here; the principle is recorded as
a boundary note rather than a passing test.

## 12. Canonical schema / documentation consistency confirmation

**Confirmed consistent.** GAI's canonical standards are expressed through the public
OpenAPI, JSON Schemas, and docs in this repo. `openapi/openapi.yaml` is the single active
spec (v0.1.0, `/v1` frozen with documented `/v2`-for-breaking-change policy) and binds its
`MatchResult` component to the active `match_result.schema.json`. All 16 active schemas are
valid and (after F2) uniformly declare draft 2020-12. After the F1 fixes, all mapped examples
validate against the active schemas; the repo's own validation tools and SDK tests pass.
Retired artifacts (`schemas/v0_4/*`, `openapi_v0_4.yaml`, `v0_4_*` examples/guides) are
consistently labeled reference-only across `AGENTS.md`, `CLAUDE.md`, and both architecture
maps. The Trust-Engine-facing surface stays explainable, not black-box: `API_OVERVIEW.md`
requires every match to carry confidence, status color, explanation, evidence, and
improvement suggestions, and the schema models structured `evidence[]` and review-only
`improvement_suggestions[]` (with `review_only: const true`, AC-R1) — explanation/support
data only.

## 13. Final recommendation

**PASS WITH NOTES.**

All runnable repository checks are green after fixes: JavaScript SDK test, Python SDK test,
both validation tools, both OpenAPI files parse, all 44 JSON files parse, all 16 active
schemas meta-validate, and every mapped example validates against its active schema. Two real
issues found during verification (F1 stale match-result examples, F2 missing `$schema`) were
fixed within scope; pre-existing CRLF churn (F4) was normalized. The notes are: no CI exists
to enforce these checks (R1/F3), BYOK/managed-processing/mode principles are not implemented
in this public repo and therefore are confirmed by boundary analysis rather than tests
(§11), minor SDK client parity and one unbound raw-input example (R2/R3), and B2/DD-3 remain
open per the repository's own status documents (R5). Not a clean PASS because of those open
items and the absence of automated enforcement, but no boundary violation, no leakage, and no
failing check remain.
