# Etapa 01 — Esqueleto da trilha do modelo

**Trilha:** Modelagem e otimização (Vítor)  
**Status:** concluída (pastas + nota do recorte; ainda **sem** treino)  
**Data:** 2026-08-15

---

## Objetivo

Criar as “gavetas” do repositório onde o modelo vai viver, **antes** de escrever o script que monta o CSV. Assim o Vini sabe onde a API vai carregar o arquivo e o Edu sabe onde a DAG deve gravar o resultado do treino.

---

## Problema que estávamos resolvendo

O repositório tinha contexto (`.cursor/`, `.github/`) e os CSVs crus em `data/raw/`, mas não havia um lugar combinado para:

- o código Python do classificador;
- os CSVs `text,label` processados;
- o arquivo `baseline.joblib`.

Sem isso, cada pessoa poderia inventar pastas (`ml/`, `artifacts/`, `output/`) e quebrar o contrato `models/baseline.joblib` fechado no `docs/TODO.md` §0.2.

---

## O que foi implementado

```
src/triage/__init__.py     # marca a pasta como pacote Python
data/raw/                  # já existia (Kaggle)
data/processed/.gitkeep    # Git não guarda pasta vazia; o keep segura a gaveta
models/.gitkeep
docs/dataset.md            # recorte, labels, vazamento, limitações
```

Não foram criados nesta etapa: `prepare_data.py`, `train.py`, `predict.py`, API, Docker, Airflow.

---

## Como funciona internamente

Não há lógica de Machine Learning ainda.

- `__init__.py` vazio (só um docstring) faz o Python tratar `src/triage` como pacote, para depois podermos escrever `from src.triage.predict import predict` (o import exato pode ajustar quando o `train` existir).
- `.gitkeep` é um arquivo vazio cuja única função é a pasta aparecer no Git.

---

## Tecnologias e por quê

| Escolha | Por quê | Alternativa descartada |
|---------|---------|------------------------|
| `src/triage/` | Nome alinhado ao produto (triagem), não `ml/` genérico | Pacote na raiz (`triage.py` solto) — piora quando a API crescer |
| `models/baseline.joblib` | Contrato §0.2; um arquivo só (Pipeline inteiro) | Pasta `pkl/` ou dois arquivos (vetor + classificador) — a API teria que carregar duas coisas |
| `docs/dataset.md` agora | O recorte já estava decidido; registrar antes do código evita treinar no CSV errado | Esperar o `prepare_data` para escrever a nota — risco de alguém usar `structured_medical_records.csv` como treino |

Nenhuma biblioteca nova foi instalada.

---

## Impacto no sistema

- **Vini:** pode assumir que o modelo virá de `models/baseline.joblib`.
- **Edu:** a DAG deve terminar nesse mesmo path.
- **Você (próximo passo):** `prepare_data.py` grava em `data/processed/`.

---

## Exemplo prático

Depois desta etapa, no disco:

1. Você baixa/já tem os CSVs em `data/raw/`.
2. Ainda **não** existe `train.csv`.
3. A pasta `models/` existe, mas está vazia (exceto o `.gitkeep`).

O “cérebro” do classificador só aparece na Etapa 03.

---

## Fluxo de dados (ainda não corre)

```
data/raw/*.csv  --(Etapa 02)-->  data/processed/*.csv  --(Etapa 03)-->  models/baseline.joblib
                                                                      --(Etapa 04)--> predict(text)
```

---

## Limitações e próxima etapa

- Esqueleto não treina nem valida vazamento.
- Próximo: **Etapa 02** — `prepare_data.py` (ver `TODO.md` desta pasta).

Leitura complementar: `docs/dataset.md`.
