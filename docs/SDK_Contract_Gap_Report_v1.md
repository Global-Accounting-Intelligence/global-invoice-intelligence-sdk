# SDK Contract Inventory & Gap Report v1

**Status:** Documentation-only. Advisory. **Closes nothing.**
**Date:** 2026-06-21 (Phase 6A, branch `phase-6a-sdk-contract-inventory-gap-report`).
**Repository:** `global-invoice-intelligence-sdk` (SDK repo).
**Reference repository:** `global-accounting-intelligence` (planning repo) — used **read-only**; no planning document was copied into this repo.
**Nature:** A read-only inventory of the current SDK contract artifacts compared against the authoritative planning references for blocker **B2** (Core/SDK contract alignment) and deferred decision **DD-3** (public JSON-Schema hardening). This is the Step 1 read-only gap baseline called for in `Phase5_Final_Implementation_Handoff_v1.md` §5/§12. It creates no code, executable JSON Schema, OpenAPI file, DDL, migration, or test; it modifies no governance authority; it changes no ADR status; and it closes no Deferred Decision or blocker.

**Authority chain (unchanged):** `SOURCE_OF_TRUTH_v0_6.md` → `architecture/Architecture_Freeze_v1.md` → ADRs → `architecture/Acceptance_Criteria_v1.md` → `MVP_Scope_and_Non_Goals.md` / `PRD.md` → `architecture/phase1/Knowledge_Model_Freeze_v1.md` → `governance/`. On conflict, the authority document wins.

---

## 1. Status and Scope

This document inventories the SDK's current contract surface — OpenAPI, JSON Schemas, examples, SDK clients, connectors, and validation tools — and reports the gaps between that surface and the frozen planning references. Its scope is **B2** and **DD-3** only, plus the six missing public I/O schemas tracked in `Canonical_Schema_Set_v1.md`.

It is a **comparison, not a change**. The executable schemas and the OpenAPI file are SDK-owned and are **not** edited here. DD-3 stays open and B2 stays incomplete; this report neither closes DD-3 nor declares B2 complete (that path is `DD3_B2_SDK_Contract_Decision_Package_v1.md` §8 through Change Control). The recommended A1–A9 sequence in §12 is gated on the decision rows DC-1…DC-12 being recorded by the named owners before any executable edit.

## 2. Reference Documents Read

All eleven planning references were read in full from the planning repo (read-only):

| # | Path |
|---|---|
| 1 | `architecture/API_Contract_Design_v1.md` |
| 2 | `docs/DD3_B2_SDK_Contract_Decision_Package_v1.md` |
| 3 | `docs/SDK_Core_Implementation_Work_Orders_v1.md` |
| 4 | `docs/Phase5_Final_Implementation_Handoff_v1.md` |
| 5 | `architecture/Canonical_Schema_Set_v1.md` |
| 6 | `architecture/Canonical_Schema_Field_Dictionary_v1.md` |
| 7 | `architecture/Acceptance_Criteria_v1.md` |
| 8 | `architecture/Core_vs_SDK_Boundary.md` |
| 9 | `architecture/Private_vs_Public_Repos.md` |
| 10 | `governance/Coding_Agent_Rules.md` |
| 11 | `governance/Open_Source_Policies.md` |

## 3. SDK Files Inspected

- **OpenAPI:** `openapi/openapi.yaml` (active, v0.1.0); `openapi/openapi_v0_4.yaml` (legacy, not the contract).
- **Schemas (active):** `schemas/{invoice, invoice_line, supplier, material, match_result, material_score, correction, feedback, error, webhook_event}.schema.json`. `schemas/v0_4/*` is retired / reference-only per `Canonical_Schema_Set_v1.md`.
- **Examples:** `examples/{invoices, match_results, materials, feedback}/*`.
- **SDK clients:** `sdk/python/global_invoice_intelligence/{client, models, errors, webhooks}.py`; `sdk/javascript/src/{client, errors, index, webhooks}.js`.
- **Connectors:** `connectors/{erpnext, odoo-starter, generic-rest}/src/*`.
- **Validation tools:** `tools/{validate_invoice_schema, validate_material_schema, sample_webhook_receiver}.py`.
- **Postman:** `postman/global_invoice_intelligence.postman_collection.json`.

