# AGENTS.md — Global Invoice Intelligence SDK

## Purpose

This public repository contains the open-source developer-facing assets for Global Invoice Intelligence.

It includes:

- public schemas
- SDKs
- connector starters
- examples
- documentation
- OpenAPI specification

It must not include private matching algorithms, trust engine logic, tenant learning logic, commercial scoring rules, or customer data.

## Public Repository Rules

Allowed:

- API documentation
- OpenAPI specs
- JSON schemas
- sample invoices with fake data
- SDK clients
- connector starters
- webhook examples
- validation tools

Not allowed:

- private matching engine code
- private material scoring algorithm
- private trust engine logic
- private learning engine logic
- real customer invoices
- real customer names
- API secrets
- internal deployment details
- private roadmap details

## Developer Experience Goal

This repository should make it easy for a developer to integrate Global Invoice Intelligence in less than one day.

Prioritize:

- clear README
- quick start
- API examples
- Postman collection
- SDK examples
- connector examples
- error handling documentation
- webhook examples

## Documentation-as-Code & Architecture Drift Control (SDK-local pointer)

This section is an **SDK-local pointer**. The binding governance policy lives in the
planning repository `global-accounting-intelligence`:

- `governance/documentation-as-code-and-architecture-drift-control.md`

This SDK repository does **not** own that policy and must **not** duplicate it locally.
Follow the planning-repo policy as the source of truth; the instructions below are the
thin, repo-local restatement of how to apply it inside this SDK repo.

### Before any SDK change

Before making any change in this repo, determine and record the impact across each of:

- documentation impact
- contract impact
- schema impact
- OpenAPI impact
- SDK public interface impact
- examples impact
- connector impact
- architecture impact
- public/private boundary impact

### Contract & schema handling rules

- Do **not** modify schemas or OpenAPI unless the task explicitly authorizes it.
- If code conflicts with the public schemas or OpenAPI, **report the conflict**. Do not
  silently rewrite the contracts to fit the code. Public schemas and OpenAPI are the
  API I/O contract, not a mirror of internal Core behaviour.
- If a schema or OpenAPI change is authorized, review the downstream impact on docs,
  examples, SDK clients, validation tools, and tests before completing the change.
- `schemas/v0_4/*` is retired / reference-only and must **not** be used as the active
  contract.

### Public/private boundary (must hold for every change)

This repository is public and exposes public I/O contracts, developer ergonomics,
examples, validation tools, and connector starters only. It must never expose private
Core logic, matching weights, trust weights or trust-tier internals beyond
already-public contract references, scoring formulas, learning internals, tenant
knowledge-graph internals, raw prompts, hidden reasoning, raw provider responses, or
cross-tenant learning. ERPNext push must remain draft-only and never auto-post. PO,
UOM, and tax remain optional signals and must never be made mandatory.

### Final report (required at the end of every task)

End every task with a final report covering:

- Files changed
- Tests run
- Documentation impact
- Contract impact
- Schema/OpenAPI impact
- SDK public interface impact
- Examples impact
- Architecture impact
- Binding documents changed
- Derived documents changed
- Conflicts detected
- Remaining risks

See also the SDK-local maps `docs/architecture/sdk-documentation-map.md` and
`docs/architecture/sdk-module-map.md`, and the PR template
`.github/pull_request_template.md`.
