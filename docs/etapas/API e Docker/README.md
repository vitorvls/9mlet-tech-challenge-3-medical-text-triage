# Trilha Vini — API e Docker

Dono: **Vini**. Critério FIAP: API FastAPI em Docker + baseline de latência (Etapa 1).

## Etapas concluídas

| # | Arquivo | Status | O que faz |
|---|---------|--------|-----------|
| 01 | [etapa-01-skeleton-api.md](etapa-01-skeleton-api.md) | ✅ | FastAPI com /health, /predict, /metrics + instrumentação Prometheus |
| 02 | [etapa-02-integracao-modelo.md](etapa-02-integracao-modelo.md) | ✅ | Integração com models/baseline.joblib + 11 testes automáticos |
| 03 | [etapa-03-dockerfile.md](etapa-03-dockerfile.md) | ✅ | Dockerfile multi-stage + .dockerignore |
| 04 | [etapa-04-baseline-latencia.md](etapa-04-baseline-latencia.md) | ✅ | Benchmark 100 req: Docker mean 7.4ms, p95 10.3ms |

## Checkpoint Vini A — ✅ concluído (2026-08-18)

- [x] Contrato da API estável
- [x] Docker build/run ok
- [x] Baseline de latência registrada em `evidencias/`

**Extra opcional (não é da rubrica):** page de demo form + chat — só se sobrar tempo, só consome endpoints já existentes. Ver `docs/TODO.md` (backlog).

Ver `docs/etapas/README.md` e `.cursor/rules/documentation-rules.md`.