## 4. Current OpenAPI Status

`openapi.yaml` is the skeleton described in `API_Contract_Design_v1.md` — v0.1.0, four paths: `GET /health`, `POST /v1/invoices/normalize`, `POST /v1/invoices/match`, `POST /v1/feedback/correction`. Measured against the §1 conventions:

| Convention (`API_Contract_Design_v1.md` §1) | Required | Observed | Status |
|---|---|---|---|
| Base path `/v1` | yes | business endpoints under `/v1` | OK |
| `application/json` media type | yes | no request/response bodies typed | Gap |
| API-key security scheme | `securitySchemes` (Bearer or `X-API-Key`); all but `/health` | none declared (SDK sends `Authorization: Bearer` + `X-Tenant-ID`, the spec declares nothing) | Gap |
| `X-Tenant-ID` required header | all tenant-scoped endpoints | present on the 3 business endpoints | OK |
| `Idempotency-Key` on mutating endpoints | yes | absent | Gap |
| Pagination `limit` / `cursor` / `next_cursor` | list endpoints | absent | Gap |
| Rate-limit headers `X-RateLimit-*` + `429` | yes | absent | Gap |
| `X-Request-ID` correlation | yes | absent | Gap |
| Versioning / deprecation rule | `/v1` frozen; breaking → `/v2` | not documented | Gap |

## 5. Required Endpoint Coverage

| Endpoint (`API_Contract_Design_v1.md` §2) | Status |
|---|---|
| `GET /v1/invoices/{id}/result` | **MISSING** |
| `GET /v1/materials/{id}/score` | **MISSING** |
| `POST /v1/connectors/erpnext/push` | **MISSING** from OpenAPI. `connectors/erpnext/src/erpnext_connector.py` has a `push_match_result()` stub, but no API path and no draft-only contract is declared |

All three required endpoints are absent, consistent with `DD3_B2_SDK_Contract_Decision_Package_v1.md` §3.2 and Work Order A2. Two further design endpoints are also absent (outside the required three but part of §2): `POST /v1/feedback` (generic feedback) and the optional `POST /v1/webhooks`.

## 6. Component Schema Binding Gaps

The active OpenAPI has **no `components` section** — zero `$ref`, every endpoint uses an undeclared / inline body. This fails `API_Contract_Design_v1.md` §3 ("`components/schemas` must reference every canonical schema; no inline anonymous body where a canonical schema exists"), DC-7, and AC-A1.

| Canonical schema | File exists | Bound in OpenAPI |
|---|---|---|
| invoice, invoice_line, supplier, material, match_result, material_score, correction, feedback, error, webhook_event | yes (all 10) | no (0 of 10) |

**Schema-content drift** vs the Field Dictionary (will surface during binding): `feedback.schema.json` carries `action ∈ {accepted, rejected, corrected}`, but the dictionary §10 / API §5 require an `event_type` enum with the nine-value learnable catalogue (`accepted_match … retention_treatment_updated`); `correction.schema.json` lacks the required `correction_type` enum (dictionary §9); `material_score.schema.json` exposes `score` + `missing[]` where the dictionary §8 requires `score` + `dimensions[]`; `match_result.evidence` is typed `object` where the dictionary §7 specifies an array of per-signal entries; and no schema carries the `method ∈ {deterministic, ai_assisted}` provenance flag (FD-11 / AC-R2).

## 7. Missing Public I/O Schemas

All six are absent, confirming `Canonical_Schema_Set_v1.md` "Schemas to Add" / DC-11 / Work Order A9:

