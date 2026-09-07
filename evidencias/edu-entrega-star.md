# Evidências da entrega do Edu

**Data de conferência:** 2026-09-07

## Evidências técnicas

| Entrega | Arquivo ou comando |
|---|---|
| CI/CD | `.github/workflows/ci.yml` |
| Documentação do CI | `docs/etapas/CI-CD Airflow e documentacao/etapa-01.md` |
| DAG | `dags/train_dag.py` |
| Documentação do Airflow | `docs/etapas/CI-CD Airflow e documentacao/etapa-02.md` |
| Preparação dos dados | `python src/triage/prepare_data.py` |
| Treino e artefato | `python src/triage/train.py` -> `models/baseline.joblib` |
| Testes | `python -m pytest -q` |
| Lint | `python -m flake8 src tests` |
| Build | `docker build --tag medical-text-triage:local .` |

## Roteiro do vídeo STAR (até 5 minutos)

## Prompt pronto para uma IA de vídeo

Copie o texto abaixo em uma ferramenta de edição assistida por IA. Anexe, como
materiais, o README, `dags/train_dag.py`, `.github/workflows/ci.yml`,
`evidencias/grafana_dashboard.json` e `evidencias/latency_baseline_summary.csv`.

```text
Crie um vídeo técnico em português do Brasil, com duração entre 4 e 5 minutos,
no formato STAR: Situation, Task, Action e Result. Use estilo profissional,
claro e objetivo, com gravação de tela do repositório e dos comandos. Não use
avatar médico, imagens de hospital ou efeitos dramáticos. O sistema é um
protótipo acadêmico e não faz diagnóstico médico.

Título inicial: "Medical Text Triage — Deploy, CI/CD, Airflow e otimização"

Cena 1 — Situation, 0:00–0:40:
Mostrar o título e a arquitetura simples. Narrar que o projeto classifica
laudos médicos em normal, atenção ou urgente, e que o desafio era demonstrar
um ciclo completo e reproduzível, não apenas treinar um modelo. Exibir a
ressalva: "Protótipo acadêmico; não substitui avaliação médica profissional."

Cena 2 — Task, 0:40–1:15:
Mostrar o PDF ou o README com os requisitos. Narrar que a equipe precisava de
API FastAPI em Docker, CI/CD com pelo menos duas automações, DAG Airflow,
monitoramento com Prometheus e Grafana e comparação de latência antes e depois
da otimização.

Cena 3 — Action: modelo e API, 1:15–2:00:
Mostrar `src/triage/train.py`, `src/triage/predict.py`, `models/baseline.joblib`
e `src/triage/api.py`. Explicar que o baseline usa TF-IDF e Logistic Regression,
que a API recebe texto em `POST /predict` e retorna label e confidence. Mostrar
brevemente `/health` e `/metrics`.

Cena 4 — Action: CI/CD e Airflow, 2:00–2:50:
Mostrar `.github/workflows/ci.yml`. Destacar lint com Flake8, testes com Pytest
e build Docker dependente do job de validação. Em seguida mostrar
`dags/train_dag.py` e a sequência `ingest_data >> train_and_export_model`.
Explicar que o fluxo prepara os CSVs, treina e salva `models/baseline.joblib`.

Cena 5 — Action: monitoramento e otimização, 2:50–3:40:
Mostrar `docker-compose.yml`, o dashboard Grafana e os artefatos ONNX.
Explicar que a stack reúne API, Prometheus e Grafana, com painéis de chamadas,
latência e erros. Mostrar a tabela do README comparando o modelo Sklearn
original com ONNX Runtime.

Cena 6 — Result, 3:40–4:30:
Mostrar os resultados documentados: 14 testes aprovados na validação local,
baseline Sklearn de 0,236 s por amostra e ONNX Runtime de 0,154 s por amostra,
com redução aproximada de 34,7% no benchmark registrado. Não afirmar que o
workflow remoto passou se não houver um run do GitHub anexado.

Cena 7 — Fechamento, 4:30–4:50:
Narrar que o resultado é um ciclo organizado de dados, treino, API,
observabilidade e otimização. A principal lição foi reutilizar os mesmos
scripts de preparação e treino na execução local e na DAG, reduzindo divergência.
Encerrar com: "O projeto apoia a priorização técnica; a decisão clínica continua
com profissionais de saúde."

Use cortes suaves, fonte legível, legendas em português e zoom apenas nas linhas
importantes. Não invente métricas, telas, nomes de serviços ou resultados que
não estejam nos arquivos anexados.
```

## Roteiro detalhado para gravação

### Cena 1 — Situation (0:00–0:40)

**Mostrar:** título do projeto e o diagrama de arquitetura no README.

**Fala:**

> Este projeto foi desenvolvido para o Tech Challenge da FIAP e apresenta uma solução de triagem automática de laudos médicos em formato de texto.
>
> O sistema classifica o texto em três categorias: normal, atenção ou urgente.
>
> O objetivo não foi apenas treinar um modelo, mas demonstrar todo o ciclo de uma solução de machine learning: preparação dos dados, treinamento, API, monitoramento, automação e otimização de latência.
>
> Este é um protótipo acadêmico. Ele não realiza diagnóstico médico e não substitui a avaliação de profissionais de saúde.

