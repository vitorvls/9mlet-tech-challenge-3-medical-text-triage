# Etapa 03 — Treinar o baseline (TF-IDF + Logistic Regression)

**Trilha:** Modelagem e otimização (Vítor)  
**Status:** concluída (código + `models/baseline.joblib` + este documento)  
**Data:** 2026-08-15

---

## Objetivo

Ensinar um classificador **leve** a ler o laudo (`text`) e devolver uma das três labels (`normal`, `atenção`, `urgente`). O resultado precisa ser **um único arquivo**:

`models/baseline.joblib`

A API do Vini e a DAG do Edu vão carregar **esse** path. Vetorizador e classificador viajam juntos, dentro de um `Pipeline` do scikit-learn.

---

## Problema que estávamos resolvendo

Computadores não “leem” português/inglês do jeito que nós lemos. Eles precisam de **números**. Esta etapa faz duas coisas:

1. Transformar cada laudo numa lista de números (TF-IDF).
2. Aprender um limite de decisão nesses números (Regressão Logística) para escolher a label.

O PDF da FIAP cita TF-IDF + Random Forest como **exemplo**. O contrato do projeto (§0.2) já escolheu **TF-IDF + Logistic Regression** com `class_weight="balanced"`.

---

## Dataset desta etapa

Não voltamos nas tabelas crus. Usamos só o que a Etapa 02 gerou:

| Arquivo | n | `normal` | `atenção` | `urgente` |
|---------|---|----------|-----------|-----------|
| `data/processed/train.csv` | 102 | 6 | 1 | 95 |
| `data/processed/test.csv` | 27 | 2 | 1 | 24 |

- **Origem:** recorte MIMIC-III Open Access (Kaggle), 129 internações.
- **Texto:** laudo simulado (diagnóstico + sexo + idade + labs anormais), **sem** tipo de admissão.
- **Alvo:** proxy de `admission_type` (ELECTIVE→`normal`, URGENT→`atenção`, EMERGENCY→`urgente`).
- **Split:** já feito por `hadm_id` na Etapa 02. Esta etapa **não** ressplitta. Treina no `train.csv` e avalia no `test.csv`.

Pré-processamento extra aqui: só `lowercase=True` e remoção de stop words em inglês (`the`, `with`, `of`…). O conteúdo clínico já foi limpo na Etapa 02 (`/SDA`, IDs, óbito).

---

## O que foi implementado

```
src/triage/train.py
models/baseline.joblib
```

Comando (venv Python 3.11.9, raiz do repo):

```powershell
.\.venv\Scripts\Activate.ps1
python src/triage/train.py
```

Não foram criados nesta etapa: `predict.py`, API, Docker, Airflow, ONNX.

---

## Como funciona internamente (didático)

Imagine cada laudo como uma receita de palavras.

### Passo 1 — TF-IDF (`TfidfVectorizer`)

- **TF (term frequency):** se “sepsis” aparece várias vezes neste laudo, o peso sobe.
- **IDF (inverse document frequency):** se “sepsis” aparece em *quase todos* os laudos, o peso cai — a palavra não ajuda a distinguir.
- O resultado é um vetor esparso: cada posição é uma palavra do vocabulário do **treino**. Palavras que só existem no teste entram como zero.

Usamos **unigramas** (uma palavra de cada vez). Com 102 textos, bigramas (`white blood`) criariam muitas colunas para poucos exemplos — o modelo memorizaria combinações raras.

### Passo 2 — Regressão logística (`LogisticRegression`)

Não é uma reta de “preço × tamanho”. É um classificador: para cada label, aprende **pesos** das palavras. Na hora de prever, calcula três notas (uma por classe) e escolhe a maior. Com `predict_proba` (Etapa 04) essas notas viram probabilidades — a `confidence` da API.

`class_weight="balanced"`: como 95 dos 102 treinos são `urgente`, sem isso o modelo ganharia “chutando urgente sempre”. O peso inverso da frequência força ele a prestar mais atenção em `normal` e `atenção`.

### Passo 3 — `Pipeline` + `joblib`

```
texto  →  TfidfVectorizer  →  LogisticRegression  →  label
              \________________ Pipeline ________________/
```

Salvar o Pipeline inteiro evita a API ter que lembrar a ordem das colunas do TF-IDF. Um arquivo só.

---

## Hiperparâmetros (o que fixamos)

