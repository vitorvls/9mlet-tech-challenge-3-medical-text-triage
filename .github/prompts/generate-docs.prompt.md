---
description: "Gerar e atualizar documentação do projeto e README"
---

# Generate Documentation

## Objective

Gerar documentação viva priorizando o que a FIAP avalia no README e nas evidências das 4 etapas.

## Project Context

- Requirements: `.github/context/tech-challenge-requirements.md`
- Deployment/cloud notes: `.github/context/deployment.md`
- Evaluation: README 15% (cloud strategy + clear run instructions)

## Instructions

When asked for project docs, prioritize in this order:

1. **`docs/etapas/<trilha>/etapa-NN.md`** da etapa que acabou de ser implementada (obrigatório; didático). Trilhas: `Modelagem e otimização`, `API e Docker`, `Monitoramento`, `CI-CD Airflow e documentacao`.
2. **README do desafio** (quando for a trilha do Edu / entrega FIAP)
   - Estratégia cloud (batch vs real-time) com justificativa
   - Instruções claras de execução (API Docker, Compose, CI, Airflow, etc.)
3. Evidências de latência (baseline + original vs otimizado)
4. Como ver métricas Prometheus/Grafana (≥3 painéis)

Uma etapa de código **não** está concluída sem o `.md` correspondente. Modelo/treino: explicar métricas em linguagem simples. Ver `.github/rules/documentation-rules.md`.

Classify statements as OBRIGATÓRIO / EXEMPLO / DECISÃO / PENDENTE when documenting requirements.

## Constraints

- Do not invent a completed cloud provider decision if still PENDENTE — mark it
- Do not document diagnosis/treatment capabilities
- Avoid generic filler; be specific to this repo

## Output

Documentation ready to paste into README/docs, with clear sections for cloud + runbook + evidence links.

## Related Documentation

- `.github/context/tech-challenge-requirements.md`
- `.github/context/deployment.md`
- `.github/context/architecture.md`
- `.github/rules/documentation-rules.md`
