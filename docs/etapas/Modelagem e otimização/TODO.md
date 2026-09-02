# TODO linear — Modelagem e otimização (Vítor)

Executar **de cima para baixo**. Não iniciar uma etapa sem a anterior concluída (código + `etapa-NN.md`).

Contratos já fechados: `docs/TODO.md` §0.2 e `docs/dataset.md`.  
Regra de documentação: `docs/etapas/README.md`.

Legenda: `[ ]` pendente · `[x]` feita **e** documentada.

---

## Fase A — Baseline (desbloqueia Vini e Edu)

- [x] **Etapa 01 — Esqueleto da trilha do modelo**
  - **Objetivo:** Gavetas combinadas no repo (`src/triage`, `data/processed`, `models`, `docs/dataset.md`) para ninguém gravar artefato no lugar errado.
  - **Pré-requisitos:** decisões §0.2 (path `models/baseline.joblib`, labels, dataset).
  - **Implementação:** pastas + `__init__.py` + `.gitkeep` + nota do recorte. Sem treino ainda.
  - **Conclusão:** estrutura existe; `docs/dataset.md` descreve o recorte.
  - **Documento:** [`etapa-01.md`](etapa-01.md)

- [x] **Etapa 02 — Montar o CSV de treino (`prepare_data`)**
  - **Objetivo:** Transformar as 4 tabelas MIMIC em `text,label` para as **129** internações, sem vazamento do rótulo.
  - **Pré-requisitos:** Etapa 01; CSVs em `data/raw/`.
  - **Implementação:** `src/triage/prepare_data.py` — laudo simulado (diagnóstico + sexo/idade + labs anormais); mapear `admission_type`; **não** usar `structured_medical_records.csv` como único treino; split por `hadm_id`; gravar `data/processed/train.csv` e `test.csv`.
  - **Conclusão:** os dois CSVs existem (102 / 27); texto sem `Admission Type`; três labels nos dois lados (`atenção` = 1+1); comando: `python src/triage/prepare_data.py` na venv 3.11.9.
  - **Documento:** [`etapa-02.md`](etapa-02.md)

- [x] **Etapa 03 — Treinar o baseline sklearn**
  - **Objetivo:** Ensinar TF-IDF + Logistic Regression e salvar **um** Pipeline em `models/baseline.joblib`.
  - **Pré-requisitos:** Etapa 02 (`train.csv` / `test.csv`).
  - **Implementação:** `src/triage/train.py` — `TfidfVectorizer` + `LogisticRegression(class_weight="balanced")`; joblib; imprimir F1 macro, accuracy e matriz de confusão.
  - **Conclusão:** `models/baseline.joblib` gerado (`python src/triage/train.py`); teste accuracy=0,8889 / F1 macro=0,4796 (números explicados no `.md`).
  - **Documento:** [`etapa-03.md`](etapa-03.md)

- [x] **Etapa 04 — Função `predict` para a API e a DAG**
  - **Objetivo:** Contrato Vítor → Vini/Edu: texto entra, `{label, confidence}` sai.
  - **Pré-requisitos:** Etapa 03 (`baseline.joblib`).
  - **Implementação:** `src/triage/predict.py` — carregar o Pipeline **uma vez**; `predict(text: str) -> dict`; labels só `normal` | `atenção` | `urgente`; erro claro se o arquivo do modelo faltar.
  - **Conclusão:** três exemplos (`normal` 0,6954 / `atenção` 0,7095 / `urgente` 0,5980); `python src/triage/predict.py`.
  - **Documento:** [`etapa-04.md`](etapa-04.md)

- [x] **Etapa 05 — Checkpoint Vítor A (entrega da trilha A)**
  - **Objetivo:** Fechar o pacote que o time usa: treina, salva, prevê, path estável.
  - **Pré-requisitos:** Etapas 02–04.
  - **Implementação:** conferir os três critérios do `docs/TODO.md` (Checkpoint Vítor A); recado ao grupo com path e JSON; **não** mudar `models/baseline.joblib` sem avisar.
  - **Conclusão:** CA-Vítor marcado; recado em [`etapa-05.md`](etapa-05.md).
  - **Documento:** [`etapa-05.md`](etapa-05.md)

---

## Fase B — Otimização de latência (Etapa 4 da FIAP / Semana C)

Não começar antes do Checkpoint Vítor A, salvo justificativa técnica no `.md`.

- [x] **Etapa 06 — Exportar modelo otimizado (proposta: ONNX)**
  - **Objetivo:** Pelo menos uma técnica de latência vista no curso; ONNX implementado com `skl2onnx` e `onnxruntime`.
  - **Pré-requisitos:** Etapa 05.
  - **Implementação:** artefato otimizado (`models/baseline.onnx`) + módulo `src/models/onnx_export.py` e script de benchmark `scripts/benchmark_latency_onnx.py`.
  - **Conclusão:** arquivo `models/baseline.onnx` gerado; função `predict_onnx` e testes em `tests/test_model.py`.
  - **Documento:** `etapa-06.md`

- [x] **Etapa 07 — Comparar latência original vs otimizado**
  - **Objetivo:** Números que entram no README e no vídeo STAR.
  - **Pré-requisitos:** Etapa 06.
  - **Implementação:** 1.000 amostras comparando scikit-learn vs ONNX Runtime via `scripts/benchmark_latency.py`.
  - **Conclusão:** Sklearn 0,236 s vs ONNX 0,154 s (~34,7% mais rápido / 1.53x speedup), registrado no `README.md`.
  - **Documento:** `etapa-07.md`

---

## Fora desta lista (não é sua etapa)

API FastAPI, Dockerfile, Prometheus, Grafana, GitHub Actions, DAG Airflow, README cloud, vídeo — pastas dos colegas em `docs/etapas/`.

Page de demo (formulário + chat): **extra opcional** no `docs/TODO.md` (backlog). Não faz parte desta lista linear. Se o time fizer, não altera `prepare_data` / `train` / `predict` / `baseline.joblib`.