| Peça | Valor | Por quê |
|------|-------|---------|
| `ngram_range` | `(1, 1)` | vocabulário cabe no n pequeno |
| `min_df` | `1` | com 102 docs, exigir df≥2 apagaria termos raros das classes minoritárias |
| `stop_words` | `"english"` | laudos estão em inglês (MIMIC) |
| `lowercase` | `True` | `SEPSIS` e `sepsis` viram a mesma feature |
| `class_weight` | `"balanced"` | contrato §0.2; 92% `urgente` |
| `max_iter` | `1000` | dá tempo do solver convergir |
| `solver` | `"lbfgs"` | padrão multinomial do sklearn |
| `random_state` | `42` | treino reproduzível |

Não fizemos busca em grade (grid search). O baseline é este; comparar RF/BERT fica para se o time pedir.

---

## Estratégia de treino e validação

- **Treino:** `fit` só em `train.csv`.
- **Teste:** `predict` em `test.csv` **depois** do `fit`. Esses números são os que valem.
- **Por que não k-fold:** a classe `atenção` tem **1** exemplo no treino. Dobrar o treino em 5 fatias deixaria folds sem essa classe. O hold-out da Etapa 02 (1 `atenção` em cada lado) já é o desenho honesto.

Imprimimos métricas de **treino e teste**. Treino serve para detectar memorização; **não** para vender o modelo.

---

## Métricas — o que cada uma significa neste problema

Pense num plantão que precisa priorizar laudos. Errar “é urgente” quando não é, ou o contrário, tem custos diferentes. As métricas abaixo **não** medem qualidade clínica real (o alvo é só o tipo de admissão). Medem se o classificador acerta esse proxy.

### Accuracy (acurácia) — “quantos acertei no total?”

\[
\text{accuracy} = \frac{\text{acertos}}{\text{total}}
\]

No teste: **0,8889** (24 acertos em 27).

**Por que ela mente aqui:** se o modelo chutar `urgente` em tudo, acerta 24/27 ≈ **89%** sem nunca reconhecer `normal` ou `atenção`. Por isso o contrato do projeto **não** usa accuracy sozinha.

### Precision (precisão) — “quando eu grito essa classe, eu estava certo?”

Exemplo `normal`: das vezes que o modelo disse `normal`, quantas realmente eram `normal`?

No teste, `normal` teve precisão **0,50** (disse `normal` 2 vezes; acertou 1).

### Recall (revocação / sensibilidade) — “dos que realmente eram essa classe, quantos eu peguei?”

Exemplo `urgente`: dos 24 urgentes reais, o modelo pegou **23** → recall **0,9583**.  
Exemplo `atenção`: havia 1 caso real; o modelo previu `urgente` → recall **0,00**.

Neste problema, recall baixo em `atenção`/`normal` significa: as classes raras passam batidas, misturadas no monte de `urgente`.

### F1 — média harmônica de precision e recall

O F1 de uma classe só fica alto se **as duas** (precision e recall) estiverem razoáveis. Se uma for zero, F1 é zero.

### F1 macro — a métrica principal deste projeto

Média **não ponderada** do F1 das três classes. Cada classe vale **1/3**, mesmo `atenção` tendo 1 exemplo.

No teste: **0,4796**.

É a métrica certa *porque* o dataset é torto. Ela pune o modelo que só sabe a classe majoritária. O número baixo **não** é surpresa: com 1 exemplo de `atenção` no treino, o modelo não tem como generalizar essa classe.

F1 *weighted* (0,87 no teste) parece bonito porque pesa pelas 24 linhas `urgente`. Não usamos weighted como critério de escolha.

### Matriz de confusão — “quem foi confundido com quem?”

Linha = verdade. Coluna = o que o modelo disse.

**Teste (n=27):**

| verdade \ predito | normal | atenção | urgente |
|-------------------|--------|---------|---------|
| normal (2) | **1** | 0 | 1 |
| atenção (1) | 0 | **0** | 1 |
| urgente (24) | 1 | 0 | **23** |

Leitura em linguagem simples:

- Quase todos os `urgente` foram reconhecidos (23/24).
- Metade dos `normal` foi para `urgente`.
- O único `atenção` foi para `urgente`.
- O modelo **nunca** previu `atenção` no teste.

---

## Resultados obtidos

