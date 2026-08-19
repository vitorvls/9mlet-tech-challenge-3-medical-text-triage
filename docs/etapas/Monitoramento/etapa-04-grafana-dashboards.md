# Etapa 04 — Grafana Dashboards e Provisionamento Automático

**Trilha:** Monitoramento — Fernando  
**Data:** 2026-08-18  
**Branch:** `feature/monitoring`  
**Atividade:** `F4` do `docs/TODO.md`

---

## 1. Objetivo da etapa

Construir o painel visual no **Grafana** com provisionamento automático e **múltiplos painéis** (atendendo e superando a exigência de ≥ 3 painéis do Tech Challenge FIAP), permitindo observar métricas de negócio de Machine Learning e saúde operacional em tempo real.

---

## 2. Problema que estamos resolvendo

Configurar gráficos manualmente via interface do Grafana toda vez que a máquina ou container sobe é lento, não reproduzível e sujeito a inconsistências. 

Para resolver isso, implementamos o **provisionamento como código (*dashboard as code*)**: o Grafana já inicializa com a fonte de dados Prometheus conectada e o dashboard carregado e pronto para uso, sem intervenção manual.

---

## 3. Estrutura de Arquivos Criada

```text
monitoring/
├── prometheus/
│   └── prometheus.yml                     # Alvo de scrape da API
└── grafana/
    ├── provisioning/
    │   ├── datasources/
    │   │   └── datasource.yml             # Conecta ao Prometheus automaticamente
    │   └── dashboards/
    │       └── dashboards.yml             # Provider apontando para a pasta de JSONs
    └── dashboards/
        └── medical-triage-dashboard.json  # Definição visual completa do dashboard
```

---

## 4. Detalhamento dos Painéis Implementados

O dashboard **Medical Text Triage — Dashboard Operacional** possui **14 visualizações** organizadas em 4 linhas temáticas:

### 4.1 Linha 1: Visão Executiva, SLA & Disponibilidade (Meta: 99.0%)
1. **Disponibilidade do Serviço vs SLA (Meta $\ge 99\%$)** (Gauge):
   - **PromQL:** `100 - (((sum(rate(triage_errors_total[5m])) or vector(0)) / ((sum(rate(triage_requests_total[5m])) or vector(0)) + (sum(rate(triage_errors_total[5m])) or vector(0)))) * 100 or vector(0))`
   - **Semáforo:** Verde $\ge 99\%$, Amarelo $95-99\%$, Vermelho $< 95\%$.
2. **Error Budget Consumido (Meta $\le 1\%$)** (Stat):
   - **PromQL:** `(((sum(rate(triage_errors_total[5m])) or vector(0)) / ((sum(rate(triage_requests_total[5m])) or vector(0)) + (sum(rate(triage_errors_total[5m])) or vector(0)))) * 100) or vector(0)`
3. **Status do Modelo em Memória** (Stat):
   - **PromQL:** `triage_model_loaded` (`🟢 OPERACIONAL (baseline.joblib)` quando 1).
4. **Total de Requisições Processadas**: `sum(triage_requests_total) or vector(0)`.
5. **Throughput Atual (req/s)**: `sum(rate(triage_requests_total[1m])) or vector(0)`.

### 4.2 Linha 2: Métricas de Inteligência Artificial & NLP (Qualidade do Modelo)
6. **Confiança Média Geral da IA (Detecção de Drift)** (Stat com Sparkline):
   - **PromQL:** `(sum(rate(triage_prediction_confidence_sum[1m])) / sum(rate(triage_prediction_confidence_count[1m]))) * 100`
   - **Alerta de Drift:** Verde $\ge 50\%$, Amarelo $40-50\%$, Vermelho $< 40\%$ (calibrado para 3 classes, onde incerteza máxima é 33.3%).
7. **Confiança Média por Classe de Triagem** (Bar Gauge):
   - **PromQL:** `(sum by (label) (rate(triage_prediction_confidence_sum[1m])) / sum by (label) (rate(triage_prediction_confidence_count[1m]))) * 100`
8. **Painel 1 FIAP — Volume de Predições por Classe** (Time Series):
   - **PromQL:** `sum by (label) (rate(triage_requests_total[1m]))`
9. **Tamanho Médio do Laudo Clínico (chars)** (Time Series):
   - **PromQL:** `sum(rate(triage_input_length_chars_sum[1m])) / sum(rate(triage_input_length_chars_count[1m]))`

### 4.3 Linha 3: Desempenho e Latência de Inferência
10. **Painel 2 FIAP — Latência de Inferência (Percentis p50, p95, p99 em ms)** (Time Series):
    - **PromQL (p50):** `histogram_quantile(0.50, sum by (le) (rate(triage_request_duration_seconds_bucket[1m]))) * 1000`
    - **PromQL (p95):** `histogram_quantile(0.95, sum by (le) (rate(triage_request_duration_seconds_bucket[1m]))) * 1000`
    - **PromQL (p99):** `histogram_quantile(0.99, sum by (le) (rate(triage_request_duration_seconds_bucket[1m]))) * 1000`
11. **Latência Média de Inferência (ms)**:
    - **PromQL:** `(rate(triage_request_duration_seconds_sum[1m]) / rate(triage_request_duration_seconds_count[1m])) * 1000`

### 4.4 Linha 4: Monitoramento de Erros, Falhas & Distribuição
12. **Painel 3 FIAP — Taxa de Erros e Falhas Operacionais** (Time Series em Vermelho):
    - **PromQL:** `sum by (error_type) (rate(triage_errors_total[1m]))`
    - **Legendas:** `Erro de Validação de Laudo (HTTP 422)`, `Erro HTTP na Inferência (HTTP 4xx)`, `Erro Interno do Servidor (HTTP 500)`.
13. **Total de Erros Operacionais** (Stat com destaque em Vermelho).
14. **Distribuição Acumulada por Classe de Triagem** (Donut Chart).

---

## 5. Simulação de Carga e Demonstração Contínua (SLA 99% / Error Budget 1%)

O script `scripts/simulate_traffic.py` foi calibrado para disparar requisições com taxa estocástica de **1% de erros / 99% de sucessos**:

```bash
# Modo contínuo (padrão): opera até Ctrl+C com 99% de disponibilidade e 1% de erro
python scripts/simulate_traffic.py

# Ajustando a taxa de erro desejada (ex: testar violação de SLA com 5% de erros):
python scripts/simulate_traffic.py --error-rate 0.05

# Modo fixo de requisições:
python scripts/simulate_traffic.py --count 100 --error-rate 0.01
```

O script envia laudos médicos realistas extraídos do padrão MIMIC e casos inválidos em loop contínuo, mantendo os gráficos do Grafana dinâmicos e atualizados. Ao pressionar `Ctrl+C`, ele exibe um relatório consolidado com total de requisições, tempo e distribuição percentual de classes e erros.

---

## 6. Evidências Geradas

- Artefato do dashboard exportado: `evidencias/grafana_dashboard.json`.
- Acesso local: [http://localhost:3000](http://localhost:3000) (Login automático ou `admin`/`admin`).

---

## 7. Conclusão do Checkpoint Fernando A (`CA-Fernando`)

Com esta etapa concluída:
- [x] API FastAPI totalmente instrumentada com `prometheus_client`
- [x] Prometheus configurado com scrape a cada 5s
- [x] Docker Compose orquestrando os 3 serviços
- [x] Grafana pré-configurado com ≥ 3 painéis (8 painéis ao todo)
- [x] Script de simulação de tráfego criado
