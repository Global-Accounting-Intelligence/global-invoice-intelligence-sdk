# SDK Documentation Map (SDK-local pointer)

This is an **SDK-local pointer** document. It maps what this public SDK repository owns,
what it does not own, and what to review when each area changes. It does **not** restate or
own the binding governance policy. The binding Documentation-as-Code & Architecture Drift
Control policy lives in the planning repository `global-accounting-intelligence` at
`governance/documentation-as-code-and-architecture-drift-control.md`. This repo does not
own that policy and must not duplicate it.

This repository is **public**. Public schemas and OpenAPI are API I/O contracts only — not
the internal Core model.

## What this SDK repo owns

- **OpenAPI** — `openapi/openapi.yaml` (the active public API specification).
- **Active public JSON Schemas** — `schemas/*.schema.json` (the active I/O contracts).
- **SDK clients** — `sdk/python/` and `sdk/javascript/` (public developer clients).
- **Examples** — `examples/` (fake-data sample invoices, match results, materials, feedback).
- **Connector starters** — `connectors/` (ERPNext, Odoo, generic-REST starters).
- **Validation tools** — `tools/` (public schema validation utilities).
- **Public developer docs** — `docs/` (getting started, auth, errors, webhooks, rate limits,
  connector guides, and these architecture maps).

## What this SDK repo does not own

These belong to the private Core / planning repositories and must never appear here:

- private Core runtime model
- matching engine
- Trust Engine internals (including trust weights and trust-tier internals beyond
  already-public contract references)
- learning engine
- scoring formulas
- tenant knowledge graph
- provider orchestration internals
- raw prompts, hidden reasoning, raw provider responses, cross-tenant learning

## What to review when each area changes

When changing an area below, assess the listed downstream surfaces and record the impact in
the PR (see `.github/pull_request_template.md`). Do not change schemas or OpenAPI unless the
task explicitly authorizes it; if code conflicts with the public contract, report the
conflict rather than silently rewriting the contract to fit code.

- **OpenAPI change** (`openapi/openapi.yaml`) → review affected JSON Schemas, examples,
  both SDK clients, validation tools, public docs, and tests; confirm the public/private
  boundary still holds.
- **Schema change** (`schemas/*.schema.json`) → review OpenAPI references, examples that
  validate against the schema, SDK client models, validation tools, and tests. Confirm
  `schemas/v0_4/*` is not used as the active contract.
- **Webhook change** → review `schemas/webhook_event.schema.json`, the OpenAPI webhook
  definitions, webhook examples, the sample webhook receiver in `tools/`, and `docs/WEBHOOKS.md`.
- **Error model change** → review `schemas/error.schema.json`, OpenAPI error responses,
  error examples, SDK client error handling, and `docs/ERROR_CODES.md`.
- **Examples change** (`examples/`) → revalidate examples against the active schemas; keep
  data fake; confirm no private internals or real customer data are introduced.
- **ERPNext connector push change** (`connectors/erpnext/`) → confirm push remains
  **draft-only** (never auto-post); review connector mapping, config examples, and
  `docs/ERPNext_CONNECTOR_GUIDE.md`; confirm PO, UOM, and tax stay optional.
- **Validation tool change** (`tools/`) → confirm tools validate against the active schemas
  only (not `schemas/v0_4/*`); review related examples and developer docs.

## Status notes

- Implementation progress exists across the A1–A9 sequence, but formal acceptance/closure
  remains pending through the governance path unless an explicit acceptance record exists.
- **B2** (Core/SDK contract alignment) remains open / incomplete; it is not declared
  complete here.
- **DD-3** (public JSON-Schema hardening) remains open; it is not declared closed here.
