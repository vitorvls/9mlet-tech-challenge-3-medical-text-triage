# Model Card — Medical Text Triage

**Versão:** baseline 0.1.0  
**Atualizado:** 2026-09-09  
**Status:** protótipo acadêmico validado no fluxo local e no CI

## 1. Visão geral

O Medical Text Triage é um classificador leve de texto desenvolvido para o
Tech Challenge Fase 3 da FIAP. O sistema recebe um texto de laudo e retorna
uma classificação de prioridade acadêmica:

- `normal`
- `atenção`
- `urgente`

As classes são um proxy do tipo de admissão hospitalar usado no recorte do
dataset. Elas não representam diagnóstico, prognóstico ou recomendação clínica.

## 2. Uso pretendido

### Uso apropriado

- Demonstração acadêmica de um ciclo de machine learning aplicado a texto.
- Testes de integração entre treinamento, API, Airflow, Docker e observabilidade.
- Benchmark comparativo entre inferência Scikit-learn e ONNX Runtime.

### Uso inadequado

- Diagnosticar pacientes ou definir conduta médica.
- Substituir profissionais de saúde ou protocolos hospitalares.
- Tomar decisões clínicas reais com base na label ou na confiança retornada.
- Inferir risco individual fora do domínio e da distribuição deste recorte.

## 3. Dados de treinamento e avaliação

### Fonte

O projeto usa o recorte público da demo MIMIC-III Clinical Database disponível
no Kaggle:

<https://www.kaggle.com/datasets/ihssanened/mimic-iii-clinical-databaseopen-access>

O recorte contém 4.829 internações e 4.800 pacientes. O target não vem pronto no
dataset: ele é derivado de `ADMISSIONS.admission_type`.

| Tipo de admissão | Label do projeto | Casos |
|---|---|---:|
| `ELECTIVE` | `normal` | 1.208 |
| `URGENT` | `atenção` | 2.002 |
| `EMERGENCY` | `urgente` | 1.619 |

O texto é montado por `src/triage/prepare_data.py` a partir de diagnóstico,
sexo, idade e exames laboratoriais anormais. Campos que vazariam o target,
como tipo de admissão, flags de óbito, identificadores e `/SDA`, são removidos.

### Divisão

O split é feito por `hadm_id`, evitando que a mesma internação apareça nos
dois conjuntos:

- treino: 3.863 internações;
- teste: 966 internações.

O PDF da FIAP recomenda pelo menos 2.000 amostras; o conjunto processado atual
possui 4.829 exemplos. A distribuição das labels deve ser considerada nas
avaliações e novos treinamentos.

## 4. Modelo e treinamento

O baseline é um Pipeline Scikit-learn composto por:

1. `TfidfVectorizer`, com texto em minúsculas, unigramas e remoção de stopwords
   em inglês;
2. `LogisticRegression`, com `class_weight="balanced"`, `solver="lbfgs"`,
   `max_iter=1000` e estado aleatório 42.

O treinamento é implementado em `src/triage/train.py` e salva o pipeline em:

```text
models/baseline.joblib
```

A DAG `dags/train_dag.py` executa o fluxo:

```text
prepare_data -> train -> models/baseline.joblib
```

## 5. Resultados de qualidade

A métrica principal é F1 macro, pois a distribuição é fortemente desbalanceada.
Accuracy isolada é enganosa neste dataset.

| Conjunto | Amostras | Accuracy | F1 macro |
|---|---:|---:|---:|
| Treino | 3.863 | 0,9047 | 0,9013 |
| Teste | 966 | 0,8747 | 0,8700 |

No conjunto de teste, o relatório por classe registrado foi:

| Classe | Precision | Recall | F1 | Suporte |
|---|---:|---:|---:|---:|
| `normal` | 0,7985 | 0,8678 | 0,8317 | 242 |
| `atenção` | 0,9036 | 0,8900 | 0,8967 | 400 |
| `urgente` | 0,9029 | 0,8611 | 0,8815 | 324 |

O resultado indica overfitting no treino e baixa generalização das classes
raras. Esses números não devem ser apresentados como desempenho clínico.

## 6. Otimização de inferência

O pipeline foi exportado para ONNX com `skl2onnx` e executado com ONNX Runtime.
Os artefatos e scripts relacionados são:

- `models/baseline.onnx`;
- `src/models/onnx_export.py`;
- `scripts/benchmark_latency.py`;
- `scripts/benchmark_latency_onnx.py`.

Benchmark registrado com 1.000 amostras:

| Implementação | Tempo médio por amostra | Resultado |
|---|---:|---|
| Scikit-learn | 0,236 s | baseline |
| ONNX Runtime | 0,154 s | aproximadamente 34,7% mais rápido |

O resultado varia conforme CPU, memória e carga do host. A versão ONNX é usada
como otimização e comparação; o contrato principal da API continua carregando
`models/baseline.joblib`.

## 7. Interface de inferência

A API FastAPI expõe:

- `GET /health`: estado do serviço e disponibilidade do modelo;
- `POST /predict`: recebe `{"text": "..."}` e retorna
  `{"label": "...", "confidence": 0.0}`;
- `GET /metrics`: métricas Prometheus.

O campo `confidence` é a probabilidade estimada pelo classificador para a
classe escolhida. Não é uma probabilidade clínica nem uma medida de segurança.

## 8. Operação e validação

A stack local é executada pelo Docker Compose no Rancher Desktop:

- API na porta 8000;
- Prometheus na porta 9090;
- Grafana na porta 3000.

O Prometheus coleta contagem de requisições, latência, erros, confiança,
tamanho do input e estado do modelo. O Grafana possui dashboards provisionados
com oito painéis.

Validações registradas:

- suíte local: 14 testes aprovados;
- Flake8: aprovado;
- DAG: carregada com `ingest_data` antes de `train_and_export_model`;
- Compose: API saudável, Prometheus pronto e Grafana ativo;
- GitHub Actions: [run #6 aprovado](https://github.com/vitorvls/9mlet-tech-challenge-3-medical-text-triage/actions/runs/34303445013), com jobs de validação e build.

## 9. Riscos e limitações

- O recorte ainda é específico da demo MIMIC-III e não representa toda a população hospitalar.
- A distribuição das labels deve ser monitorada a cada incremento dos dados.
- Os laudos são simulados; não são notas clínicas completas.
- O target é um proxy administrativo derivado do tipo de admissão.
- O modelo pode memorizar vocabulário específico do recorte.
- Não há validação externa, calibração clínica, análise de subgrupos ou
  aprovação para uso hospitalar.
- A licença indicada pelo Kaggle é `Unknown`; o uso é acadêmico e o MIMIC
  completo não deve ser redistribuído.

## 10. Reprodutibilidade

Na raiz do repositório, com Python 3.11:

```powershell
python -m pip install -e ".[dev]"
python src/triage/prepare_data.py
python src/triage/train.py
python -m pytest -q
```

Para subir a stack:

```powershell
docker compose up -d --build
```

## 11. Manutenção do card

Este documento deve ser atualizado quando houver mudança no dataset, labels,
artefato, métrica, endpoint, técnica de otimização ou resultado de validação.