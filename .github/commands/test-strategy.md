# Test Strategy

## Objective

Planejar testes alinhados ao CI do Tech Challenge (sem impor TDD ou coverage %).

## Project Context

- Python + FastAPI + NLP inference
- CI: GitHub Actions with tests (EXEMPLO FIAP: pytest)
- Rules: `.github/rules/testing-rules.md`
- Requirements: `.github/context/tech-challenge-requirements.md`

## Instructions

For the module/feature in scope:

1. Critical scenarios (API predict, validation, metrics exposure when relevant)
2. Unit tests needed
3. Essential integration tests
4. Edge cases (empty text, invalid payload)
5. What NOT to test yet (frontend, auth, DB) unless decided

## Constraints

- Do not write code yet
- Do not mandate TDD or coverage thresholds
- Prefer pytest as the natural path from the PDF example
- Keep scope proportional to CI/CD evaluation weight (15%)

## Output

Structured test plan prioritized by delivery risk.

## Related Documentation

- `.github/rules/testing-rules.md`
- `.github/context/tech-challenge-requirements.md`
