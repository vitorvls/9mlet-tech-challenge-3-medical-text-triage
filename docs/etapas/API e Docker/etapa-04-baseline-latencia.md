# Etapa 04 — Baseline de Latência (N4)

**Trilha:** API e Docker — Vini  
**Data:** 2026-08-18  
**Branch:** `feat/api-docker-baseline`

---

## O que foi feito (em linguagem simples)

Medimos quanto tempo a API demora para responder. Essa medição é o **baseline** — o ponto de partida que o Vítor vai comparar com a versão otimizada (etapa de otimização, Semana C).

---

## Método de medição

- **Script:** `scripts/benchmark_latency.py`
- **N:** 100 requisições sequenciais (uma de cada vez, sem paralelismo)
- **Textos:** 3 laudos de exemplo do dataset (sepse, cirurgia eletiva, parada cardíaca), rotacionados
- **Métrica principal:** média e p95 de latência ponta-a-ponta (cliente → API → resposta)
- **Hardware:** MacBook Apple M-series (macOS), porta local

---

## Resultados

### Ambiente: servidor local (`uvicorn` direto, sem Docker)

| Métrica | Valor |
|---------|-------|
| n (requisições) | 100 / 100 |
| Média | 16.4 ms |
| Mediana (p50) | 11.09 ms |
| p95 | 34.58 ms |
| p99 | 180.96 ms |
| Mínimo | 5.96 ms |
| Máximo | 181.39 ms |

### Ambiente: API dentro do Docker (`docker run -p 8766:8000`)

| Métrica | Valor |
|---------|-------|
| n (requisições) | 100 / 100 |
| Média | 7.44 ms |
| Mediana (p50) | 6.96 ms |
| p95 | 10.25 ms |
| p99 | 19.96 ms |
| Mínimo | 5.7 ms |
| Máximo | 20.01 ms |

> **Nota:** Docker mostrou latência menor que o servidor local neste teste, provavelmente por diferença no overhead de startup e carregamento do modelo em cada ambiente. O número relevante para comparação com a versão otimizada (Vítor, Semana C) é o **ambiente Docker**, por ser mais próximo de produção.

---

## Resultados completos

Os arquivos JSON e CSV com os resultados completos estão em `evidencias/`:

- `evidencias/latency_baseline_<timestamp>.json` — resultado detalhado
- `evidencias/latency_baseline_summary.csv` — tabela acumulativa para comparação futura

---

## Como reproduzir

```bash
# 1. Suba a API (local ou Docker)
uvicorn triage.api:app --host 127.0.0.1 --port 8000
# ou
docker run --rm -p 8000:8000 medical-triage:dev

# 2. Execute o script
python scripts/benchmark_latency.py
# Resultado em evidencias/

# Opções:
python scripts/benchmark_latency.py --url http://localhost:8000 --n 200 --out-dir evidencias/
```

---

## Contrato com o Vítor (Semana C)

- Referência: Docker, 100 requisições, média ~7ms, p95 ~10ms
- Comparação futura (modelo otimizado): mesma metodologia, mesmo hardware
- Evidências na pasta `evidencias/`

---

## Checkpoint Vini A — ✅ concluído

- [x] Contrato da API estável (`POST /predict`, `GET /health`, `GET /metrics`)
- [x] Docker build/run ok (`medical-triage:dev`)
- [x] Baseline de latência registrada (`evidencias/`)
