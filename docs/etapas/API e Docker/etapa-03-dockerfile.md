# Etapa 03 — Dockerfile da API

**Trilha:** API e Docker — Vini  
**Data:** 2026-08-18  
**Branch:** `feat/api-docker-baseline`

---

## O que foi feito (em linguagem simples)

Empacotamos a API numa "caixa" Docker de dois estágios. Qualquer máquina com Docker consegue rodar a API com dois comandos, independentemente de ter Python instalado.

---

## Arquivos criados

| Arquivo | Para que serve |
|---------|----------------|
| `Dockerfile` | Define como construir a imagem da API |
| `.dockerignore` | Exclui arquivos desnecessários da imagem (reduz tamanho e tempo de build) |

---

## Como o Dockerfile funciona (dois estágios)

```
Stage 1: builder
  ├── python:3.11-slim (imagem base)
  ├── Copia pyproject.toml + src/
  └── Cria /opt/venv e instala todas as dependências

Stage 2: runtime
  ├── python:3.11-slim (imagem limpa — sem cache de pip, sem build tools)
  ├── Copia /opt/venv do stage 1
  ├── Copia src/ do stage 1
  ├── Copia models/baseline.joblib
  ├── Cria usuário appuser (não-root, por segurança)
  └── Expõe porta 8000
```

O `stage 2` não tem `pip install` — só o que é necessário para rodar. Isso reduz a superfície de ataque e o tamanho final da imagem.

---

## Como usar

### Build

```bash
# Da raiz do projeto
docker build -t medical-triage:dev .
```

### Run

```bash
docker run --rm -p 8000:8000 medical-triage:dev
```

### Testar dentro do container

```bash
# Health
curl http://localhost:8000/health
# → {"status":"ok","model_loaded":true}

# Predição
curl -s -X POST http://localhost:8000/predict \
  -H "Content-Type: application/json" \
  -d '{"text": "Diagnosis: SEPSIS\nSex: F\nAge: 70"}'
# → {"label":"urgente","confidence":0.6088}

# Métricas Prometheus
curl http://localhost:8000/metrics
```

---

## Evidência de funcionamento

Saída real obtida durante os testes de build:

```
$ curl -s http://localhost:8766/health
{"status":"ok","model_loaded":true}

$ curl -s -X POST http://localhost:8766/predict \
    -H "Content-Type: application/json" \
    -d '{"text": "Diagnosis: SEPSIS\nSex: F\nAge: 70\nAbnormal lab results:\n- Lactate: 4.1 mmol/L (abnormal)"}'
{"label":"urgente","confidence":0.6088}
```

---

## Decisões técnicas

- **Multi-stage build:** reduz imagem final (apenas runtime, sem cache de pip nem ferramentas de build).
- **Usuário não-root (`appuser`):** boa prática de segurança (OWASP A05 — Security Misconfiguration).
- **PYTHONDONTWRITEBYTECODE + PYTHONUNBUFFERED:** evita `.pyc` desnecessários e faz logs aparecerem em tempo real.
- **Porta 8000:** padrão do uvicorn; `docker run -p 8000:8000` para mapear ao host.