| Schema | Status | Reference constraint |
|---|---|---|
| `tenant` | MISSING | `tenant_id` discipline FD-1 / AC-T1; not the internal tenant KG model |
| `purchase_order` | MISSING | shape for when a PO is present; optional signal, never required (FD-7 / AC-M4) |
| `po_line` | MISSING | aligns `invoice_line.po_line_id`; optional |
| `tax_category` | MISSING | tax is a review / matching signal only (FD-10) |
| `uom` | MISSING | matching never requires UOM (FD-10 / AC-M1) |
| `audit_event` | MISSING | mandated audit logging AC-T3; append-only, must outlive the data (FD-9) |

## 8. DD-3 Schema-Hardening Gaps

| Item | Reference target | Observed | Status |
|---|---|---|---|
| `match_result.evidence` | typed, public-safe: per-signal entries carrying `method`, source fields, confidence (FD-11 / AC-R2 / DC-1) | bare `{"type":"object"}`; example value `{}` | Gap (also wrong base type — object vs array per dictionary §7) |
| `improvement_suggestions` | typed item: kind enum, target field, evidence, confidence, proposed/confirmed, review-only (FD-3 / AC-R1 / DC-2) | array of untyped objects | Gap |
| `webhook_event.payload` discriminator | `event_type` discriminator + typed payload per event (API §6 / DC-3) | `event_type` free string, `payload` bare object, no `oneOf` / discriminator | Gap |
| `event_type` catalogue | enumerated: `match.completed`, `feedback.recorded`, `erp.draft.created`, `erp.push.failed` (API §6) | none | Gap |
| Public-safe validation rules | field-level types / required / enums / regex; I/O-contract scope only; no engine internals (DC-4 / DC-5) | no `additionalProperties:false`, minimal `required`, no enums beyond `status_color` | Gap (under-constrained) |
| `confidence_score` range | integer **0–100** (ADR-0008 / DC-4) | `type: number`, no `minimum` / `maximum` | Gap |
| `status_color` enum | `[green, yellow, red]` (ADR-0008) | exactly `[green, yellow, red]` | OK (thresholds green ≥ 90 / 70 ≤ yellow < 90 / red < 70 are server-side, correctly not in the schema) |

## 9. B2 Alignment Gaps (vs `API_Contract_Design_v1.md` + `Acceptance_Criteria_v1.md`)

| AC | Requirement | Status |
|---|---|---|
| AC-A1 | all endpoints documented with request/response schema bindings | FAIL — 3 endpoints missing; 0 component bindings |
| AC-A2 | error model (stable `code` / `message`); 400/401/403/404/409/422/429/500; enumerated error-code catalogue | FAIL — `error.schema` is `code` + `message`, both optional, no `details` / `request_id`; no statuses declared; no catalogue |
| AC-A3 | auth + tenant enforced via documented security scheme | FAIL — no `securitySchemes` / `security`; `X-Tenant-ID` is a header param only, not bound to auth |
| AC-A4 | idempotency, pagination, rate-limit behavior match the design | FAIL — none present |

Per `DD3_B2_SDK_Contract_Decision_Package_v1.md` §3, B2 is "complete only when the implemented OpenAPI satisfies `API_Contract_Design_v1.md` and AC-A1…AC-A4." None of AC-A1…AC-A4 is met, and decision rows DC-6…DC-10 are unrecorded. **B2 remains open / incomplete.** This report does not declare B2 complete, and DD-3 stays open.

## 10. Public / Private Boundary Risks

The loose `evidence` / `improvement_suggestions` / webhook `payload` objects are the DD-3 hardening surface, and that is exactly where boundary leakage can occur: hardening must expose **shape + provenance + confidence only** and must never encode trust-weight tiers, the matching/trust/learning algorithm, or the scoring formula (`Open_Source_Policies.md` §5; `AI_Policies.md` §4 as cited; `Core_vs_SDK_Boundary.md`; DC-5). Today's risk is the inverse-but-related one — the contract is under-specified, so a careless hardening could over-expose; the guardrail must be set before A5–A7.

