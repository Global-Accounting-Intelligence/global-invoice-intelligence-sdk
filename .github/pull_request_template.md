<!--
SDK-local pull request template.
This is an SDK-local pointer artifact. The binding policy is the planning-repo
`governance/documentation-as-code-and-architecture-drift-control.md` in
`global-accounting-intelligence`. Do not duplicate that policy here.
Complete every section. Do not delete sections; write "None" where not applicable.
-->

## Summary

<!-- What this change does and why. -->

## Files Changed

<!-- List each file added/modified/removed. -->

## Tests Run

<!-- Commands run and their outcome, or "None" with justification. -->

## Documentation Impact

<!-- Docs added/updated, or "None". -->

## Contract Impact

<!-- Effect on public I/O contracts, or "None". -->

## Schema/OpenAPI Impact

<!-- Effect on schemas/ or openapi/openapi.yaml, or "None — no schema/OpenAPI change". -->

## SDK Public Interface Impact

<!-- Effect on public SDK client surface (python/javascript), or "None". -->

## Examples Impact

<!-- Effect on examples/, or "None". -->

## Connector Impact

<!-- Effect on connectors/ (ERPNext, Odoo, generic-rest), or "None". -->

## Architecture Impact

<!-- Effect on module/documentation maps or architecture docs, or "None". -->

## Governance/Boundary Impact

<!-- Effect on public/private boundary and governance pointers, or "None". -->

## Conflicts Detected

<!-- Any conflict between code and public schemas/OpenAPI. Report; do not silently
     rewrite contracts to fit code. "None" if no conflict. -->

## Remaining Risks

<!-- Open risks after this change. -->

## Checklist

- [ ] No private Core logic exposed.
- [ ] No matching, trust, scoring, or learning internals exposed (no matching weights,
      trust weights/tier internals, scoring formulas, or learning internals).
- [ ] No schema or OpenAPI changed unless this task explicitly authorized it.
- [ ] If schema/OpenAPI changed: docs, examples, SDK clients, validation tools, and tests
      were reviewed for impact.
- [ ] No `schemas/v0_4/*` used as the active contract (it stays retired / reference-only).
- [ ] ERPNext push remains draft-only (never auto-post).
- [ ] PO, UOM, and tax remain optional signals (never mandatory).
- [ ] B2 (Core/SDK contract alignment) is **not** declared complete unless the formal
      acceptance/closure path in the planning repo says so.
- [ ] DD-3 (public JSON-Schema hardening) is **not** declared closed unless the formal
      acceptance/closure path in the planning repo says so.
