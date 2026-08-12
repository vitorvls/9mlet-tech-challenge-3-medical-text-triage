# Extract Business Rules

## Objective

Tornar regras de domínio explícitas e testáveis, sem inventar requisitos clínicos.

## Project Context

- Triagem de laudos por classificação de urgência (NLP)
- Fonte: `.github/context/tech-challenge-requirements.md`
- Regras atuais: `.github/rules/business-rules.md`

## Instructions

Analyze context and related code (if any).

Extract:

1. Explicit rules (from docs/code)
2. Implicit rules inferred from code
3. Ambiguities needing human/product validation
4. For each rule, label origin: PDF OBRIGATÓRIO / EXEMPLO FIAP / DECISÃO DO PROJETO / código / ambígua

## Constraints

- Do not invent diagnosis/treatment rules
- Do not treat auth/DB as business rules unless explicitly decided
- Labels `normal`/`atenção`/`urgente` are EXEMPLO FIAP until dataset decision

## Output

Structured list with origin labels + validation recommendations.

## Related Documentation

- `.github/rules/business-rules.md`
- `.github/context/project-goals.md`
- `.github/context/tech-challenge-requirements.md`