Public schemas must stay **I/O contracts only**, never the internal Knowledge Graph / canonical runtime model — DD-1 is closed by ADR-0012 (Option A) with the boundary confirmed, not moved (`Open_Source_Policies.md` §6); the SDK must not absorb any Core model during binding. Connectors must remain mapping / adapter only with no intelligence logic (`Open_Source_Policies.md` §5 rule 4); the `erpnext` `push_match_result` stub must stay an adapter and the push must create an **ERP draft only** (ADR-0007 / AC-E3). `schemas/v0_4/*` physically present in the SDK repo must never be cited as the active v1 contract and must not be promoted without an explicit scoped decision (DC-12). Examples appear synthetic (e.g. `ITEM-000154`) and must stay fake — no real customer data or secrets in any repo (`Open_Source_Policies.md` §5 rule 3).

## 11. MVP vs Post-MVP vs Future-Scope Observations

Recorded only where the references explicitly support the classification.

- **MVP (in scope, SDK-owned):** the B2 OpenAPI alignment, the three missing endpoints, component binding, the DD-3 hardening, and the six missing public I/O schemas (Field Dictionary §14 classifies `tenant` / `purchase_order` / `po_line` / `tax_category` / `uom` / `audit_event` as MVP "SDK to author"). ERPNext is the only MVP connector exercised (AC-E1) and push is draft-only (AC-E3).
- **Post-MVP:** Odoo / local connectors (AC-E1). The SDK already ships `odoo-starter` and `generic-rest` starters; they may exist as examples but are not MVP-exercised.
- **Future:** SAP / Oracle connectors (AC-E1); country-pack locale tax logic and the supplier `country_code` hook (dictionary §5). Per `Acceptance_Criteria_v1.md` §10, auto-posting, payments, bank reconciliation, custom OCR, mobile, and a full global product registry are out of MVP scope entirely.
- **Scope guards (explicit in the references):** PO / `po_line`, `uom`, and `tax_category` stay optional signals — never required for matching (FD-7 / FD-10 / AC-M4); `POST /v1/webhooks` is optional. Nothing in this report expands MVP scope.

## 12. Recommended Implementation Sequence A1–A9

These are Work Order A (`SDK_Core_Implementation_Work_Orders_v1.md` §4), reproduced as the authoritative sequence — all in the **SDK repo**, each gated: the relevant decision row DC-1…DC-12 must be recorded by the named owners before any executable edit, and DD-3 closure / B2-complete only via the DD-3/B2 package §8 path through Change Control.

1. **A1 — OpenAPI alignment.** Base path `/v1`, `application/json`, API-key security scheme + `X-Tenant-ID`, `Idempotency-Key` replay, `limit` / `cursor` / `next_cursor` pagination, rate-limit headers, `X-Request-ID`, and the `/v1` versioning / deprecation rule. Target AC-A1…AC-A4.
2. **A2 — Missing endpoints.** Add `GET /v1/invoices/{id}/result`, `GET /v1/materials/{id}/score`, `POST /v1/connectors/erpnext/push` (ERP **draft only**, ADR-0007 / AC-E3).
3. **A3 — Component binding.** `components/schemas` references all ten canonical schemas; no inline anonymous body where a canonical schema exists (AC-A1).
4. **A4 — Error / auth / idempotency / pagination.** Wire `error.schema` with 400/401/403/404/409/422/429/500 + enumerated error-code catalogue (AC-A2); enforce API-key + `X-Tenant-ID` with tenant resolved before data access (AC-A3 / AC-T1); `Idempotency-Key` replay (AC-N5 / AC-E4); pagination + rate-limit headers (AC-A4).
5. **A5 — `evidence` hardening (DC-1, DC-5).** Typed, public-safe sub-schema: `method ∈ {deterministic, ai_assisted}`, source fields, confidence — evidence shape + provenance only, no weighting / scoring internals.
6. **A6 — `improvement_suggestions` hardening (DC-2).** Typed item: kind enum, target field, evidence, confidence, proposed/confirmed (FD-3), review-only (AC-R1) — never an auto-mutation instruction.
7. **A7 — Webhook discriminator (DC-3).** `event_type` discriminator + enumerated catalogue + typed payload per event (API §6).
8. **A8 — Field-level validation (DC-4).** Types / required / enums / regex; `confidence_score` 0–100; `status_color ∈ {green, yellow, red}` per ADR-0008 — I/O-contract scope only; encodes no algorithm / weights / formula.
9. **A9 — Missing public I/O schemas (DC-11).** Add `tenant`, `purchase_order`, `po_line`, `tax_category`, `uom`, `audit_event` as I/O contracts only; PO / UOM / tax stay optional signals; `audit_event` append-only (AC-T3 / FD-9); `schemas/v0_4/*` stays reference-only (DC-12).

