# Etapa 02 — Montar o CSV de treino (`prepare_data`)

**Trilha:** Modelagem e otimização (Vítor)  
**Status:** concluída (código + CSVs + este documento)  
**Data:** 2026-08-15

---

## Objetivo

Transformar as quatro tabelas do recorte MIMIC-III em dois arquivos simples:

- `data/processed/train.csv`
- `data/processed/test.csv`

Cada linha tem só duas colunas: **`text`** (laudo simulado) e **`label`** (`normal` / `atenção` / `urgente`).  
A Etapa 03 vai treinar o classificador **nesses** CSVs. Sem eles, não há o que ensinar ao modelo.

---

## Problema que estávamos resolvendo

O Kaggle **não** entrega uma coluna pronta de urgência nem um laudo único por paciente. O que existe são tabelas hospitalares:

| Arquivo | O que é, em linguagem simples |
|---------|-------------------------------|
| `ADMISSIONS.csv` | Cada linha é **uma internação**. Traz o diagnóstico preliminar e o tipo de admissão. |
| `PATIENTS.csv` | Cada linha é **uma pessoa** (sexo e data de nascimento). |
| `LABEVENTS.csv` | Cada linha é **um resultado de exame** de laboratório. |
| `D_LABITEMS.csv` | Dicionário: o código do exame (`itemid`) vira o **nome** (ex.: Hemoglobin). |

Havia ainda `structured_medical_records.csv`: 408 textos prontos, mas só **9** internações, **todas** `EMERGENCY`, e o próprio texto contém `Admission Type: EMERGENCY`. Se treinássemos só nele, o modelo “colaria” na palavra EMERGENCY e nunca veria as classes `normal` e `atenção`.

O trabalho desta etapa é **montar** o conjunto de treino a partir das tabelas, cobrindo as **129** internações, **sem vazar o rótulo** para dentro do texto.

---

## O que foi implementado

```
pyproject.toml                 # Python 3.11.9 + pandas / scikit-learn / joblib
.venv/                         # ambiente isolado (não vai para o Git)
.gitignore
src/triage/prepare_data.py     # script desta etapa
data/processed/train.csv       # 102 linhas, colunas text,label
data/processed/test.csv        # 27 linhas, colunas text,label
```

Não foram criados nesta etapa: `train.py`, `predict.py`, API, Docker, Airflow.

---

## Dataset utilizado

- **Nome:** MIMIC-III Clinical Database (Open Access), recorte público da **demo** (não é o MIMIC completo).
- **Link:** https://www.kaggle.com/datasets/ihssanened/mimic-iii-clinical-databaseopen-access
- **Onde está no repo:** `data/raw/`
- **Unidade de caso:** uma internação (`hadm_id`). Uma linha no CSV processado = uma internação.
- **Tamanho:** 100 pacientes, 129 internações, ~76 mil linhas de laboratório.
- **Licença:** uso acadêmico do Tech Challenge; não é dado clínico próprio.

### Origem do texto e do alvo

| Papel | Origem |
|-------|--------|
| Texto (`text`) | diagnóstico + sexo + idade + até 20 exames **anormais** daquela internação |
| Alvo (`label`) | `ADMISSIONS.admission_type` mapeado (abaixo) |

Isto **não** é um diagnóstico médico. É um *proxy* acadêmico: o hospital já registrou se a entrada foi eletiva, urgente ou emergência; nós só traduzimos isso para as três palavras do contrato.

---

## Labels

| `admission_type` no MIMIC | `label` do projeto | Quantas internações |
|---------------------------|--------------------|---------------------|
| `ELECTIVE` | `normal` | 8 |
| `URGENT` | `atenção` | 2 |
| `EMERGENCY` | `urgente` | 119 |

Valores válidos: **somente** essas três strings.

---

## Pré-processamento, limpeza e “feature” (o texto)

Não há features numéricas soltas. A “feature” desta etapa **é o próprio texto** do laudo simulado. O modelo da Etapa 03 vai transformar esse texto em números (TF-IDF). Aqui só montamos o texto com cuidado.

### 1. Junção das tabelas

