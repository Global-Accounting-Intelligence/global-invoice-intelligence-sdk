# CLAUDE.md — SDK-local pointer

This is a short **SDK-local pointer** file. It does not restate policy; it points to the
documents that govern work in this public SDK repository.

## Read these first

- **`AGENTS.md`** — SDK-local agent instructions: the before-change impact checklist,
  contract/schema handling rules, public/private boundary, and the required final report.
- **`.github/pull_request_template.md`** — the impact sections and boundary checklist
  every PR must complete.
- **`docs/architecture/sdk-documentation-map.md`** — what this repo owns vs. does not own,
  and what to review when each area changes.
- **`docs/architecture/sdk-module-map.md`** — SDK responsibility areas by folder.

## Binding governance policy (planning repo)

The binding Documentation-as-Code & Architecture Drift Control policy lives in the
planning repository `global-accounting-intelligence`:

- `governance/documentation-as-code-and-architecture-drift-control.md`

This SDK repo does **not** own that policy and must **not** duplicate it. Follow it as the
source of truth.

## Public/private boundary (non-negotiable)

This repository is **public**. It exposes public I/O contracts, developer ergonomics,
examples, validation tools, and connector starters only. Never expose private Core logic,
matching weights, trust weights or trust-tier internals beyond already-public contract
references, scoring formulas, learning internals, tenant knowledge-graph internals, raw
prompts, hidden reasoning, raw provider responses, or cross-tenant learning. Public
schemas/OpenAPI are API I/O contracts, not the internal Core model. ERPNext push stays
draft-only (never auto-post); PO, UOM, and tax stay optional (never mandatory);
`schemas/v0_4/*` stays retired / reference-only.
