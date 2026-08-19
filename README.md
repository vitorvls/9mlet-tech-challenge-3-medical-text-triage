# Medical Text Triage

Classificador NLP **leve** de laudos em texto para apoio à triagem de urgência, no contexto do **Tech Challenge Fase 3 (FIAP — Machine Learning Engineering)**.

O serviço previsto pelo desafio lê um laudo, devolve `normal` / `atenção` / `urgente` e, nas próximas trilhas do time, será exposto via FastAPI, Docker, CI/CD, Airflow e monitoramento.

> **Isto não é um produto clínico.** Não substitui profissional de saúde, não emite diagnóstico e não recomenda conduta. O alvo do modelo é um *proxy* acadêmico (tipo de admissão hospitalar), não a gravidade real do paciente.

**Estado atual (2026-08-18):** Checkpoints **Vítor A** (modelo e dados), **Vini A** (API FastAPI, Dockerfile e baseline de latência) e **Fernando A** (Monitoramento com Prometheus, Grafana e Docker Compose) concluídos.

---

## Time

| Pessoa | Responsabilidade |
|--------|------------------|
| **Vítor** | Modelagem e otimização (esta fase) |
| **Vini** | API FastAPI + Docker + baseline de latência |
| **Fernando** | Prometheus, Grafana, Docker Compose (concluído) |
| **Edu** | GitHub Actions, Airflow, README cloud (expansão), vídeo STAR |

Quadro operacional: [`docs/TODO.md`](docs/TODO.md).

---

## O que já existe

```text
texto do laudo  →  FastAPI (/predict)  →  TF-IDF + LR  →  { label, confidence }
                          ↓
             Métricas Prometheus (/metrics)  →  Prometheus (:9090)  →  Grafana (:3000)
```

| Artefato | Caminho |
|----------|---------|
| Pacote Python / API | `src/triage/` (`api.py`, `predict.py`, `train.py`, `prepare_data.py`) |
| Dados crus (recorte Kaggle) | `data/raw/` |
| Treino / teste | `data/processed/train.csv`, `test.csv` |
| Modelo | `models/baseline.joblib` |
| Dockerfile | `Dockerfile` |
| Docker Compose | `docker-compose.yml` |
| Configuração Prometheus | `monitoring/prometheus/prometheus.yml` |
| Provisionamento Grafana | `monitoring/grafana/` (`datasource.yml`, `dashboards.yml`, `medical-triage-dashboard.json`) |
| Simulador de Tráfego | `scripts/simulate_traffic.py` |
| Contrato de inferência | `from triage.predict import predict` ou `POST /predict` |

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

---

## Como executar a solução

### Opção 1: Stack Completa com Docker Compose (Recomendado)

Sobe simultaneamente a **API de Triagem**, o **Prometheus** e o **Grafana** (com dashboards e datasources 100% pré-configurados):

```bash
# 1. Subir os containers em background
docker compose up -d --build

# 2. Gerar tráfego contínuo para popular os gráficos em tempo real (encerra com Ctrl+C)
python scripts/simulate_traffic.py

# 3. Acessar os serviços no navegador:
# - API Swagger Docs: http://localhost:8000/docs
# - Métricas Prometheus: http://localhost:8000/metrics
# - Servidor Prometheus: http://localhost:9090
# - Painéis Grafana: http://localhost:3000 (Acesso anônimo liberado / admin:admin)
```

Para parar os serviços:
```bash
docker compose down
```

### Opção 2: Localmente via Python

```powershell
py -3.11 -m venv .venv
.\.venv\Scripts\Activate.ps1
python -m pip install -e ".[dev]"

# Preparar dados e treinar modelo
python src/triage/prepare_data.py
python src/triage/train.py

# Iniciar servidor da API
uvicorn triage.api:app --reload --port 8000
```

Inferência via código Python:

```python
from triage.predict import predict

predict("Diagnosis: SEPSIS\nSex: F\nAge: 70")
# {"label": "urgente", "confidence": 0.58}
```

Inferência via HTTP `POST /predict`:

```bash
curl -X POST http://localhost:8000/predict \
  -H "Content-Type: application/json" \
  -d '{"text": "Diagnosis: SEPSIS\nSex: F\nAge: 70\nAbnormal lab results:\n- Lactate: 4.1 mmol/L (abnormal)"}'
```

---

## Estrutura do repositório

```text
src/triage/           # api.py, predict.py, train.py, prepare_data.py
data/raw/             # CSVs do Kaggle (recorte MIMIC-III)
data/processed/       # train.csv, test.csv
models/               # baseline.joblib
monitoring/           # prometheus/prometheus.yml, grafana/ (provisioning + dashboards)
evidencias/           # grafana_dashboard.json, baseline de latência
scripts/              # benchmark_latency.py, simulate_traffic.py
docs/                 # quadro do time (TODO.md), dataset.md, etapas de cada integrante
docker-compose.yml    # Orquestração API + Prometheus + Grafana
Dockerfile            # Build multi-stage da API FastAPI
pyproject.toml        # Dependências pinadas do projeto
```

---

## Próximos passos do time

1. **Edu** — Actions (≥ 2 automações), DAG (`prepare_data` → `train` → `models/baseline.joblib`), evidências, vídeo STAR.
2. **Vítor (Semana C)** — otimização de latência (proposta: ONNX) e tabela original vs otimizado.

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

Trilhas detalhadas:
- **Modelagem e Otimização (Vítor):** [`docs/etapas/Modelagem e otimização/`](docs/etapas/Modelagem%20e%20otimização/)
- **API e Docker (Vini):** [`docs/etapas/API e Docker/`](docs/etapas/API%20e%20Docker/)
- **Monitoramento (Fernando):** [`docs/etapas/Monitoramento/`](docs/etapas/Monitoramento/)
- **CI/CD, Airflow e Documentação (Edu):** [`docs/etapas/CI-CD Airflow e documentacao/`](docs/etapas/CI-CD%20Airflow%20e%20documentacao/)

### Documentação de Monitoramento (Fernando)

| Arquivo | Conteúdo |
|---------|----------|
| [etapa-01-instrumentacao-metricas.md](docs/etapas/Monitoramento/etapa-01-instrumentacao-metricas.md) | Instrumentação com `prometheus_client` (`/metrics`, contadores por classe/erro, histograma com buckets) |
| [etapa-02-prometheus.md](docs/etapas/Monitoramento/etapa-02-prometheus.md) | Configuração do servidor Prometheus para *scrape* a cada 5s |
| [etapa-03-docker-compose.md](docs/etapas/Monitoramento/etapa-03-docker-compose.md) | Orquestração da stack unificada (API + Prometheus + Grafana) no Compose |
| [etapa-04-grafana-dashboards.md](docs/etapas/Monitoramento/etapa-04-grafana-dashboards.md) | Provisionamento automático de DataSource e Dashboards no Grafana (8 painéis em tempo real) |
