# Medical Text Triage

Classificador NLP **leve** de laudos em texto para apoio à triagem de urgência, no contexto do **Tech Challenge Fase 3 (FIAP — Machine Learning Engineering)**.

O serviço previsto pelo desafio lê um laudo, devolve `normal` / `atenção` / `urgente` e, nas próximas trilhas do time, será exposto via FastAPI, Docker, CI/CD, Airflow e monitoramento.

> **Isto não é um produto clínico.** Não substitui profissional de saúde, não emite diagnóstico e não recomenda conduta. O alvo do modelo é um *proxy* acadêmico (tipo de admissão hospitalar), não a gravidade real do paciente.

**Estado atual (2026-08-15):** Checkpoint **Vítor A** fechado — dataset processado, modelo treinado, função `predict` pronta. API, Docker, Airflow, CI e Grafana ainda são das outras pessoas do time.

---

## Time

| Pessoa | Responsabilidade |
|--------|------------------|
| **Vítor** | Modelagem e otimização (esta fase) |
| **Vini** | API FastAPI + Docker + baseline de latência |
| **Fernando** | Prometheus, Grafana, Docker Compose |
| **Edu** | GitHub Actions, Airflow, README cloud (expansão), vídeo STAR |

Quadro operacional: [`docs/TODO.md`](docs/TODO.md).

---

## O que já existe

```text
texto do laudo  →  TF-IDF + Logistic Regression  →  { label, confidence }
```

| Artefato | Caminho |
|----------|---------|
| Pacote Python | `src/triage/` |
| Dados crus (recorte Kaggle) | `data/raw/` |
| Treino / teste | `data/processed/train.csv`, `test.csv` |
| Modelo | `models/baseline.joblib` |
| Contrato de inferência | `from triage.predict import predict` |

**Labels**

| Origem (`admission_type`) | Saída do modelo |
|---------------------------|-----------------|
| `ELECTIVE` | `normal` |
| `URGENT` | `atenção` |
| `EMERGENCY` | `urgente` |

