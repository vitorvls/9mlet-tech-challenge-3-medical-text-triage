# Generate Boilerplate

## Objective

Gerar boilerplate mecânico **somente** com a stack aprovada do Tech Challenge.

## Project Context

- Python + FastAPI
- Allowed: `.cursor/libs/allowed-libs.md`
- Forbidden: `.cursor/libs/forbidden-libs.md`
- Requirements: `.cursor/context/tech-challenge-requirements.md`
- Style: `.cursor/rules/code-style.md`

## Instructions

Generate boilerplate for the requested module following:

1. Approved stack only (FastAPI, prometheus_client, sklearn-or-chosen-framework, etc.)
2. Existing project patterns; no new abstraction layers
3. No JWT, DB, Redis, Node, Express, frontend scaffolds
4. If the request depends on a PENDENTE DE DECISÃO (dataset, optimizer, linter): stop and ask

## Constraints

- Consult allowlist before adding imports/dependencies
- Do not choose optional libraries silently
- Keep comments minimal; code names in English

## Output

Ready-to-adapt boilerplate + short explanation of structure + list of assumptions.

## Related Documentation

- `.cursor/libs/allowed-libs.md`
- `.cursor/context/architecture.md`
- `.cursor/context/tech-stack.md`