1. Cada internação pega o paciente pelo `subject_id` (sexo e data de nascimento).
2. Os exames daquela internação entram pelo `hadm_id`.
3. O nome do exame vem de `D_LABITEMS`.
4. Só entram exames com `flag = abnormal` (o próprio laboratório já marcou como fora do esperado). Exames `delta` ficaram de fora: são poucos e significam “mudou bastante”, não “está anormal”.

### 2. Idade

Idade = diferença entre data de admissão e data de nascimento, em anos.

No MIMIC, pacientes com mais de 89 anos têm a data de nascimento **deslocada ~300 anos** (regra de privacidade HIPAA). O `pandas` não consegue subtrair datas tão distantes (`Timedelta` estoura). Por isso a conta usa `datetime` nativo do Python. Se a idade calculada passa de 150 anos, gravamos **90**.

### 3. Limpeza do diagnóstico (anti-vazamento)

Sete das oito internações eletivas traziam `/SDA` no diagnóstico (*Same Day Admission*). **Nenhuma** emergência trazia. Se deixássemos `/SDA` no texto, o modelo aprenderia “SDA = normal” — um atalho administrativo, não clínico. O script **remove** `/SDA` e troca barras invertidas do MIMIC por `;`.

### 4. O que **não** entra no texto

Proibido (e checado no final do script):

- `Admission Type` / EMERGENCY / ELECTIVE / URGENT como categoria
- `subject_id`, Patient ID
- óbito, `hospital_expire_flag`, `expire_flag`
- local da admissão (muitos dizem `EMERGENCY ROOM ADMIT` — vazaria a classe)

`structured_medical_records.csv` **não** é fonte de treino. O script só avisa isso no terminal.

### 5. Quantos exames cabem no laudo

Cada internação pode ter dezenas de exames anormais (mediana ~96 ocorrências). Um texto gigante memoriza ruído. Copiamos a ideia do caderno simulado: no máximo **20** nomes únicos, na **primeira** vez em que aquele exame aparece (mais perto da admissão — mais parecido com triagem).

---

## Como o script funciona internamente

Rodar, na venv 3.11.9, a partir da raiz do repositório:

```powershell
.\.venv\Scripts\Activate.ps1
python src/triage/prepare_data.py
```

Fluxo:

```
ADMISSIONS + PATIENTS + LABEVENTS + D_LABITEMS
        │
        ▼
  uma linha por hadm_id  →  texto montado  →  label mapeada
        │
        ▼
  checagem de vazamento (regex)
        │
        ▼
  split 80/20 por hadm_id, estratificado por label
        │
        ▼
  train.csv  e  test.csv
```

O split **não** é aleatório solto. Para cada classe:

- embaralha os `hadm_id` com semente `42` (reproduzível);
- reserva cerca de 20% para teste, **pelo menos 1** se a classe tiver 2 ou mais casos;
- a mesma internação **nunca** aparece nos dois lados.

Com só 2 casos de `atenção`, isso coloca **1 no treino e 1 no teste**. Sem isso, o teste poderia ficar sem a classe do meio e a Etapa 03 não conseguiria medir as três labels.

---

## Resultados obtidos (esta execução)

| Conjunto | n | `normal` | `atenção` | `urgente` |
|----------|---|----------|-----------|-----------|
| completo | 129 | 8 | 2 | 119 |
| treino | 102 | 6 | 1 | 95 |
| teste | 27 | 2 | 1 | 24 |

- Checagem de vazamento: **passou** (treino e teste).
- Textos repetidos entre treino e teste: **0**.
- Colunas dos CSVs: exatamente `text,label`.

A métrica de qualidade do **modelo** (F1 macro, accuracy) ainda **não** existe: não treinamos nada. Esses números entram na Etapa 03. O que esta etapa entrega é o **insumo** do treino.

---

## Tecnologias e por quê

| Escolha | Por quê | Alternativa descartada |
|---------|---------|------------------------|
| Python **3.11.9** | Decisão do projeto; interpretador já instalado na máquina | 3.13 do PATH — quebraria o pin do `pyproject.toml` |
| `pip` + `pyproject.toml` + `.venv` | Isola libs; versões ficam no Git | Poetry/uv — não adotados; `pip install` no Python global — polui a máquina |
| `pandas==2.3.3` | Junção das 4 tabelas e CSV | Só `csv` da biblioteca padrão — funciona, mas o join de labs fica longo e frágil |
| Um laudo por `hadm_id` | 129 casos honestos; evita repetir a mesma internação 20 vezes | Usar só `structured_medical_records.csv` — 9 casos, 1 classe, vazamento. Snapshots de lab por horário — infla n sem pacientes novos |
| Split próprio (não `train_test_split`) | Garante 1 `atenção` em cada lado | `sklearn.model_selection.train_test_split` com `stratify` — com n=2 e 20%, as duas `atenção` podem cair só no treino |

