# SDK A1 OpenAPI Alignment Decision Record v1

**Status:** Documentation-only. Advisory decision record. **Closes nothing. Generates nothing.**
**Date:** 2026-06-21 (Phase 6B, branch `phase-6b-sdk-a1-openapi-alignment-decision`).
**Repository:** `global-invoice-intelligence-sdk` (SDK repo).
**Reference repository:** `global-accounting-intelligence` (planning repo) — used **read-only**; no planning document is copied into this repo.
**Nature:** Records that Phase 6A (the read-only contract inventory and gap baseline) is complete, and that the **next executable** SDK change may address **A1 — OpenAPI alignment only**, scoped strictly to the OpenAPI envelope conventions. This record creates no code, executable JSON Schema, OpenAPI file, DDL, migration, or test; it modifies no governance authority; it changes no ADR status; and it closes no Deferred Decision or blocker. It does **not** itself modify `openapi/openapi.yaml`.

**Authority chain (unchanged):** `SOURCE_OF_TRUTH_v0_6.md` → `architecture/Architecture_Freeze_v1.md` → ADRs → `architecture/Acceptance_Criteria_v1.md` → `MVP_Scope_and_Non_Goals.md` / `PRD.md` → `architecture/phase1/Knowledge_Model_Freeze_v1.md` → `governance/`. On conflict, the authority document wins.

---

## 1. Status and Scope

Phase 6A produced the read-only contract inventory and gap baseline (`docs/SDK_Contract_Gap_Report_v1.md`), the Step-1 baseline called for in `Phase5_Final_Implementation_Handoff_v1.md` §5/§12. That baseline is **complete**: it inventoried the SDK's current contract surface and recorded the gaps against the frozen planning references for blocker **B2** (Core/SDK contract alignment) and deferred decision **DD-3** (public JSON-Schema hardening), without editing any executable artifact.

This record authorizes that the **next executable pull request** may implement **A1 — OpenAPI alignment only**, the first item in the recommended A1–A9 sequence (`SDK_Contract_Gap_Report_v1.md` §12; `SDK_Core_Implementation_Work_Orders_v1.md` §4). A1 is limited to the OpenAPI **envelope conventions** measured in `SDK_Contract_Gap_Report_v1.md` §4 against `API_Contract_Design_v1.md` §1. It targets the convention-level gaps only; it does **not** extend to endpoints (A2), component binding (A3), error/auth/idempotency wiring beyond envelope declaration (A4), DD-3 hardening (A5–A8), or the missing public I/O schemas (A9).

This decision record is itself documentation-only. It is a **scoping decision, not a change**. It does not edit the OpenAPI file, the JSON Schemas, or any code. The executable A1 work is a separate, later pull request (Phase 6C; see §6).

## 2. References

Read read-only to ground this record. No planning document is copied into this repo.

| # | Path | Repo |
|---|---|---|
| 1 | `docs/SDK_Contract_Gap_Report_v1.md` | SDK repo (this repo) |
| 2 | `docs/DD3_B2_SDK_Contract_Decision_Package_v1.md` | planning repo |
| 3 | `docs/SDK_Core_Implementation_Work_Orders_v1.md` | planning repo |
| 4 | `docs/Phase5_Final_Implementation_Handoff_v1.md` | planning repo |
| 5 | `architecture/API_Contract_Design_v1.md` | planning repo |
| 6 | `architecture/Acceptance_Criteria_v1.md` | planning repo |

## 3. A1 Authorized Scope

A1, and only A1, is authorized for the next executable change. The authorized surface is the OpenAPI **envelope conventions** from `API_Contract_Design_v1.md` §1, matching the gap rows in `SDK_Contract_Gap_Report_v1.md` §4:

| # | A1 envelope item | Reference |
|---|---|---|
| 1 | **OpenAPI base conventions** — base path `/v1` for business endpoints; envelope structure consistent with `API_Contract_Design_v1.md` §1 | API §1 |
| 2 | **`application/json` media type** declared on request/response bodies | API §1 |
| 3 | **API-key security scheme** — `securitySchemes` declared (Bearer or `X-API-Key`), applied to all endpoints except `/health` | API §1; AC-A3 |
| 4 | **`X-Tenant-ID`** required header on tenant-scoped endpoints (formalized as a declared header parameter) | API §1; AC-T1 |
| 5 | **`Idempotency-Key`** header declared on mutating endpoints | API §1; AC-A4 |
| 6 | **`X-Request-ID`** correlation header declared | API §1 |
| 7 | **Rate-limit headers** — `X-RateLimit-*` family and the `429` response declared | API §1; AC-A4 |
| 8 | **`/v1` versioning and deprecation rule** documented (`/v1` frozen; breaking → `/v2`) | API §1 |

