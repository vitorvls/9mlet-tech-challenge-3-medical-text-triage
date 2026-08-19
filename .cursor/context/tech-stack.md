# Technology Stack

## Objective

Stack do projeto alinhada ao Tech Challenge.  
Classificação detalhada: `.cursor/context/tech-challenge-requirements.md`.  
Dependências: `.cursor/libs/allowed-libs.md`.

Agentes **não** devem adicionar stacks paralelas (Node/Express/npm CLI, etc.).

---

## Language & Runtime

| Item | Status | Notas |
|------|--------|-------|
| Python | Stack do projeto | Ecossistema FastAPI / sklearn / Airflow |
| Versão específica do Python | DECISÃO DO PROJETO | **3.11.9** (`requires-python = "==3.11.9"` no `pyproject.toml`; venv com esse interpretador). |

---

## REQUIRED BY CHALLENGE

| Tecnologia | Papel |
|------------|--------|
| FastAPI | API REST de inferência |
| prometheus_client | Instrumentação (latência + contagem) |
| Prometheus | Coleta de métricas |
| Grafana | Dashboards (≥3 painéis) |
| Docker | Container do serviço de inferência |
| Docker Compose | API + Prometheus + Grafana juntos |
| GitHub Actions | CI/CD (≥2 automações) |
| Apache Airflow | DAG de treino/retreino |
| Scikit-Learn **ou** framework de preferência | Modelo NLP leve |

**EXEMPLO FIAP (não obrigação única):** TF-IDF + Random Forest; pytest + lint no push; ONNX / quantização / pruning; painéis de total de req / latência / taxa de erro.

---

## PROJECT DECISION

| Item | Status |
|------|--------|
| Conventional Commits para histórico semântico | Adotado como decisão interna (ver `git-rules.md`) |
| Dataset concreto | [MIMIC-III Open Access (Kaggle)](https://www.kaggle.com/datasets/ihssanened/mimic-iii-clinical-databaseopen-access) — ver `docs/TODO.md` §0.2 |
| Labels | `normal` / `atenção` / `urgente` (proxy de `admission_type`) |
| Framework/algoritmo concreto do classificador | TF-IDF + Logistic Regression (sklearn) |
| Artefato do modelo | `models/baseline.joblib` |
| Técnica concreta de otimização | PROPOSTO: ONNX Runtime (Semana C) — time ainda não confirmou |
| Linter/formatter concretos | PENDENTE |
| Empacotamento Python | `pip` + `pyproject.toml` + `.venv/` (2026-08-15). Sem Poetry/uv. |

---

## OPTIONAL / DEV TOOLING

Ferramentas úteis **somente** se decididas explicitamente:

| Área | Exemplos possíveis | Status |
|------|-------------------|--------|
| Testes | pytest (EXEMPLO FIAP) | Preferível alinhar ao exemplo do PDF; pin/versão PENDENTE |
| Lint/format | ruff, black, isort, flake8, etc. | PENDENTE DE DECISÃO — não impor sem aprovação |
| Empacotamento Python | pip + `pyproject.toml` + `.venv` | **DECISÃO DO PROJETO** — ver `pyproject.toml` |
| Runtime de otimização | onnxruntime (se ONNX for escolhido) | Condicional à decisão de otimização |

Não tratar tooling opcional como requisito FIAP.

---

## Explicitamente NÃO é a stack deste projeto

Não usar como stack padrão (legado de template / fora de escopo):

- Node.js, TypeScript, Express, npm/pnpm CLI frameworks
- ESLint, Prettier, Vitest, Playwright como stack do produto
- JWT/RBAC, ORMs, Redis, Kubernetes como requisitos
- Placeholders `Nenhum`, `templates.none`
- SetAI / `@setai/cli`

---

## Related Documentation

- **Requirements:** `.cursor/context/tech-challenge-requirements.md`
- **Allowed Libs:** `.cursor/libs/allowed-libs.md`
- **Forbidden Libs:** `.cursor/libs/forbidden-libs.md`
- **Code Style:** `.cursor/rules/code-style.md`
- **Architecture:** `.cursor/context/architecture.md`
