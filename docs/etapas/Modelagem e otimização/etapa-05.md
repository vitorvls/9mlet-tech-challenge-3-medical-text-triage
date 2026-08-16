# Etapa 05 — Checkpoint Vítor A (entrega da trilha A)

**Trilha:** Modelagem e otimização (Vítor)  
**Status:** concluída (critérios conferidos + recado ao time + este documento)  
**Data:** 2026-08-15

---

## Objetivo

Fechar o **pacote** que o resto do grupo usa daqui pra frente. Não há modelo novo nesta etapa: só conferir, congelar o contrato e avisar o time.

A partir daqui, Vini pode trocar o mock da API pelo `predict` real, e Edu pode apontar a DAG para os mesmos scripts/path.

---

## Problema que estávamos resolvendo

Sem um checkpoint explícito, cada um pergunta no chat:

- onde está o arquivo do modelo?
- como eu chamo a classificação?
- posso retreinar e sobrescrever o joblib?
- o F1 está “bom”?

Esta etapa responde isso por escrito, uma vez.

---

## Conferência dos três critérios (docs/TODO.md)

Smoke em 2026-08-15, venv Python 3.11.9:

| Critério | Status | Evidência |
|----------|--------|-----------|
| Modelo treinado salva e carrega | ok | `models/baseline.joblib` existe; `joblib.load` devolve um `Pipeline` com passos `tfidf` e `clf` |
| `predict` em ≥ 3 textos | ok | ver tabela abaixo (iguais à Etapa 04) |
| Path alinhado | ok | `triage.predict.DEFAULT_MODEL_PATH` = `models/baseline.joblib` na raiz do repo |

```text
eletiva / normal     →  {"label": "normal",  "confidence": 0.6954}
urgência / atenção   →  {"label": "atenção", "confidence": 0.7095}
emergência / urgente →  {"label": "urgente", "confidence": 0.598}
```

Comando da conferência: `python src/triage/predict.py`

---

## O que o Vini importa (API)

```python
from triage.predict import predict

# payload JSON da API: {"text": "<laudo>"}
result = predict(payload_text)
# {"label": "urgente", "confidence": 0.598}
```

Regras para a API:

1. Devolver exatamente `label` + `confidence`. Não acrescentar diagnóstico.
2. **Não** chamar `joblib.load` em todo POST — `predict` já carrega o Pipeline uma vez.
3. Texto vazio/`None`: a função levanta `ValueError` / `TypeError`; mapear para 4xx.
4. Arquivo ausente: `FileNotFoundError` — 503 ou similar, com a dica de rodar o treino.
5. Path HTTP (`POST /predict`, `/health`, `/metrics`) é **seu**. O JSON de negócio já está fechado.

O laudo que chegar na API deve parecer com o da Etapa 02 (diagnóstico + sexo + idade + labs), **sem** `Admission Type`.

---

## O que o Edu chama (DAG / CI)

A DAG não precisa reimplementar sklearn. Encadear, na venv 3.11.9, a partir da raiz:

```text
python src/triage/prepare_data.py
python src/triage/train.py
```

Isso **reescreve** `models/baseline.joblib`. Combinado: avisar Vini antes de retreinar em cima do artefato que a API já estiver usando.

Smoke opcional depois do treino:

```text
python src/triage/predict.py
```

Python do projeto: **3.11.9**. Dependências: `pyproject.toml` (`pandas`, `scikit-learn`, `joblib`).  
`pip install -e .` na `.venv` criada com esse interpretador.

---

## Como reproduzir o pacote inteiro (runbook local)

```powershell
# na raiz do repo
py -3.11 -m venv .venv
.\.venv\Scripts\Activate.ps1
python -m pip install -e .
python src/triage/prepare_data.py
python src/triage/train.py
python src/triage/predict.py
```

CSVs crus em `data/raw/` (já no repo deste recorte).

---

## Recado para colar no grupo

```text
Checkpoint Vítor A fechado (2026-08-15).

Path do modelo (não mudar sem avisar):
  models/baseline.joblib

Como classificar:
  from triage.predict import predict
  predict(texto) -> {"label": "...", "confidence": 0.91}

Labels: somente normal | atenção | urgente
JSON da API: {"text": "..."}  →  {"label", "confidence"}

Treino (Edu / DAG):
  python src/triage/prepare_data.py
  python src/triage/train.py
Python 3.11.9 + pip install -e .

Vini: pode ligar o POST no predict real.
Não retreinar por cima do joblib da API sem avisar.

Limitação: F1 macro no teste ≈ 0,48 (classe atenção tem 2 casos no recorte).
Accuracy ≈ 0,89 engana porque ~92% é urgente. Detalhes na etapa-03.md.
```

---

## Qualidade do modelo (o que o time deve citar)

Não vender o checkpoint como “modelo ótimo”.

| Número | Onde | Como falar |
|--------|------|------------|
| Accuracy teste **0,89** | Etapa 03 | chutar sempre `urgente` já acertaria ~89% |
| **F1 macro 0,48** | Etapa 03 | métrica do projeto; cada classe pesa igual |
| `atenção` F1 **0** no teste | Etapa 03 | 1 exemplo no teste; o modelo não generaliza essa classe |
| Três exemplos da Etapa 04 | demo | ilustração das labels, **não** nova avaliação |

O desafio pontua o **ciclo** (treino → artefato → API → retreino → latência), não um F1 de paper.

Isto **não** é diagnóstico médico.

---

## O que NÃO entra neste checkpoint

- FastAPI, Docker, Prometheus, Airflow, README cloud, vídeo
- ONNX / comparação de latência (Etapas 06–07, Semana C)
- Page de demo (backlog opcional; só consome a API quando ela existir)
- Mudança de path, labels ou JSON

---

## Impacto no sistema

| Pessoa | Pode fazer agora |
|--------|------------------|
| **Vini** | N2 — trocar mock por `predict` |
| **Edu** | DAG apontando para `prepare_data` + `train` no path combinado |
| **Fernando** | métricas em cima da API quando o Vini publicar `/metrics` |
| **Vítor** | Semana C = Etapas 06–07; não reabrir o joblib sem avisar |

---

## Estrutura entregue (trilha A)

```
src/triage/prepare_data.py
src/triage/train.py
src/triage/predict.py
data/processed/train.csv
data/processed/test.csv
models/baseline.joblib
docs/dataset.md
docs/etapas/Modelagem e otimização/etapa-01.md … etapa-05.md
```

---

## Critério de conclusão

- [x] Três checks do Checkpoint Vítor A
- [x] Recado com path + JSON
- [x] Time informado (este `.md` + quadro `docs/TODO.md`)

Próximo na **sua** lista: Etapa 06 (ONNX), só depois do time confirmar a técnica — e sem bloquear Vini/Edu.
