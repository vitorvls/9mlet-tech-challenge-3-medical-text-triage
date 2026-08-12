---
description: "Revisão de Pull Request conforme critérios do projeto"
---

# Review PR

## Objective

Review educacional de PR no contexto do Tech Challenge.

## Project Context

- Python + FastAPI + NLP triage
- Requirements: `.github/context/tech-challenge-requirements.md`
- Testing: `.github/rules/testing-rules.md` (no mandatory TDD)
- Git: `.github/rules/git-rules.md`

## Instructions

Review as a senior engineer:

1. Clarity and Python/FastAPI idioms
2. Correctness vs business rules / inference contract
3. Test adequacy for the change (not coverage dogma)
4. Challenge compliance: does this PR help a scored deliverable or add out-of-scope complexity?
5. Flag EXEMPLO FIAP treated as hard requirement incorrectly

## Constraints

- Be constructive and actionable
- Do not require JWT/DB/TDD unless the PR itself introduced that decision with justification
- Prefer simplicity that still meets FIAP criteria

## Output

Strengths, issues, suggestions, challenge-compliance notes.

## Related Documentation

- `.github/rules/code-style.md`
- `.github/rules/testing-rules.md`
- `.github/rules/git-rules.md`
- `.github/context/tech-challenge-requirements.md`
