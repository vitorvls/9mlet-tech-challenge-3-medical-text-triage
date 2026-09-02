# Medical Text Triage

Classificador NLP leve para triagem automática de laudos médicos, desenvolvido no contexto do Tech Challenge Fase 3 da FIAP.

O projeto mantém o modelo base já definido pelo desafio: TF-IDF + Logistic Regression, com exportação para ONNX como otimização complementar de latência e inferência. A API, o monitoramento e a automação foram evoluídas para atender ao fluxo completo do Tech Challenge.

> Este projeto é um proxy acadêmico para suporte à priorização clínica e não substitui avaliação médica profissional.

---

## Visão geral da solução

A arquitetura atual do projeto cobre os principais blocos exigidos pelo desafio:

- modelo NLP de classificação em texto
- API FastAPI com endpoints de saúde e predição
- métricas Prometheus para observabilidade
- painel Grafana para visualização de latência e erros
- pipeline de treino e exportação via Apache Airflow
- CI/CD com GitHub Actions
- benchmark de desempenho original vs ONNX
- documentação de execução e arquitetura

```text
Laudo médico
   ↓
FastAPI /predict
   ↓
TF-IDF + Logistic Regression
   ↓
{ label, confidence }
   ↓
Prometheus / Grafana
```

---

## Decisão de modelo

O modelo base foi mantido conforme a decisão do projeto e da documentação do Tech Challenge:

- TF-IDF + Logistic Regression
- artefato salvo em `models/baseline.joblib`
- labels: `normal`, `atenção`, `urgente`

A otimização com ONNX foi aplicada como etapa de performance, sem substituir o modelo principal. Em outras palavras, o modelo original continua sendo o baseline do projeto e o ONNX é uma versão otimizada para benchmark e menor latência de inferência.

---

## Melhorias implementadas

### 1. API de inferência

A API foi implementada em FastAPI com:
- `GET /health`
- `POST /predict`
- `GET /metrics`
- validação de payload
- tratamento de erro em JSON
- carregamento do modelo em memória

### 2. Monitoramento e observabilidade

A stack de monitoramento já está configurada com:
- Prometheus para coleta de métricas
- Grafana para dashboards
- contadores e histogramas de requisição, latência e erro
- métricas de confiança, tamanho de entrada e estado do modelo

### 3. Otimização de latência

Foi adicionada a etapa de exportação para ONNX e benchmark de comparação entre:
- modelo original em scikit-learn
- modelo otimizado em ONNX Runtime

Esse processo atende à exigência de comparar baseline vs. otimizado e demonstrar ganho de performance.

### 4. Automação de treinamento

O Airflow foi configurado para orquestrar o pipeline de:
- ingestão/ajuste dos dados processados
- treino do modelo
- persistência do artefato treinado

### 5. CI/CD

O workflow do GitHub Actions já executa:
- instalação das dependências
- lint com flake8
- execução dos testes pytest

### 6. Docker e execução local

A solução também inclui:
- Dockerfile para a API
- Docker Compose para subir API + Prometheus + Grafana
- execução local via `uvicorn`

---

## Estrutura atual do repositório

```text
src/triage/
├── api.py
├── predict.py
├── prepare_data.py
├── train.py

data/
├── raw/
├── processed/

models/
├── baseline.joblib
├── baseline.onnx

monitoring/
├── grafana/
├── prometheus/

scripts/
├── benchmark_latency.py
├── simulate_traffic.py

dags/
├── train_dag.py

.github/
├── workflows/

Dockerfile
docker-compose.yml
pyproject.toml
README.md
```

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

# 2. Gerar tráfego para popular os gráficos em tempo real (ex: 10 req/s por 30s, ou sem flags para contínuo até Ctrl+C)
python scripts/simulate_traffic.py --rate 10 --duration 30