**Dataset:** [MIMIC-III Clinical Database (Open Access)](https://www.kaggle.com/datasets/ihssanened/mimic-iii-clinical-databaseopen-access) — demo pública (~100 pacientes, 129 internações), não o MIMIC completo. Detalhes em [`docs/dataset.md`](docs/dataset.md).

---

## Qualidade do baseline (teste, n = 27)

Métrica principal do projeto: **F1 macro** (as três classes pesam igual). Accuracy sozinha mente neste recorte (~92% das internações são `EMERGENCY`).

| Métrica | Treino (102) | **Teste (27)** |
|---------|--------------|----------------|
| Accuracy | 1,00 | **0,89** |
| F1 macro | 1,00 | **0,48** |
| F1 `urgente` | 1,00 | 0,94 |
| F1 `normal` | 1,00 | 0,50 |
| F1 `atenção` | 1,00 | 0,00 |

Treino perfeito + teste mediano = o modelo memoriza o conjunto pequeno. A classe `atenção` tem só **2** internações no recorte; o baseline enviesa para `urgente`. Interpretação didática: [`docs/etapas/Modelagem e otimização/etapa-03.md`](docs/etapas/Modelagem%20e%20otimização/etapa-03.md).

`confidence` é a probabilidade da classe escolhida (`predict_proba`). **Não** está calibrada e **não** é certeza clínica.

---

## Requisitos

- **Python 3.11.9** (pin em `pyproject.toml` e `.python-version`)
- CSVs em `data/raw/` (já versionados neste recorte de trabalho)
- Windows (PowerShell) ou equivalente Unix

---

## Como executar (trilha do modelo)

Na raiz do repositório:

```powershell
py -3.11 -m venv .venv
.\.venv\Scripts\Activate.ps1
python -m pip install -e .

python src/triage/prepare_data.py
python src/triage/train.py
python src/triage/predict.py
```

Inferência em código:

```python
from triage.predict import predict

predict("Diagnosis: SEPSIS\nSex: F\nAge: 70")
# {"label": "urgente", "confidence": 0.58}
```

Um laudo deve seguir o formato montado no prepare (diagnóstico + sexo + idade + labs anormais), **sem** `Admission Type`, identificadores ou marcador `/SDA`.

JSON que a API deve espelhar (path HTTP ainda com o Vini; sugestão `POST /predict`):

```json
{ "text": "texto do laudo médico aqui" }
```

```json
{ "label": "urgente", "confidence": 0.91 }
```

---

## Estrutura do repositório

```text
src/triage/           prepare_data.py, train.py, predict.py
data/raw/             CSVs do Kaggle (recorte)
data/processed/       train.csv, test.csv
models/               baseline.joblib
docs/                 quadro do time, dataset, etapas
pyproject.toml        dependências pinadas (pandas, scikit-learn, joblib)
```

Ainda **não** fazem parte desta fase: FastAPI, Dockerfile, Compose, DAG Airflow, GitHub Actions.

---

## Próximos passos do time

1. **Vini** — FastAPI carregando `predict`; Docker; baseline de latência.
2. **Fernando** — `prometheus_client`, Prometheus, Grafana (≥ 3 painéis), Compose.
3. **Edu** — Actions (≥ 2 automações), DAG (`prepare_data` → `train` → `models/baseline.joblib`), evidências, vídeo STAR.
4. **Vítor (Semana C)** — otimização de latência (proposta: ONNX) e tabela original vs otimizado.

Path do modelo **não muda** sem avisar Vini e Edu: `models/baseline.joblib`.

Page de demo (formulário + conversa) é **extra opcional**, só se sobrar tempo, e só consome a API já existente. Ver backlog em `docs/TODO.md`.

---

## Estratégia em nuvem (documental)

O desafio **não exige** deploy real em AWS/Azure/GCP. Abaixo está o enquadramento teórico; o Edu pode expandir no fechamento.

| Modo | Quando faria sentido | Neste projeto |
|------|----------------------|---------------|
| **Tempo real** | Laudo chega e a classificação precisa voltar na hora (API síncrona) | Caminho natural da inferência: FastAPI + modelo em memória |
| **Batch** | Retreino periódico, reprocessar um lote de laudos, jobs noturnos | Caminho natural do Airflow: carregar dados → treinar → salvar o joblib |

Na nuvem, a analogia seria: serviço de inferência sempre ligado (tempo real) + job agendado de treino (batch), com o artefato do modelo versionado e carregado pela API. A demonstração avaliável do desafio continua **local** (Docker / Compose), não um cluster pago.

---

## Dados e licença

Uso acadêmico do Tech Challenge. Recorte público da demo MIMIC-III (Kaggle). Não é dado clínico próprio. A demo PhysioNet correspondente usa ODbL. Não redistribuir o MIMIC completo (exige credencial).

---

# Para estudo

Esta seção é para **colegas de classe** (e para o próprio time) entenderem *onde está escrito o raciocínio*, não só o código.

## Para que serve a pasta `docs/`

`docs/` é a trilha de aprendizado do repositório. Código sem o `.md` da etapa **não** conta como etapa concluída.

| Caminho | O que é |
|---------|---------|
| [`docs/TODO.md`](docs/TODO.md) | Quadro do **time inteiro**: papéis, contratos, checkpoints, backlog opcional |
| [`docs/dataset.md`](docs/dataset.md) | Recorte MIMIC, labels, split, vazamento, limitações |
| [`docs/dataset_doc/`](docs/dataset_doc/) | Dicionário das tabelas (`admissions`, `patients`, `labevents`, `d_labitems`) |
| [`docs/etapas/`](docs/etapas/) | Uma pasta **por integrante**; cada passo vira `etapa-01.md`, `etapa-02.md`, … |
| [`docs/etapas/README.md`](docs/etapas/README.md) | Mapa das quatro trilhas |

Trilhas:

```text
docs/etapas/
├── Modelagem e otimização/          ← Vítor (feita até a etapa 05)
├── API e Docker/                    ← Vini
├── Monitoramento/                   ← Fernando
└── CI-CD Airflow e documentacao/    ← Edu
```

Cada `etapa-NN.md` explica objetivo, problema, o que foi implementado, por que aquela lib/abordagem, o que foi descartado, fluxo dos dados e limitações. Em modelagem, as métricas vêm **explicadas em linguagem simples**, não só o número.

## Documentação da modelagem (ler nesta ordem)

Lista linear: [`docs/etapas/Modelagem e otimização/TODO.md`](docs/etapas/Modelagem%20e%20otimização/TODO.md).

| Arquivo | Conteúdo |
|---------|----------|
| [etapa-01.md](docs/etapas/Modelagem%20e%20otimização/etapa-01.md) | Esqueleto: pastas `src/triage`, `data/processed`, `models` |
| [etapa-02.md](docs/etapas/Modelagem%20e%20otimização/etapa-02.md) | Como 4 tabelas viram `text,label`; anti-vazamento (`/SDA`, tipo de admissão); split 102/27 |
| [etapa-03.md](docs/etapas/Modelagem%20e%20otimização/etapa-03.md) | TF-IDF + LR; por que não Random Forest; accuracy vs F1 macro; matriz de confusão |
| [etapa-04.md](docs/etapas/Modelagem%20e%20otimização/etapa-04.md) | `predict(text) → {label, confidence}`; o que é confidence; 3 exemplos |
| [etapa-05.md](docs/etapas/Modelagem%20e%20otimização/etapa-05.md) | Checkpoint A: recado ao Vini/Edu, runbook, congelar o path do joblib |
| etapa-06 / 07 | Ainda não: otimização de latência (Semana C) |

## Resumo do que foi feito nesta fase (2026-08-15)

Fase de **modelagem baseline** (Checkpoint Vítor A). Não incluímos API, Docker nem Airflow.

1. **Regras de documentação** para o repositório inteiro (cada integrante documenta a própria pasta em `docs/etapas/`).
2. **Python 3.11.9**, `pyproject.toml` (pandas 2.3.3, scikit-learn 1.9.0, joblib 1.5.3) e venv em `.venv/`.
3. **Etapa 01** — Gavetas do modelo no repo.
4. **Etapa 02** — `prepare_data.py`: 129 internações → laudo simulado (diagnóstico + sexo + idade + até 20 labs anormais). **Não** usamos `structured_medical_records.csv` como treino (só 9 internamentos, todos emergência, vazava `Admission Type`). Removemos `/SDA` (marcador quase só das eletivas). Split por `hadm_id`: 102 treino / 27 teste, as três labels nos dois lados.
5. **Etapa 03** — Pipeline sklearn `TfidfVectorizer` + `LogisticRegression(class_weight="balanced")` salvo em `models/baseline.joblib`. Teste: accuracy 0,89 (enganosa) e **F1 macro 0,48**. Classe `atenção` não generaliza (2 casos no recorte).
6. **Etapa 04** — `predict` carrega o Pipeline uma vez; texto vazio dá erro; três exemplos documentados (`normal`, `atenção`, `urgente`).
7. **Etapa 05** — Pacote entregue ao time: Vini importa `from triage.predict import predict`; Edu encadeia `prepare_data.py` → `train.py` no mesmo path.
8. **Contratos fechados:** labels, JSON in/out, path do artefato, algoritmo da Fase 1. ONNX continua **proposta** para a Semana C.
9. **Extra local (não vai no Git):** pasta `testes_local/` com 100 laudos **inventados** e um relatório esperado vs previsto — só para estudo do viés do modelo (`urgente` demais). Está no `.gitignore`.
10. **Page form+chat** ficou no backlog opcional do `docs/TODO.md`: só se sobrar tempo, sem alterar este modelo.

Quem for implementar a API: não retreine por cima de `models/baseline.joblib` sem avisar. Quem for estudar o modelo: comece pela etapa-02 (dados) e etapa-03 (métricas).
