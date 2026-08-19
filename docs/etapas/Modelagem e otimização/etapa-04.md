# Etapa 04 — Função `predict` (contrato da API e da DAG)

**Trilha:** Modelagem e otimização (Vítor)  
**Status:** concluída (código + três exemplos + este documento)  
**Data:** 2026-08-15

---

## Objetivo

Entregar a função que o Vini (API) e o Edu (DAG / smoke) vão chamar:

```python
predict(text: str) -> {"label": str, "confidence": float}
```

- `label`: só `normal`, `atenção` ou `urgente`
- `confidence`: número entre 0 e 1 (probabilidade da classe escolhida)

O JSON da API deve **espelhar** isso. Path HTTP (`POST /predict`) continua com o Vini.

---

## Problema que estávamos resolvendo

Na Etapa 03 o modelo passou a existir em disco (`models/baseline.joblib`), mas cada colega ainda poderia carregar o arquivo de um jeito diferente:

- chamar `pipeline.predict` e esquecer a probabilidade;
- recarregar o joblib **a cada requisição** (lento);
- inventar uma quarta label;
- quebrar se o arquivo não estiver lá, com um erro ilegível.

Esta etapa fecha o **contrato de software**: um módulo, um path, uma assinatura.

---

## O que foi implementado

```
src/triage/predict.py
src/triage/__init__.py   # reexporta predict
```

Não foram criados: FastAPI, Docker, Airflow, page de demo.

---

## Como funciona internamente

1. **`get_pipeline()`** carrega `models/baseline.joblib` **uma vez** por processo (e por path). A API sobe, chama isso no startup ou na primeira inferência, e reutiliza o objeto em memória.
2. **`predict(text)`**
   - rejeita o que não for string ou for só espaço (`ValueError` / `TypeError`) — a API do Vini traduz isso para HTTP;
   - `pipeline.predict([texto])` → label;
   - `pipeline.predict_proba([texto])` → vetor de 3 probabilidades; `confidence` é a da **classe escolhida**;
   - recusa label fora do contrato (não deveria acontecer; é cinto de segurança).
3. Se o arquivo do modelo não existe: `FileNotFoundError` com a dica `python src/triage/train.py`.

### O que é `confidence` (em linguagem simples)

Não é “o modelo tem 70% de certeza clínica”. É só:

> das três notas que a regressão logística deu, a da classe vencedora, convertida em probabilidade (softmax interno do sklearn).

Limitações:

- **Não está calibrada.** 0,70 não significa “70% dos casos assim estão certos”.
- Com classes raras, o número pode parecer alto e a label ainda ser instável (ver F1 da Etapa 03).
- A API deve devolver o número; o README/vídeo **não** devem vender como diagnóstico.

Arredondamos para 4 casas para o JSON ficar estável na demo.

---

## Como o Vini importa (exemplo)

Com a venv e `pip install -e .` (já feito neste repo):

```python
from triage.predict import predict

result = predict("Diagnosis: SEPSIS\nSex: F\nAge: 70")
# {"label": "urgente", "confidence": 0.5847}
```

Na API: chamar `predict(payload.text)` e devolver o dict. **Não** chamar `joblib.load` de novo em cada request — `get_pipeline()` já segura o objeto.

O Edu, num smoke da DAG, pode usar o mesmo import ou:

```powershell
.\.venv\Scripts\Activate.ps1
python src/triage/predict.py --text "Diagnosis: SEPSIS"
```

---

## Três textos de exemplo (critério da etapa)

Comando: `python src/triage/predict.py`  
Modelo: `models/baseline.joblib`

Os laudos seguem o formato da Etapa 02 (sem `Admission Type`, sem `/SDA`).

| # | Intenção do exemplo | `label` | `confidence` |
|---|---------------------|---------|--------------|
| 1 | Cirurgia programada (carótida) | `normal` | 0,6954 |
| 2 | VF arrest / CK muito alto | `atenção` | 0,7095 |
| 3 | Sepse + lactato | `urgente` | 0,5980 |

Saída bruta:

```json
{"label": "normal", "confidence": 0.6954}
{"label": "atenção", "confidence": 0.7095}
{"label": "urgente", "confidence": 0.598}
```

Estes três acertos **não** contradizem o F1 macro 0,48 da Etapa 03. Ali o teste tinha 27 internações reais; aqui escolhemos textos **ilustrativos** (inclusive vizinhos do treino). Servem para o Vini plugar a API e para o vídeo mostrar as três labels. Não são uma nova métrica de qualidade.

Texto vazio:

```text
ValueError: text must be a non-empty string
```

---

## Tecnologias e por quê

| Escolha | Por quê | Descartado |
|---------|---------|------------|
| `joblib.load` do Pipeline | mesmo arquivo da Etapa 03; vetor + clf juntos | carregar só o classificador |
| Singleton em memória | latência da API não paga I/O a cada POST | `load` dentro de `predict` |
| `predict_proba` | contrato pede `confidence` ∈ [0, 1] | devolver só a label ou a distância da decisão |
| Erros de validação na função | BR-4; a API mapeia para HTTP depois | silenciar texto vazio como `normal` |
| Sem FastAPI neste arquivo | trilha do Vini; não misturar | endpoint HTTP aqui |

Bibliotecas: `joblib==1.5.3`, `scikit-learn==1.9.0` (já no `pyproject.toml`). Python 3.11.9.

---

## Impacto no sistema

- **Vini:** pode implementar `POST /predict` agora. Input `{"text": "..."}`, output = retorno de `predict`.
- **Edu:** a DAG não precisa desta função para **treinar**; precisa do `train.py`. `predict` serve para checar o artefato depois de salvar.
- **Page opcional (backlog):** se existir, só chama a API; não importa este módulo no browser.
- Path do modelo **não muda** sem avisar o time.

---

## Fluxo

```
texto  →  predict()  →  Pipeline em memória  →  {label, confidence}
              │
              └── primeira chamada: joblib.load(models/baseline.joblib)
```

---

## Limitações e próxima etapa

- Confidence não calibrada; não usar como risco clínico.
- Texto muito longo: ainda **sem** teto (PENDENTE no `business-rules.md`). Não inventamos limite aqui.
- Checkpoint Vítor A (Etapa 05) empacota isto + treino + path para o recado ao grupo.

Próximo: **Etapa 05** — Checkpoint Vítor A.