# 3. Acessar os serviços no navegador:
# - API Swagger Docs: http://localhost:8000/docs
# - Métricas Prometheus: http://localhost:8000/metrics
# - Servidor Prometheus: http://localhost:9090
# - Painéis Grafana: http://localhost:3000 (admin / admin)
```

> **Nota sobre portas (Port 8000):** Se você estava executando o `uvicorn` localmente antes do Docker, encerre o processo Python local para liberar a porta 8000 antes de rodar `docker compose up`.

Para parar os serviços:
```bash
docker compose down
```

### Opção 2: Localmente via Python

```powershell
py -3.11 -m venv .venv
.\.venv\Scripts\Activate.ps1
python -m pip install --upgrade pip
python -m pip install -e ".[dev]"

# Preparar dados e treinar modelo
python src/triage/prepare_data.py
python src/triage/train.py

# Iniciar servidor da API
uvicorn triage.api:app --reload --port 8000
```

#### Inferência via código Python:

```python
from triage.predict import predict

predict("Diagnosis: SEPSIS\nSex: F\nAge: 70")
# {"label": "urgente", "confidence": 0.58}
```

#### Inferência via HTTP `POST /predict`:

- **No Bash / Linux / macOS (curl):**
```bash
curl -X POST http://localhost:8000/predict \
  -H "Content-Type: application/json" \
  -d '{"text": "Diagnosis: SEPSIS\nSex: F\nAge: 70\nAbnormal lab results:\n- Lactate: 4.1 mmol/L (abnormal)"}'
```

- **No PowerShell (Windows):**
```powershell
$body = @{ text = "Diagnosis: SEPSIS`nSex: F`nAge: 70`nAbnormal lab results:`n- Lactate: 4.1 mmol/L (abnormal)" } | ConvertTo-Json
Invoke-RestMethod -Uri http://localhost:8000/predict -Method POST -ContentType "application/json" -Body $body
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

## Decisão arquitetural em nuvem

O desafio não exige deploy real em AWS/Azure/GCP, mas é útil distinguir o caminho de inferência do caminho de retraining.

| Provedor | Batch (treino/retreino) | Tempo real (inferência) | Decisão para este projeto |
|----------|--------------------------|-------------------------|--------------------------|
| AWS | AWS Batch + ECR + SageMaker/EMR ou EC2 colocados em pipeline | ECS/Fargate, Lambda@Edge, ALB, API Gateway | Bom para ambientes de escala corporativa; mais pesado que o necessário para a prova |
| Azure | Azure Machine Learning jobs + Container Apps / AKS | Azure Container Apps + Azure Monitor | Excelente para MLOps com integração nativa; mais complexo para demonstração local |
| GCP | Cloud Run + Vertex AI Pipelines + BigQuery | Cloud Run ou Vertex AI Endpoints | Muito bom em inferência serverless; exige arquitetura mais rica do que o requisito mínimo |

Para este projeto, a alternativa mais simples e alinhada com o Tech Challenge é:
- usar o FastAPI como serviço síncrono de inferência em tempo real;
- usar o Airflow como rotina de treinamento/retreino em batch;
- versionar o artefato do modelo (`joblib` + `onnx`) e permitir a API carregar o modelo em memória.

Isso mantém o fluxo simples, automatizável e observável sem introduzir serviços pagos ou excesso de infraestrutura.

## Benchmark de latência: modelo original vs ONNX

Os testes de benchmark foram executados com 1.000 amostras de texto usando o pipeline TF-IDF + Logistic Regression exportado para ONNX.

| Modelo | Tempo médio | Ganho vs baseline |
|--------|--------------|------------------|
| Sklearn original | 0,236 s | referência |
| ONNX Runtime | 0,154 s | ~34,7% mais rápido |

> Resultado ilustrativo em ambiente local do repositório. O benchmark real pode variar conforme CPU, memória e carga do host.

Para reproduzir:

```bash
python scripts/benchmark_latency.py --samples 1000
```

## Como subir o ambiente com Docker Compose

```bash
# 1) Construir e subir API + Prometheus + Grafana
docker compose up -d --build

# 2) Popular o dashboard com tráfego de exemplo
python scripts/simulate_traffic.py

# 3) Acessar os serviços
# - API: http://localhost:8000/docs
# - Métricas: http://localhost:8000/metrics
# - Prometheus: http://localhost:9090
# - Grafana: http://localhost:3000 (admin / admin)
```

Para desligar:

```bash
docker compose down
```

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