A1 is the envelope only. It declares conventions and headers at the OpenAPI level; it targets AC-A1…AC-A4 at the envelope layer, but does not by itself complete those acceptance criteria (component binding, the error catalogue, and the missing endpoints are A2–A4, excluded here).

## 4. Explicit Exclusions from A1

The following are **out of scope** for the A1 change and must not appear in the next executable pull request. Each remains tracked for its own later, separately gated step:

- **Do not add the three missing endpoints yet** — `GET /v1/invoices/{id}/result`, `GET /v1/materials/{id}/score`, `POST /v1/connectors/erpnext/push` are **A2**, not A1 (`SDK_Contract_Gap_Report_v1.md` §5/§12).
- **Do not add or modify JSON Schemas** — no edit to any file under `schemas/`, including no schema-content reconciliation against the Field Dictionary.
- **Do not add the six missing public I/O schemas** — `tenant`, `purchase_order`, `po_line`, `tax_category`, `uom`, `audit_event` are **A9** (`SDK_Contract_Gap_Report_v1.md` §7/§12).
- **Do not implement DD-3 hardening** — no `evidence`, `improvement_suggestions`, or webhook `payload` discriminator/typing work; that is **A5–A8** and is gated on DC-1…DC-4 (`SDK_Contract_Gap_Report_v1.md` §8).
- **Do not edit SDK clients** — no change to `sdk/python/*` or `sdk/javascript/*`.
- **Do not edit connectors** — no change to `connectors/erpnext/*`, `connectors/odoo-starter/*`, or `connectors/generic-rest/*`.
- **Do not add tests** — no new or modified test, and no change to `tools/validate_*`.
- **Do not close DD-3** — closure is the `DD3_B2_SDK_Contract_Decision_Package_v1.md` §8 path through Change Control only.
- **Do not declare B2 complete** — B2 is complete only when the implemented OpenAPI satisfies `API_Contract_Design_v1.md` and AC-A1…AC-A4; the A1 envelope alone does not satisfy them.

## 5. Guardrails

These guardrails bind the A1 change and this record. They restate the standing boundary rules (`Open_Source_Policies.md` §5; `Core_vs_SDK_Boundary.md`; `Coding_Agent_Rules.md` §3; `SDK_Contract_Gap_Report_v1.md` §10), and none is relaxed here:

- **No private Core model exposure** — the OpenAPI envelope must stay an I/O contract surface only; it must not surface or absorb the internal Knowledge Graph or canonical runtime model.
- **No matching / trust / learning / scoring logic** — no algorithm, weight tier, trust-weight, or scoring formula may be encoded in any convention, header, security scheme, or example introduced by A1.
- **No MVP expansion** — A1 implements existing frozen conventions only; nothing in this record adds scope beyond what the references already classify as MVP.
- **No governance changes** — no `governance/*` file in either repo is modified.
- **No ADR status changes** — ADR statuses are reported as the references state them; none is modified.

## 6. Expected Next Executable PR After This Record

The next executable pull request after this record is **Phase 6C — implement A1 OpenAPI envelope only**. That pull request, and only that pull request, may edit `openapi/openapi.yaml` to introduce the §3 envelope conventions, within the §4 exclusions and §5 guardrails. It is a separate change on its own branch; this record does not perform it and does not authorize any step beyond A1.

Subsequent steps (A2 endpoints, A3 component binding, A4 error/auth/idempotency/pagination, A5–A8 DD-3 hardening, A9 missing public I/O schemas) remain gated on their respective decision rows DC-1…DC-12 being recorded by the named owners before any executable edit (`SDK_Contract_Gap_Report_v1.md` §12), and are not authorized by this record.

## 7. Confirmation

- **DD-3 remains open.** This record frames only the A1 envelope scope; it does not close DD-3 (closure is the `DD3_B2_SDK_Contract_Decision_Package_v1.md` §8 path through Change Control).
- **B2 remains open / incomplete.** AC-A1…AC-A4 are not met by the A1 envelope alone; this record does not declare B2 complete.
- **The A1 decision record does not itself modify OpenAPI.** No change is made to `openapi/openapi.yaml` by this document; the envelope edit is the separate Phase 6C pull request.
- **No code / schema / OpenAPI generated by this document.** No executable artifact is created or edited; this is a documentation-only decision record.

---

*End of SDK A1 OpenAPI Alignment Decision Record v1. This document is a documentation-only scoping decision. It creates no code, executable schema, OpenAPI file, DDL, or migration; modifies no governance authority; changes no ADR status; closes no Deferred Decision; does not declare B2 complete; and expands no MVP scope. It authorizes only that the next executable change may address A1 — OpenAPI alignment — as scoped above.*