| Conjunto | Accuracy | F1 macro | Leitura honesta |
|----------|----------|----------|-----------------|
| Treino (102) | 1,0000 | 1,0000 | memorizou o treino |
| **Teste (27)** | **0,8889** | **0,4796** | acerta o grosso `urgente`; falha nas raras |

Relatório por classe no **teste**:

| Classe | Precision | Recall | F1 | n no teste |
|--------|-----------|--------|-----|------------|
| `normal` | 0,50 | 0,50 | 0,50 | 2 |
| `atenção` | 0,00 | 0,00 | 0,00 | 1 |
| `urgente` | 0,92 | 0,96 | 0,94 | 24 |

---

## Interpretação

1. **O baseline cumpre o contrato técnico:** existe um Pipeline sklearn em `models/baseline.joblib`, treinado com TF-IDF + LR balanceada.
2. **Não cumpre um padrão clínico** — e não precisa: o desafio pede classificador leve + ciclo MLOps, não um modelo de pronto-socorro.
3. **Treino perfeito + teste mediano = overfitting.** Com 102 textos e milhares de palavras possíveis, a logística consegue “decorar” o treino. O F1 macro de teste é o número que o README/vídeo devem citar se falarem de qualidade.
4. **A classe `atenção` é um limite do dado**, não um bug do `train.py`. Dois pacientes no recorte inteiro. Sem mais `URGENT`, F1 dessa classe continua instável.

---

## Experimentos nesta etapa

Um único treino: o baseline fechado no §0.2. Não comparamos Random Forest nem BERT aqui.

O “experimento” implícito é treino vs teste: se só olhássemos accuracy de treino (100%), acharíamos o modelo perfeito. O teste mostra o contrário. Por isso o script imprime os dois blocos.

---

## Por que este modelo (e o que foi descartado)

| Escolha | Por quê | Descartado |
|---------|---------|------------|
| Logistic Regression | linear, rápido, dá probabilidade (`predict_proba`) para a `confidence` da API; `class_weight` nativo | Random Forest (exemplo FIAP) — com n pequeno memoriza regras; BERT — pesado, fora do “NLP leve” |
| TF-IDF | clássico, CPU, zero GPU | embeddings / transformers nesta fase |
| Um `Pipeline` + joblib | um path para API e DAG | salvar vetor e clf em dois `.pkl` |
| `joblib` | contrato `models/baseline.joblib` | pickle cru, ONNX (Semana C, Etapa 06) |

Bibliotecas: `scikit-learn==1.9.0`, `joblib==1.5.3`, `pandas==2.3.3` (ler CSV). Python **3.11.9** na `.venv`.

---

## Impacto no sistema

- **Vini:** pode carregar `models/baseline.joblib` com `joblib.load`. A função `predict` ainda não existe (Etapa 04); até lá, `pipeline.predict([texto])` já devolve a label.
- **Edu:** a DAG deve chamar `python src/triage/train.py` (depois do `prepare_data`) e terminar nesse mesmo path.
- **Não** mudar o path sem avisar o time.

---

## Exemplo prático

Depois desta etapa, no disco:

```text
models/baseline.joblib    # Pipeline sklearn (tfidf + clf)
```

Trecho equivalente ao que o script faz:

```python
import joblib
pipe = joblib.load("models/baseline.joblib")
print(pipe.predict(["Diagnosis: SEPSIS\nSex: F\nAge: 70"])[0])
```

A embalagem `{label, confidence}` é a Etapa 04.

---

## Fluxo dos dados

```
train.csv  --fit-->  Pipeline  --joblib-->  models/baseline.joblib
test.csv   --predict-->  métricas impressas (accuracy, F1 macro, matriz)
```

---

## Limitações e melhorias futuras

- F1 macro de teste baixo; accuracy alta e enganosa.
- `atenção` com suporte 1: qualquer acerto/erro muda o F1 macro bastante.
- Sem calibração de probabilidade ainda (a `confidence` da Etapa 04 será o `max(predict_proba)`, não um score calibrado).
- Sem comparação RF (opcional depois, se o time quiser uma tabela no README).
- Otimização de latência (ONNX) é Etapa 06, não agora.

---

## Critério de conclusão

- [x] `src/triage/train.py` reproduzível
- [x] `models/baseline.joblib` gerado
- [x] F1 macro, accuracy e matriz de confusão no teste, **explicados** neste `.md`

Próximo: **Etapa 04** — `predict(text) -> {label, confidence}`.
