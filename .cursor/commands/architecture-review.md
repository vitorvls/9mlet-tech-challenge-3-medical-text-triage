# Architecture Review

## Objective

Validar decisões arquiteturais contra o Tech Challenge e detectar overengineering.

## Project Context

- Python + FastAPI + NLP classifier
- Docker, Compose (API + Prometheus + Grafana), Airflow, GitHub Actions
- Fonte: `.cursor/context/tech-challenge-requirements.md`
- Arquitetura alvo: `.cursor/context/architecture.md`

## Instructions

Act as the architect responsible for delivery quality.

1. Check adherence to the **four stages** (API/Docker/baseline, CI+Airflow, Compose monitoring, optimization+STAR evidence).
2. Verify nothing FORA DO ESCOPO was introduced without explicit project decision.
3. Flag confusion between OBRIGATÓRIO and EXEMPLO FIAP.
4. Point out overengineering (extra services, auth, DB, K8s, etc.).
5. Assess alignment with evaluation weights (Modeling 20%, Monitoring 20%, etc.).

## Constraints

- Do not implement code
- Prefer the simplest architecture that still scores on all criteria
- Consult requirements file before concluding gaps

## Output

- Stage-by-stage compliance
- Overengineering findings
- Example-vs-mandatory confusions
- Prioritized recommendations

## Related Documentation

- `.cursor/context/tech-challenge-requirements.md`
- `.cursor/context/architecture.md`
- `.cursor/context/tech-stack.md`
