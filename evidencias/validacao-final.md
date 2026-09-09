# Validacao final da entrega

**Data:** 2026-09-08
**Branch:** `feat/cicd-airflow-pipeline`

## Checks locais

| Check | Resultado |
|---|---|
| `python -m pytest -q` | `14 passed` |
| `python -m flake8 src tests` | aprovado |
| Importacao da DAG | `medical_text_triage_training` carregada |
| Tarefas da DAG | `ingest_data`, `train_and_export_model` |
| Dependencia | `ingest_data` -> `train_and_export_model` |
| Auditoria de segredos | nenhum padrao de segredo hardcoded encontrado |
| Sanitizacao | caches temporarios removidos |

## Stack local no Rancher Desktop

| Check | Resultado |
|---|---|
| `docker compose up -d --build` | concluido |
| `triage-api` | `Up (healthy)` na porta `8000` |
| `GET /health` | HTTP `200`; `model_loaded: true` |
| `triage-prometheus` | `Up` na porta `9090` |
| `GET /-/ready` | HTTP `200`; `Prometheus Server is Ready.` |
| `triage-grafana` | `Up` na porta `3000` |

Essa validacao confirma a Opção 1 do README: API, Prometheus e Grafana
executados juntos pelo Docker Compose no Rancher Desktop.

## Pendencia externa

O ultimo run publico do GitHub Actions ainda e o run 5, que falhou antes das correcoes atuais. As correcoes locais precisam ser publicadas para gerar um novo run verde:

- Workflow: `.github/workflows/ci.yml`
- Run anterior: https://github.com/vitorvls/9mlet-tech-challenge-3-medical-text-triage/actions/runs/34167193869
- Branch: `feat/cicd-airflow-pipeline`

Esta evidencia registra somente resultados realmente executados localmente; nao afirma que o run remoto passou.
