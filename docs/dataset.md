# Dataset — Medical Text Triage

Nota operacional da trilha do modelo. Decisões canônicas: `docs/TODO.md` §0.2.  
Tabelas oficiais do MIMIC: `docs/dataset_doc/`.

Este arquivo descreve **o recorte e as regras**. Os CSVs processados são gerados por `src/triage/prepare_data.py` (Etapa 02).

---

## Fonte

- **Nome:** MIMIC-III Clinical Database (Open Access)
- **Link:** https://www.kaggle.com/datasets/ihssanened/mimic-iii-clinical-databaseopen-access
- **O que é:** recorte público da **demo** MIMIC-III (Beth Israel Deaconess, UTI), não o banco completo (esse exige credencial PhysioNet).
- **Arquivos em `data/raw/`:**
  - `ADMISSIONS.csv` — 129 internações (define `hadm_id`)
  - `PATIENTS.csv` — 100 pacientes (define `subject_id`)
  - `LABEVENTS.csv` — ~76 mil resultados de laboratório
  - `D_LABITEMS.csv` — dicionário dos exames (`itemid` → nome)
  - `structured_medical_records.csv` — 408 laudos **simulados**, só 9 internações, todas `EMERGENCY` (formato de referência, **não** o conjunto de treino)
- **Licença:** Kaggle marca Unknown; a demo PhysioNet correspondente usa ODbL. Uso acadêmico do Tech Challenge; não é dado clínico próprio.

---

## Como o dado vira texto + target

O Kaggle **não** traz uma coluna de urgência pronta. O CSV de treino é **montado** por `prepare_data.py`:

| Papel | Origem |
|-------|--------|
| Unidade de caso | uma internação (`hadm_id`) |
| Texto (`text`) | laudo simulado: `diagnosis` + sexo/idade + labs anormais daquela internação |
| Target (`label`) | `ADMISSIONS.admission_type` mapeado (abaixo) |

**Proibido no texto de treino/inferência:** tipo de admissão, as palavras EMERGENCY/ELECTIVE/URGENT como categoria, óbito, `hospital_expire_flag`, `subject_id`, e o marcador `/SDA` (quase só nas eletivas — vazaria `normal`).

`structured_medical_records.csv` serve de **modelo de redação**, não como única fonte: cobrir as 129 internações, inclusive as 8 eletivas e as 2 urgentes.

---

## Labels (contrato do projeto)

| `admission_type` | `label` | Internações neste recorte |
|------------------|---------|---------------------------|
| `ELECTIVE` | `normal` | 8 |
| `URGENT` | `atenção` | 2 |
| `EMERGENCY` | `urgente` | 119 |

Valores válidos de `label`: somente `normal`, `atenção`, `urgente`.

Isto **não** é diagnóstico clínico. É um proxy acadêmico do tipo de admissão já registrado no hospital.

---

## Split e métrica

- Separar treino/teste **por `hadm_id`** (a mesma internação não pode estar nos dois lados). Execução atual: 102 treino / 27 teste; as três labels nos dois lados.
- Métrica principal de qualidade: **F1 macro**. Accuracy sozinha mente (≈92% dos casos são `urgente`).
- Uma linha por internação (snapshots extras de lab **não** foram gerados).

---

## Limitações (documentar na entrega)

- Demo pequena: 100 pacientes, 129 internações.
- Os 100 pacientes da demo têm `expire_flag = 1` (seleção de quem um dia morreu). Não usar isso como target.
- Classe `atenção` tem só 2 internações; o modelo não vai ficar robusto nela.
- Laudo é simulado (diagnóstico preliminar + lista de lab). A demo não traz `NOTEEVENTS` preenchido.
- O PDF da FIAP *recomenda* ≥ 2.000 amostras; **não exige**. Este recorte atende o mínimo (classificador de texto treinável), não a recomendação de volume.

---

## Artefatos previstos

| Caminho | Conteúdo |
|---------|----------|
| `data/raw/` | CSVs do Kaggle |
| `data/processed/train.csv` | `text,label` — 102 internações |
| `data/processed/test.csv` | `text,label` — 27 internações |
| `models/baseline.joblib` | Pipeline sklearn (TF-IDF + Logistic Regression) |
| `src/triage/prepare_data.py` | Monta os CSVs processados |
| `src/triage/train.py` | Treina e avalia o baseline |
| `src/triage/predict.py` | `predict(text) -> {label, confidence}` |

Como reproduzir: venv Python 3.11.9 + `python src/triage/prepare_data.py` + `python src/triage/train.py` + `python src/triage/predict.py`.  
Detalhes: `docs/etapas/Modelagem e otimização/etapa-02.md`, `etapa-03.md` e `etapa-04.md`.
