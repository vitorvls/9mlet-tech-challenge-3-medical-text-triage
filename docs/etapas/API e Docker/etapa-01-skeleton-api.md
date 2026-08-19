# Etapa 01 — Skeleton da API FastAPI

**Trilha:** API e Docker — Vini  
**Data:** 2026-08-18  
**Branch:** `feat/api-docker-baseline`

---

## O que foi feito (em linguagem simples)

Criamos a "janela" por onde o texto do laudo entra e a classificação sai.

Nesta etapa o modelo **já está integrado** (o artefato `models/baseline.joblib` do Vítor já existia na branch base). Por isso pulamos o mock e subimos a integração real direto — ver Etapa 02 para o detalhe da integração.

### Arquivo criado

`src/triage/api.py` — aplicação FastAPI com três endpoints:

| Endpoint | Método | Para que serve |
|----------|--------|----------------|
| `/health` | GET | Confirma que a API está no ar e se o modelo foi carregado |
| `/predict` | POST | Recebe `{"text": "..."}` e devolve `{"label": "...", "confidence": 0.XX}` |
| `/metrics` | GET | Expõe métricas no formato Prometheus (latência, contagens, erros) |

### Contrato fechado (do TODO 0.2)

**Entrada:**
```json
{ "text": "texto do laudo médico aqui" }
```

**Saída de sucesso:**
```json
{ "label": "urgente", "confidence": 0.91 }
```

### Validações implementadas

- Campo `text` vazio ou só espaços → HTTP 422 (Unprocessable Entity)
- Tipo errado (não-string) → HTTP 422 (Pydantic valida automaticamente)
- Modelo não carregado → HTTP 503 (Service Unavailable) com mensagem de como treinar

### Métricas Prometheus (preparadas para o Fernando)

| Métrica | Tipo | O que mede |
|---------|------|-----------|
| `triage_requests_total` | Counter | Total de previsões, separado por `label` |
| `triage_request_duration_seconds` | Histogram | Latência ponta-a-ponta de cada chamada |
| `triage_errors_total` | Counter | Erros, separado por tipo (`http` / `internal`) |

### Dependências adicionadas ao `pyproject.toml`

```
fastapi==0.115.14
uvicorn[standard]==0.35.0
prometheus-client==0.22.1
```

Dependências de dev (testes):
```
httpx==0.28.1
pytest==8.3.5
pytest-asyncio==0.24.0
```

---

## Como rodar localmente

```bash
# 1. Instalar as dependências (da raiz do projeto)
pip install -e ".[dev]"

# 2. Subir a API
uvicorn triage.api:app --reload

# 3. Testar no Swagger
# Abra http://localhost:8000/docs no navegador

# 4. Testar via curl
curl -s -X POST http://localhost:8000/predict \
  -H "Content-Type: application/json" \
  -d '{"text": "Diagnosis: SEPSIS\nSex: F\nAge: 70\nAbnormal lab results:\n- Lactate: 4.1 mmol/L (abnormal)"}'
```

---

## Decisões tomadas

- **Sem mock:** o modelo do Vítor já estava pronto; a integração real foi feita diretamente.
- **Carregamento lazy com warm-up no startup:** o Pipeline é carregado uma vez por processo (`startup_event`). Se o modelo não existir, a API sobe mesmo assim e retorna 503 só no `/predict`.
- **Sem logs do texto do laudo** por padrão (regra de segurança: não expor PII desnecessariamente).
- **prometheus-client** embutido na API (não em middleware separado): suficiente para o protótipo.
