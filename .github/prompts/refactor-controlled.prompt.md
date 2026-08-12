---
description: "Refatoração controlada preservando contratos e testes"
---

# Refactor Controlled

## Objective

Melhorar código sem alterar comportamento.

## Project Context

- Python + FastAPI + NLP triage service
- Style: `.github/rules/code-style.md`
- Tests: `.github/rules/testing-rules.md`

## Instructions

Refactor selected code to:

1. Improve readability
2. Reduce complexity
3. Keep 100% of current behavior and public interfaces

## Constraints

- Do not change business behavior
- Keep existing tests passing
- Do not introduce new dependencies or architecture layers
- Do not “accidentally” add auth/DB/cloud

## Output

Refactored code + list of changes + behavior-preservation notes.

## Related Documentation

- `.github/rules/code-style.md`
- `.github/rules/testing-rules.md`
- `.github/context/tech-challenge-requirements.md`
