# GitHub Copilot Instructions — 9mlet-tech-challenge-3-medical-text-triage

Este arquivo contém as **instruções de repositório e contexto** para o GitHub Copilot e agentes de IA no projeto `9mlet-tech-challenge-3-medical-text-triage` (FIAP - Tech Challenge Fase 3).

---

## 1. Visão Geral do Projeto

O objetivo deste projeto é construir uma solução completa de **Triagem Médica por Texto (Medical Text Triage)** utilizando Machine Learning / NLP, englobando:
1. **Modelagem de IA/NLP**: Treinamento, otimização de latência/inferência e comparação de baseline vs. otimizado.
2. **API de Inferência**: FastAPI empacotada em Dockerfile.
3. **Pipeline de Treinamento/Retreino**: Orquestração via Apache Airflow (load → train → save).
4. **Monitoramento & Métricas**: `prometheus_client` exportando métricas de latência e contagem, visualizáveis em Docker Compose com Prometheus e Grafana (≥ 3 painéis).
5. **Automação CI/CD**: GitHub Actions com ≥ 2 automações (ex.: lint, test, build).
6. **Entregáveis Documentais**: `README.md` detalhado (instruções de execução + arquitetura documental cloud batch vs. tempo real) e Vídeo demonstrativo no método STAR (≤ 5 min).

---

## 2. Fonte de Verdade e Hierarquia

Ao tomar decisões ou responder a solicitações no repositório, respeite rigidamente a seguinte prioridade:

| Prioridade | Fonte de Verdade |
|------------|------------------|
| **1 (máxima)** | PDF oficial da FIAP: `MLET - Tech Challenge Fase 3.pdf` |
| **2** | `.github/context/tech-challenge-requirements.md` |
| **3** | Decisões explícitas documentadas nos arquivos de context |
| **4** | Demais arquivos da pasta `.github/` |

> **Regra em Conflito:** `PDF > requirements tipados > decisões explícitas > demais arquivos`.

---

## 3. Diretrizes Anti-Overengineering (Essencial)

- **Simplicidade Máxima**: Desenvolva a solução mais simples que cumpra os 6 critérios de avaliação da FIAP:
  - Modelagem (20%)
  - Monitoramento (20%)
  - CI/CD (15%)
  - Airflow (15%)
  - README (15%)
  - Vídeo STAR (15%)
- **Fora do Escopo Padrão**: **NÃO** introduza frontend, banco de dados relacional (PostgreSQL/MySQL), autenticação JWT/OAuth, Redis, Kubernetes ou deploy em nuvem real paga **sem** requisição explícita do usuário.
- **Isenção de Responsabilidade**: O sistema é uma ferramenta experimental para triagem de texto, não um diagnóstico médico real ou substituto de atendimento profissional.

---

## 4. Ordem Recomendada de Leitura do Contexto

Quando estiver executando tarefas no projeto, consulte os arquivos relevantes nesta ordem:

1. Este `.github/copilot-instructions.md` (Visão geral e regras do repositório)
2. [tech-challenge-requirements.md](file:///.github/context/tech-challenge-requirements.md) (Requisitos tipados OBRIGATÓRIO / EXEMPLO / PENDENTE / FORA DO ESCOPO)
3. [project-goals.md](file:///.github/context/project-goals.md) (Objetivos do projeto e critérios de avaliação)
4. [architecture.md](file:///.github/context/architecture.md) (Arquitetura-alvo da solução)
5. [tech-stack.md](file:///.github/context/tech-stack.md) (Stack técnica autorizada: Python, FastAPI, Airflow, Scikit-learn, etc.)
6. [deployment.md](file:///.github/context/deployment.md) (Instruções de Docker, Compose, Airflow e CI/CD)
7. Diretrizes e regras duras:
   - [code-style.md](file:///.github/rules/code-style.md) (Padrões de código Python / FastAPI)
   - [testing-rules.md](file:///.github/rules/testing-rules.md) (Estratégia de testes pytest)
   - [business-rules.md](file:///.github/rules/business-rules.md) (Regras de inferência e triagem)
   - [security-rules.md](file:///.github/rules/security-rules.md) (Segurança e validação)
   - [git-rules.md](file:///.github/rules/git-rules.md) (Convenções de commits)
   - [ai-usage-rules.md](file:///.github/rules/ai-usage-rules.md) (Contrato com a IA)
8. Dependências permitidas e proibidas:
   - [allowed-libs.md](file:///.github/libs/allowed-libs.md)
   - [forbidden-libs.md](file:///.github/libs/forbidden-libs.md)
   - [ai-models.md](file:///.github/libs/ai-models.md)

---

## 5. Prompts e Comandos Reutilizáveis

Os prompts pré-configurados estão disponíveis em `.github/prompts/` (e espelhados em `.github/commands/`):

- **`/kickoff-project`**: [kickoff-project.prompt.md](file:///.github/prompts/kickoff-project.prompt.md) — Iniciar etapa/tarefa alinhada com os requisitos FIAP.
- **`/architecture-review`**: [architecture-review.prompt.md](file:///.github/prompts/architecture-review.prompt.md) — Revisar a arquitetura contra os requisitos.
- **`/generate-boilerplate`**: [generate-boilerplate.prompt.md](file:///.github/prompts/generate-boilerplate.prompt.md) — Gerar código inicial mantendo alinhamento com a stack.
- **`/test-strategy`**: [test-strategy.prompt.md](file:///.github/prompts/test-strategy.prompt.md) — Criar testes unitários e de integração com pytest.
- **`/pre-delivery-validation`**: [pre-delivery-validation.prompt.md](file:///.github/prompts/pre-delivery-validation.prompt.md) — Checklist final pré-entrega do Tech Challenge.
- **`/generate-docs`**: [generate-docs.prompt.md](file:///.github/prompts/generate-docs.prompt.md) — Atualizar documentação e README.
- **`/extract-business-rules`**: [extract-business-rules.prompt.md](file:///.github/prompts/extract-business-rules.prompt.md) — Mapear regras do negócio de triagem.
- **`/refactor-controlled`**: [refactor-controlled.prompt.md](file:///.github/prompts/refactor-controlled.prompt.md) — Refatorar preservando testes e contratos.
- **`/review-pr`**: [review-pr.prompt.md](file:///.github/prompts/review-pr.prompt.md) — Auditar PR conforme normas do projeto.
- **`/challenge-solution`**: [challenge-solution.prompt.md](file:///.github/prompts/challenge-solution.prompt.md) — Criticar proposta de arquitetura/código.

---

## 6. Convenções de Código

- Linguagem: **Python 3.10+**
- Estilo: PEP 8, type hints em todas as funções publicas.
- Testes: `pytest`
- API Framework: `FastAPI` + `uvicorn`
- Docker: `docker-compose.yml` unificando API, Prometheus, Grafana e Airflow.
