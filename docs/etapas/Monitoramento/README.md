# Trilha Fernando — Monitoramento

**Dono:** Fernando  
**Critério FIAP (20%):** `prometheus_client` + Docker Compose (API + Prometheus + Grafana) + ≥ 3 painéis no Grafana.  
**Branch:** `feature/monitoring`

---

## Estrutura das Etapas

| Arquivo | Etapa | Descrição | Status |
|---|---|---|---|
| [etapa-01-instrumentacao-metricas.md](etapa-01-instrumentacao-metricas.md) | Etapa 01 (F1) | Instrumentação da API FastAPI com `prometheus_client` (`/metrics`, contadores, histograma com buckets, tratamento de erros) | Concluída |
| [etapa-02-prometheus.md](etapa-02-prometheus.md) | Etapa 02 (F2) | Configuração do Prometheus (`monitoring/prometheus/prometheus.yml`) para *scrape* a cada 5s | Concluída |
| [etapa-03-docker-compose.md](etapa-03-docker-compose.md) | Etapa 03 (F3) | Orquestração da stack completa (API + Prometheus + Grafana) via `docker-compose.yml` | Concluída |
| [etapa-04-grafana-dashboards.md](etapa-04-grafana-dashboards.md) | Etapa 04 (F4) | Provisionamento automático de DataSource e Dashboards no Grafana (8 painéis: requisições, latência p50/p95/p99, distribuição e erros) | Concluída |

---

## Como executar a stack completa

```bash
# 1. Subir todos os serviços
docker compose up -d --build

# 2. Simular tráfego contínuo para alimentar os gráficos em tempo real (encerra com Ctrl+C)
python scripts/simulate_traffic.py

# 3. Acessar interfaces
# API:        http://localhost:8000/docs
# Métricas:   http://localhost:8000/metrics
# Prometheus: http://localhost:9090
# Grafana:    http://localhost:3000
```
