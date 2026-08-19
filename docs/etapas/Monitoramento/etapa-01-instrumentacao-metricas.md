# Etapa 01 — Instrumentação da API com `prometheus_client`

**Trilha:** Monitoramento — Fernando  
**Data:** 2026-08-18  
**Branch:** `feature/monitoring`  
**Atividade:** `F1` do `docs/TODO.md`

---

## 1. Objetivo da etapa

Expor métricas operacionais e de negócio da API FastAPI de triagem médica em formato padrão Prometheus (`/metrics`), permitindo coletar em tempo real:
1. Volume total de requisições e distribuição por classe de urgência (`normal`, `atenção`, `urgente`).
2. Latência fim a fim (tempo de resposta) de cada predição.
3. Taxa e tipos de erros (erros de validação HTTP 422, erros HTTP e erros internos).

---

## 2. Problema que estamos resolvendo

Uma API em produção sem métricas é uma "caixa preta". Não é possível saber:
- Quantos laudos estão sendo triados por minuto.
- Se o tempo de resposta está se degradando sob carga.
- Se requisições estão falhando por formato inválido de texto ou indisponibilidade do modelo.

Ao instrumentar a aplicação com `prometheus-client`, a API passa a fornecer telemetria estruturada pronta para consumo pelo Prometheus e exibição no Grafana.

---

## 3. O que foi implementado

### 3.1 Métricas definidas em `src/triage/api.py`

| Métrica | Tipo Prometheus | Labels | Descrição |
|---|---|---|---|
| `triage_requests_total` | `Counter` | `label` (`normal`, `atenção`, `urgente`) | Total de requisições de predição bem-sucedidas por classe |
| `triage_request_duration_seconds` | `Histogram` | `le` (buckets) | Duração fim a fim da predição em segundos |
| `triage_errors_total` | `Counter` | `error_type` (`erro_validacao`, `erro_http`, `erro_interno`) | Contagem de erros por categoria |
| `triage_prediction_confidence` | `Histogram` | `label` | Escore de confiança da predição (0.5 a 1.0) para detecção de Data Drift |
| `triage_input_length_chars` | `Histogram` | `le` | Tamanho do laudo clínico recebido em caracteres |
| `triage_model_loaded` | `Gauge` | - | Indicador de liveness do modelo (1 = carregado, 0 = indisponível) |

### 3.2 Configuração de Buckets de Latência

Para capturar com alta fidelidade tanto predições ultra-rápidas (< 5ms) quanto eventuais picos de carga sem consumir memória excessiva, definimos buckets otimizados:

```python
_REQUEST_LATENCY = Histogram(
    "triage_request_duration_seconds",
    "End-to-end prediction latency in seconds",
    buckets=(0.001, 0.0025, 0.005, 0.01, 0.025, 0.05, 0.075, 0.1, 0.25, 0.5, 1.0, 2.5, float("inf")),
)
```

### 3.3 Tratamento de Erros de Validação

Adicionamos um exception handler para `RequestValidationError` do FastAPI, garantindo que payloads com texto vazio, campos ausentes ou tipos incorretos incrementem `triage_errors_total{error_type="erro_validacao"}` antes de retornar HTTP 422 ao cliente.

### 3.4 Endpoint `/metrics`

O endpoint `GET /metrics` gera o snapshot mais recente no formato de texto oficial do Prometheus via `generate_latest()` com content type `CONTENT_TYPE_LATEST`.

---

## 4. Tecnologias escolhidas

- **`prometheus-client` (v0.22.1):** Biblioteca padrão e oficial para Python, leve, thread-safe, sem dependências pesadas externas e com suporte nativo a contadores, histogramas e formatação do endpoint.

---

## 5. Como testar localmente

```bash
# 1. Executar a API localmente
uvicorn triage.api:app --reload --port 8000

# 2. Fazer uma requisição de predição válida
curl -X POST http://localhost:8000/predict \
  -H "Content-Type: application/json" \
  -d '{"text": "Diagnosis: SEPSIS\nSex: F\nAge: 70\nAbnormal lab results:\n- Lactate: 4.1 mmol/L (abnormal)"}'

# 3. Fazer uma requisição inválida para testar métrica de erro
curl -X POST http://localhost:8000/predict \
  -H "Content-Type: application/json" \
  -d '{"text": ""}'

# 4. Consultar as métricas exportadas
curl http://localhost:8000/metrics
```

No output de `/metrics`, você verá:
```text
# HELP triage_requests_total Total prediction requests
# TYPE triage_requests_total counter
triage_requests_total{label="urgente"} 1.0

# HELP triage_errors_total Total prediction errors
# TYPE triage_errors_total counter
triage_errors_total{error_type="validation"} 1.0

# HELP triage_request_duration_seconds End-to-end prediction latency in seconds
# TYPE triage_request_duration_seconds histogram
triage_request_duration_seconds_bucket{le="0.005"} 0.0
triage_request_duration_seconds_bucket{le="0.01"} 1.0
...
triage_request_duration_seconds_count 1.0
```

---

## 6. Próximo passo

Prosseguir para a **Etapa 02 (F2)**: Configuração do Prometheus para realizar o *scrape* automático do endpoint `/metrics` da API.
