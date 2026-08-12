---
description: "Kickoff de etapa/tarefa alinhado com requisitos FIAP"
---

# Kickoff Project

## Objective

Alinhar entendimento do **Tech Challenge** antes de implementar código.

## Project Context

- **Project:** `9mlet-tech-challenge-3-medical-text-triage`
- **Stack:** Python + FastAPI + classificador NLP leve
- **Entrega:** Docker, GitHub Actions, Airflow, Prometheus/Grafana (Compose), otimização de latência, README cloud, vídeo STAR

**Fonte de verdade:** `.github/context/tech-challenge-requirements.md`  
**Goals:** `.github/context/project-goals.md`

## Instructions

You are a senior software architect for an academic MLOps challenge.

1. Read `tech-challenge-requirements.md` and summarize:
   - OBRIGATÓRIO
   - EXEMPLO FIAP (não transformar em obrigação)
   - RECOMENDAÇÃO
   - PENDENTE DE DECISÃO
   - FORA DO ESCOPO

2. List functional needs of the inference API (text → classification) without inventing clinical diagnosis features.

3. List non-functional needs tied to the challenge: latency, CI/CD, monitoring, retrain orchestration.

4. Propose a **minimal** high-level architecture for the four stages. Flag overengineering.

5. List risks and open decisions that require human approval.

## Constraints

- Do not generate implementation code
- Do not assume database, JWT, frontend, Redis, or Kubernetes
- Do not choose dataset, model algorithm, or optimization technique
- Do not present product users as a FIAP requirement
- Respond in structured form (pt-BR unless asked otherwise)

## Output

- Requirements summary by category
- Minimal architecture proposal
- Open decisions / risks
- Suggested order of work aligned to evaluation weights

## Related Documentation

- `.github/context/tech-challenge-requirements.md`
- `.github/context/project-goals.md`
- `.github/context/architecture.md`
