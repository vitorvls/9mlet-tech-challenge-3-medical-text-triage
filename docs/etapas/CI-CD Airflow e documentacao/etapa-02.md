# Etapa 02 — DAG de treino no Airflow

**Trilha:** CI-CD, Airflow e documentação (Edu)  
**Status:** concluída  
**Data:** 2026-09-07

## Objetivo

Orquestrar o retreino com o mesmo contrato usado localmente pela equipe: preparar os CSVs processados, treinar o pipeline NLP e salvar o artefato no caminho consumido pela API.

## Fluxo implementado

O arquivo `dags/train_dag.py` define a DAG `medical_text_triage_training` com duas tarefas Python:

```text
ingest_data (prepare_data.main)
        |
        v
train_and_export_model (train.main)
        |
        v
models/baseline.joblib
```

`ingest_data` lê `data/raw/` e grava `data/processed/train.csv` e `data/processed/test.csv`. `train_and_export_model` lê esses arquivos e grava `models/baseline.joblib`, mantendo o contrato do módulo `triage.predict` e da API.

## Reprodução local do mesmo contrato

```powershell
python src/triage/prepare_data.py
python src/triage/train.py
```

Para carregar a DAG no Airflow, instalar as dependências de desenvolvimento e configurar o projeto no `PYTHONPATH` conforme o ambiente local. A DAG usa `schedule_interval=None` e `catchup=False`, portanto o retreino é disparado manualmente na demonstração.

## Critério de aceite

- [x] Arquivo `.py` de DAG versionado.
- [x] Tarefa de preparação/carregamento dos dados.
- [x] Tarefa de treino.
- [x] Artefato final em `models/baseline.joblib`.
- [x] Dependência explícita `ingest_task >> train_task`.