Forbidden across A1–A9 (Work Order A + `Coding_Agent_Rules.md` §3): exposing the canonical model / engines / weight-tiers / scoring through any schema / OpenAPI / validation rule / example; promoting `v0_4/*` without a scoped decision; making the ERPNext push do anything but a draft; requiring PO / UOM / tax; emitting an edit for any unrecorded DC-row; or declaring DD-3 closed / B2 complete outside §8.

## 13. Risks and Assumptions

The gap analysis is anchored to the authoritative references, so the residual risk is execution-side, not interpretive. Sequencing A1–A9 is correctly gated on DC-1…DC-12 being recorded first; attempting edits before those decisions exist would violate Work Order A and `Coding_Agent_Rules.md` §3.6. The sharpest standing risk is the boundary one in §10 — the under-specified `evidence` / `payload` objects must be hardened to expose shape / provenance / confidence only. Operational drift risks: schema files exist but are unbound (OpenAPI ↔ schema divergence); `invoice.schema.json` embeds an `invoice_line` `$defs` copy duplicating the standalone file; the `tools/validate_*` scripts are two-key `assert` stubs (no real JSON-Schema validation in CI); and `feedback` / `correction` / `material_score` content diverges from the Field Dictionary and will need reconciliation during A3 / A8.

Assumptions: the active (non-`v0_4`) `schemas/` set is the canonical target (`Canonical_Schema_Set_v1.md` "Decision"); DD-1 is treated as closed and ADR-0015 as `Proposed` per the Phase 5 documents — the ADR source files were not independently opened to verify their status headers, so that status is taken from the references as written.

## 14. Changed-Files Summary

This report is the only file added (`docs/SDK_Contract_Gap_Report_v1.md`). No existing file in the SDK repo was modified, and no file in the planning repo was touched. No OpenAPI, JSON Schema, SDK client code, connector, validation tool, or test was edited or generated.

## 15. Explicit Confirmation

- **DD-3 remains open.** This report frames the hardening gaps; it does not close DD-3 (closure is the `DD3_B2_SDK_Contract_Decision_Package_v1.md` §8 path through Change Control).
- **B2 remains open / incomplete.** AC-A1…AC-A4 are not met; this report does not declare B2 complete.
- **No ADR status changed.** ADR statuses are reported as the references state them; none was modified.
- **No governance changed.** No `governance/*` file in either repo was modified.
- **No code / schema / OpenAPI generated.** No executable artifact was created or edited; this is a documentation-only report.
- **No private Core logic exposed.** No canonical runtime model, matching / trust / learning engine, weight tier, or scoring formula is described or surfaced.

---

*End of SDK Contract Inventory & Gap Report v1. This document is a read-only gap report. It creates no code, executable schema, OpenAPI file, DDL, or migration; modifies no governance authority; changes no ADR status; closes no Deferred Decision; does not declare B2 complete; and expands no MVP scope.*
