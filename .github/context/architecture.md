# Architecture Overview

## Objective

Arquitetura **mínima** alinhada ao Tech Challenge Fase 3.  
Fonte tipada: `.github/context/tech-challenge-requirements.md`.

**Princípio:** solução mais simples que cumpra as 4 etapas e os critérios de avaliação. Sem superengenharia.

---

## 1. System Overview

**Project:** `9mlet-tech-challenge-3-medical-text-triage`

**Descrição:** Serviço de inferência que classifica texto de laudo médico por nível de urgência, com ciclo de vida de modelo (treino/retreino via Airflow), CI/CD, monitoramento local e otimização de latência.

**Estilo:** API REST síncrona (request/response), estática quanto a sessão (stateless), com modelo carregado em processo para inferência.

**Usuários formais:** não definidos pelo PDF. Contexto de produto em `project-goals.md` (não é requisito FIAP).

---

## 2. High-Level Components

```
┌─────────────┐     HTTP/JSON      ┌──────────────────────────┐
│   Cliente   │ ─────────────────► │  API FastAPI (Docker)    │
└─────────────┘                    │  - validação de input    │
                                   │  - inferência NLP        │
                                   │  - /metrics (Prometheus) │
                                   └────────────┬─────────────┘
                                                │ scrape
                                   ┌────────────▼─────────────┐
                                   │  Prometheus              │
                                   └────────────┬─────────────┘
                                                │
                                   ┌────────────▼─────────────┐
                                   │  Grafana (≥3 painéis)    │
                                   └──────────────────────────┘

Docker Compose: API + Prometheus + Grafana

┌─────────────────────────────────────────────────────────────┐
│  Airflow DAG (treino/retreino)                              │
│  Exemplo FIAP: carregar dados → treinar → salvar modelo     │
└─────────────────────────────────────────────────────────────┘

┌─────────────────────────────────────────────────────────────┐
│  GitHub Actions: ≥2 automações (ex.: lint + testes)         │
└─────────────────────────────────────────────────────────────┘
```

### Responsabilidades

| Componente | Responsabilidade |
|------------|------------------|
| FastAPI | Receber texto do laudo; retornar classificação; expor métricas |
| Modelo NLP leve | Inferência de urgência; versão original + versão otimizada |
| Docker | Empacotar serviço de inferência |
| Docker Compose | Subir API + Prometheus + Grafana juntos |
| prometheus_client | Tempo de requisição + contagem de chamadas |
| Grafana | Visualizar métricas (≥3 painéis) |
| Airflow | Orquestrar treino/retreino |
| GitHub Actions | Automatizar verificações (CI) |
| README | Estratégia cloud (batch vs real-time) + instruções de execução |

### O que a arquitetura **não** inclui por padrão

Banco de dados, JWT/RBAC, frontend, Redis, Kubernetes, message brokers, microserviços, deploy cloud real.  
Ver FORA DO ESCOPO em `tech-challenge-requirements.md`.

---

## 3. Request Flow (inferência)

1. Cliente envia texto do laudo (JSON) para a API.
2. API valida o input.
3. Modelo classifica o texto.
4. API retorna a classificação (e métricas internas são atualizadas).
5. Prometheus coleta métricas; Grafana exibe painéis.

Contrato JSON (`text` → `label` + `confidence`): **DECISÃO DO PROJETO** (`docs/TODO.md` §0.2). Path HTTP / status codes: ainda com o Vini (sugestão `POST /predict`).

---

## 4. Training / Retrain Flow

DAG Airflow funcional relacionada a treino/retreino.

**EXEMPLO FIAP (não obrigar esta forma exata):** carregamento de dados → treino → salvamento do modelo.

Artefato de inferência: `models/baseline.joblib` (Pipeline sklearn). A DAG deve gravar no mesmo path.

---

## 5. Latency Strategy

| Fase | O que medir |
|------|-------------|
| Etapa 1 | Baseline de latência da API em Docker (modelo ainda não otimizado ou baseline definido) |
| Etapa 4 | Comparar latência do modelo **original** vs **otimizado** |

≥1 técnica de otimização: OBRIGATÓRIO.  
ONNX / quantização / pruning: EXEMPLO FIAP.  
Técnica concreta: **PROPOSTA** ONNX Runtime (Semana C) — time ainda não confirmou.

---

## 6. Cloud Strategy (documental)

**OBRIGATÓRIO:** analisar e documentar no README qual estratégia de deploy em nuvem seria adequada, incluindo **batch vs real-time**.

AWS / Azure / GCP: EXEMPLO FIAP de provedores.  
Deploy real: FORA DO ESCOPO.  
Provedor/desenho detalhado: PENDENTE DE DECISÃO (apenas para o texto do README).

Execução do desafio: **local** via Docker / Docker Compose.

---

## 7. Architectural Decisions

### Já alinhadas ao PDF (não são “preferência estética”)

- API REST com FastAPI
- Inferência em container Docker
- Observabilidade local com Prometheus + Grafana via Compose
- CI com GitHub Actions
- Orquestração de treino com Airflow
- Modelo NLP leve (sem LLM de produção obrigatório)

### Pendentes

Ver `tech-challenge-requirements.md` §15 e `docs/TODO.md` §0.2. Dataset, labels, algoritmo e path do modelo já fechados. Restam otimização (proposta ONNX), linter, cloud documental, path HTTP e layout do restante do repo.

### Trade-offs conscientes

| Escolha | Ganho | Custo aceito |
|---------|-------|--------------|
| Sem banco | Simplicidade, foco no desafio | Sem persistência de histórico de laudos |
| Sem auth | Escopo acadêmico enxuto | API não é “produção hospitalar” |
| Compose local | Cumpre monitoramento 20% | Não é cluster de produção |
| Um serviço de API | Menos complexidade | Sem microserviços |

---

## 8. Related Documentation

- **Requirements:** `.github/context/tech-challenge-requirements.md`
- **Tech Stack:** `.github/context/tech-stack.md`
- **Deployment:** `.github/context/deployment.md`
- **Project Goals:** `.github/context/project-goals.md`
