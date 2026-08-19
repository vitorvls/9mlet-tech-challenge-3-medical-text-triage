# Etapa 02 — Integração com o modelo do Vítor

**Trilha:** API e Docker — Vini  
**Data:** 2026-08-18  
**Branch:** `feat/api-docker-baseline`

---

## O que foi feito (em linguagem simples)

A API agora usa o modelo real do Vítor (`models/baseline.joblib`) em vez de um mock.  
Também criamos os testes automáticos da API.

---

## Integração do modelo

### Como a API carrega o modelo

O artefato `models/baseline.joblib` é um `Pipeline` sklearn (TF-IDF + Logistic Regression).  
A API o carrega **uma única vez** quando o servidor sobe, usando o evento `lifespan` do FastAPI.

Fluxo:

```
servidor sobe
    └── lifespan startup
            └── triage.predict.get_pipeline("models/baseline.joblib")
                    └── joblib.load → guarda na memória do processo
```

A partir daí cada requisição `POST /predict` só chama `predict(text)` — sem re-carregar o arquivo.

### Tratamento de erro se o modelo não existir

| Situação | O que acontece |
|----------|----------------|
| Arquivo não encontrado no startup | API sobe mesmo assim; `model_loaded: false` no `/health` |
| Requisição chega sem modelo | HTTP 503 com mensagem "Run: python src/triage/train.py" |
| Modelo carregado mas texto inválido | HTTP 422 com detalhe do erro de validação |

### Teste com textos reais do dataset

Os três textos dos exemplos documentados no `predict.py` do Vítor foram usados nos testes:

| Texto | Label esperada | Resultado |
|-------|---------------|-----------|
| Sepsis (Lactato 4.1, WBC 18.2) | `urgente` | ✅ |
| Cirurgia eletiva carotídea | `normal` | ✅ |
| Parada ventricular (CK 4127) | qualquer válido | ✅ |

---

## Testes criados

Arquivo: `tests/test_api.py` (11 testes, todos passando)

| Teste | O que verifica |
|-------|----------------|
| `test_health_returns_200` | `/health` retorna 200 com `status: ok` |
| `test_predict_returns_valid_schema` | resposta tem `label` e `confidence` com tipos corretos |
| `test_predict_sepsis_classified_as_urgente` | texto de sepse → label `urgente` |
| `test_predict_elective_classified_as_normal` | texto eletivo → label `normal` |
| `test_predict_confidence_is_float` | `confidence` é float |
| `test_predict_rejects_empty_text` | texto vazio → 422 |
| `test_predict_rejects_blank_text` | texto só com espaços → 422 |
| `test_predict_rejects_missing_text_field` | JSON sem campo `text` → 422 |
| `test_predict_rejects_non_string_text` | `text: 123` (número) → 422 |
| `test_metrics_endpoint_is_accessible` | `/metrics` retorna 200 |
| `test_metrics_populated_after_predict` | histogram aparece no `/metrics` após uma previsão |

### Como rodar os testes

```bash
# Da raiz do projeto, com o .venv ativado
.venv/bin/pytest tests/test_api.py -v
```

---

## O que mudou no código

- `src/triage/api.py`: migrado de `@app.on_event("startup")` (deprecated) para `lifespan` (padrão atual do FastAPI).
- `tests/test_api.py`: criado — cobre happy path, validação e métricas.
