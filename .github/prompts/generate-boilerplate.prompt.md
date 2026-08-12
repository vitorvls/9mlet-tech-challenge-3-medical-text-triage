---
description: "Gerar código inicial alinhado com a stack e arquitetura"
---

# Generate Boilerplate

## Objective

Gerar boilerplate mecânico **somente** com a stack aprovada do Tech Challenge.

## Project Context

- Python + FastAPI
- Allowed: `.github/libs/allowed-libs.md`
- Forbidden: `.github/libs/forbidden-libs.md`
- Requirements: `.github/context/tech-challenge-requirements.md`
- Style: `.github/rules/code-style.md`

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

- `.github/libs/allowed-libs.md`
- `.github/context/architecture.md`
- `.github/context/tech-stack.md`
