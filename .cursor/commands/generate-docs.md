# Generate Documentation

## Objective

Gerar documentação viva priorizando o que a FIAP avalia no README e nas evidências das 4 etapas.

## Project Context

- Requirements: `.cursor/context/tech-challenge-requirements.md`
- Deployment/cloud notes: `.cursor/context/deployment.md`
- Evaluation: README 15% (cloud strategy + clear run instructions)

## Instructions

When asked for project docs, prioritize in this order:

1. **README do desafio**
   - Estratégia cloud (batch vs real-time) com justificativa
   - Instruções claras de execução (API Docker, Compose, CI, Airflow, etc.)
2. Evidências de latência (baseline + original vs otimizado)
3. Como ver métricas Prometheus/Grafana (≥3 painéis)
4. Documentação de módulos (responsibility, data flow, decisions) se solicitado

Classify statements as OBRIGATÓRIO / EXEMPLO / DECISÃO / PENDENTE when documenting requirements.

## Constraints

- Do not invent a completed cloud provider decision if still PENDENTE — mark it
- Do not document diagnosis/treatment capabilities
- Avoid generic filler; be specific to this repo

## Output

Documentation ready to paste into README/docs, with clear sections for cloud + runbook + evidence links.

## Related Documentation

- `.cursor/context/tech-challenge-requirements.md`
- `.cursor/context/deployment.md`
- `.cursor/context/architecture.md`
