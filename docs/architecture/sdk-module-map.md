# SDK Module Map (SDK-local pointer)

This is an **SDK-local pointer** document. It describes the current SDK responsibility areas
by folder. It does not own the binding governance policy (planning repo
`global-accounting-intelligence`, `governance/documentation-as-code-and-architecture-drift-control.md`),
and it does not invent implementation that is not present in this repo. Where a folder is
absent, it is marked `Pending / not present in this repo`.

This repository is **public**: it exposes public I/O contracts, developer ergonomics,
examples, validation tools, and connector starters only.

## Responsibility areas

### `openapi/`
Present. Active public API specification `openapi/openapi.yaml`. The legacy
`openapi/openapi_v0_4.yaml` is reference-only and is not the active contract. Public API I/O
contract surface; do not edit unless explicitly authorized.

### `schemas/`
Present. Active public JSON Schemas (`schemas/*.schema.json`) — the active I/O contracts.
Do not edit unless explicitly authorized.

### `schemas/v0_4/`
Present. **Retired / reference-only.** Must not be used as the active contract.

### Examples
Present (`examples/`). Fake-data sample payloads: `invoices/`, `match_results/`,
`materials/`, `feedback/`, and legacy `v0_4_api_examples/`. Must validate against the active
schemas and contain no real customer data or private internals.

### Connectors
Present (`connectors/`). Connector starters: `erpnext/`, `odoo-starter/`, `generic-rest/`,
and legacy `v0_4_guides/`. ERPNext push must remain **draft-only** (never auto-post); PO,
UOM, and tax remain optional signals.

### Validation tools
Present (`tools/`). Public schema validation utilities and a sample webhook receiver
(`validate_invoice_schema.py`, `validate_material_schema.py`, `sample_webhook_receiver.py`).
Must validate against the active schemas only.

### Generated clients
**Pending / not present in this repo as generated artifacts.** The repo ships
hand-maintained SDK clients under `sdk/python/` and `sdk/javascript/` (each with its own
`README`, package manifest, sources, and tests). No code-generation pipeline is present; if
one is added later it must respect the public/private boundary.

## Status notes

- Implementation progress exists across the A1–A9 sequence, but formal acceptance/closure
  remains pending through the governance path unless an explicit acceptance record exists.
- **B2** (Core/SDK contract alignment) remains open / incomplete.
- **DD-3** (public JSON-Schema hardening) remains open.