`scikit-learn` já está no `pyproject.toml` porque a Etapa 03 vai usá-lo. **Esta** etapa ainda não treina.

---

## Configurações importantes

No topo de `prepare_data.py`:

| Constante | Valor | Significado |
|-----------|-------|-------------|
| `MAX_ABNORMAL_LABS` | 20 | teto de exames no texto |
| `TEST_SIZE` | 0.20 | fração de internações no teste |
| `RANDOM_STATE` | 42 | semente do embaralhamento (mesmo comando → mesmos CSVs) |
| `HIPAA_AGE_YEARS` | 90 | idade gravada quando o DOB foi deslocado |

Caminhos padrão: `data/raw/` → `data/processed/`. A DAG do Edu pode passar `--raw-dir` e `--out-dir` sem mudar o código.

---

## Exemplo prático (laudo gerado)

Uma internação eletiva (`label = normal`) ficou assim — note a ausência de `/SDA` e de tipo de admissão:

```text
Diagnosis: RECURRENT LEFT CAROTID STENOSIS,PRE HYDRATION
Sex: M
Age: 76
Abnormal lab results:
- Creatinine: 1.4 mg/dL (abnormal)
- Glucose: 145 mg/dL (abnormal)
- Hemoglobin: 13.7 g/dL (abnormal)
...
```

Na inferência (Etapa 04 / API do Vini), o texto que entrar deve parecer com isso: diagnóstico + perfil + lista de labs, **sem** “Admission Type”.

---

## Impacto no resto do sistema

- **Etapa 03:** lê só `train.csv` / `test.csv`. Não deve voltar nas tabelas crus.
- **Vini:** o JSON `{"text": "..."}` deve ser o mesmo tipo de texto montado aqui.
- **Edu:** a DAG pode chamar `python src/triage/prepare_data.py` antes do treino, na venv 3.11.9.

---

## Limitações e riscos

- **Desbalanceamento:** ~92% das linhas são `urgente`. Accuracy sozinha vai parecer alta mesmo se o modelo chutar sempre “urgente”. Por isso a métrica combinada na Etapa 03 é **F1 macro**.
- **Classe `atenção`:** só 2 internações no recorte inteiro. Um exemplo no treino e um no teste. O modelo **não** vai ficar robusto nessa classe; isso é limitação do dado, não bug do script.
- **Laudo simulado:** a demo não traz notas clínicas reais (`NOTEEVENTS`). O texto é diagnóstico de admissão + labs.
- **Volume:** o PDF da FIAP *recomenda* ≥ 2.000 amostras; **não exige**. 129 internações atendem o mínimo (classificador treinável).
- **Todos os 100 pacientes da demo morreram em algum momento** (`expire_flag = 1`). Isso **não** entra no texto nem no alvo.
- **Labs da internação inteira (primeiros 20 únicos):** ainda podem incluir exames de horas depois da porta. Não usamos a janela rígida de 24 h porque 2 internações ficariam sem lab anormal nesse recorte.

---

## Melhorias futuras (não nesta etapa)

- Incluir FastAPI / Airflow no `pyproject.toml` quando Vini e Edu começarem as trilhas deles.
- Se o time quiser mais texto, snapshots de lab **com split ainda por `hadm_id`**.
- Não misturar outro dataset (ex.: Medical Abstracts) no mesmo `label` — os significados não combinam.

---

## Critério de conclusão (checklist)

- [x] `src/triage/prepare_data.py` existe e é reproduzível
- [x] `data/processed/train.csv` e `test.csv` gerados
- [x] três labels no conjunto; split por `hadm_id`
- [x] texto sem `Admission Type` / EMERGENCY como categoria
- [x] `structured_medical_records.csv` não usado como treino

Próximo: **Etapa 03** — `train.py` (TF-IDF + Logistic Regression → `models/baseline.joblib`).