**Texto na tela:** `Protótipo acadêmico — não substitui avaliação médica profissional`.

### Cena 2 — Task (0:40–1:15)

**Mostrar:** PDF do desafio ou requisitos do README, destacando FastAPI, Docker, GitHub Actions, Airflow, Prometheus, Grafana e otimização.

**Fala:**

> Os requisitos do desafio envolviam criar uma API para classificação de textos médicos, empacotar essa API em Docker e construir um pipeline automatizado.
>
> Também era necessário criar um workflow no GitHub Actions com pelo menos duas automações, desenvolver uma DAG no Airflow para o processo de treino, configurar monitoramento com Prometheus e Grafana e comparar a latência do modelo original com uma versão otimizada.
>
> A equipe organizou o projeto para que cada parte pudesse ser executada e validada separadamente, mantendo o mesmo contrato entre o treinamento, a API e o modelo salvo.

### Cena 3 — Action: modelo e API (1:15–2:00)

**Mostrar:** `src/triage/train.py`, `src/triage/predict.py`, `models/baseline.joblib`, `src/triage/api.py` e o Swagger em `/docs`.

**Executar:** uma requisição para `POST /predict`, mostrando também `/health` e `/metrics`.

**Fala:**

> O modelo baseline utiliza TF-IDF para transformar o texto em características numéricas e Logistic Regression para realizar a classificação.
>
> O pipeline completo é treinado no arquivo `train.py` e salvo em um único artefato chamado `models/baseline.joblib`.
>
> Esse arquivo contém o vetor TF-IDF e o classificador, permitindo que a API carregue o modelo sem reconstruí-lo a cada requisição.
>
> A função `predict` recebe um texto e retorna a classificação e a confiança da previsão.
>
> A API foi construída com FastAPI. O endpoint principal é o `POST /predict`, que recebe um JSON com o campo `text` e retorna `label` e `confidence`.

### Cena 4 — Action: CI/CD e Airflow (2:00–2:50)

**Mostrar:** `.github/workflows/ci.yml`, `dags/train_dag.py`, o terminal e a pasta `models`.

**Executar no terminal:**

```powershell
python src/triage/prepare_data.py
python src/triage/train.py
```

**Destacar no código:**

```python
ingest_task >> train_task
```

**Fala:**

> Para automatizar a qualidade do código, foi criado um workflow no GitHub Actions.
>
> O primeiro job instala as dependências, executa o Flake8 e roda os testes com Pytest. Depois dessas validações, o segundo job executa o build da imagem Docker.
>
> Para o treinamento, a DAG do Airflow possui duas tarefas principais. A primeira prepara os dados e gera os arquivos processados de treino e teste. A segunda executa o treinamento e salva o modelo em `models/baseline.joblib`.
>
> A dependência é explícita: primeiro acontece a preparação dos dados e depois o treinamento.

**Nota:** se não houver log real do Airflow, diga que a DAG foi carregada e validada localmente, sem afirmar uma execução remota.

### Cena 5 — Action: monitoramento e otimização (2:50–3:40)

**Mostrar:** `docker-compose.yml`, configuração do Prometheus, dashboard Grafana, `models/baseline.onnx` e a tabela de latência do README.

**Fala:**

> A stack de observabilidade é executada com Docker Compose e reúne a API, o Prometheus e o Grafana.
>
> A API expõe métricas de contagem de requisições, duração das requisições e erros. O Prometheus coleta essas métricas e o Grafana apresenta os dados em dashboards, incluindo chamadas, latência e erros.
>
> Além do modelo baseline em Scikit-learn, foi gerada uma versão otimizada em ONNX Runtime para comparar o tempo de inferência.

### Cena 6 — Result (3:40–4:30)

**Mostrar:** resultado real do Pytest, tabela de benchmark, arquivos em `evidencias/`, modelo salvo e dashboard Grafana.

**Fala:**

> Como resultado, o projeto passou a ter um fluxo completo de preparação, treinamento, inferência, monitoramento e otimização.
>
> Na validação local, a suíte apresentou 14 testes aprovados.
>
> No benchmark registrado, o modelo original em Scikit-learn apresentou tempo médio de 0,236 segundos por amostra. A versão executada com ONNX Runtime apresentou 0,154 segundos por amostra.
>
> Isso representa uma redução aproximada de 34,7% no tempo médio observado nesse benchmark.
>
> O projeto também possui evidências versionadas do dashboard, dos benchmarks e da documentação do Airflow.

**Mostrar no terminal:** `14 passed`. Não simular esse resultado.

### Cena 7 — Fechamento (4:30–4:50)

**Mostrar:** arquitetura final ou estrutura de pastas do projeto.

**Fala:**

> O resultado final é um ciclo organizado de dados, treinamento, API, observabilidade e otimização.
>
> A principal lição foi reutilizar os mesmos scripts de preparação e treinamento na execução local e na DAG do Airflow. Isso reduz a diferença entre o que é testado manualmente e o que será executado no pipeline automatizado.
>
> O projeto apoia a priorização técnica de textos médicos, mas a decisão clínica continua sendo responsabilidade dos profissionais de saúde.

**Tela final:** `Medical Text Triage — FastAPI | GitHub Actions | Airflow | Prometheus + Grafana | ONNX Runtime`.

