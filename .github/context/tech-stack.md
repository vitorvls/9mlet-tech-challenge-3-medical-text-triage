# Technology Stack

## Objective

Stack do projeto alinhada ao Tech Challenge.  
Classificação detalhada: `.github/context/tech-challenge-requirements.md`.  
Dependências: `.github/libs/allowed-libs.md`.

Agentes **não** devem adicionar stacks paralelas (Node/Express/npm CLI, etc.).

---

## Language & Runtime

| Item | Status | Notas |
|------|--------|-------|
| Python | Stack do projeto | Ecossistema FastAPI / sklearn / Airflow |
| Versão específica do Python | PENDENTE DE DECISÃO | Não fixar silenciosamente |

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
| Framework/algoritmo concreto do classificador | PENDENTE |
| Técnica concreta de otimização | PENDENTE |
| Dataset concreto | PENDENTE |
| Linter/formatter concretos | PENDENTE |

---

## OPTIONAL / DEV TOOLING

Ferramentas úteis **somente** se decididas explicitamente:

| Área | Exemplos possíveis | Status |
|------|-------------------|--------|
| Testes | pytest (EXEMPLO FIAP) | Preferível alinhar ao exemplo do PDF; pin/versão PENDENTE |
| Lint/format | ruff, black, isort, flake8, etc. | PENDENTE DE DECISÃO — não impor sem aprovação |
| Empacotamento Python | pip + requirements / poetry / uv | PENDENTE DE DECISÃO |
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

- **Requirements:** `.github/context/tech-challenge-requirements.md`
- **Allowed Libs:** `.github/libs/allowed-libs.md`
- **Forbidden Libs:** `.github/libs/forbidden-libs.md`
- **Code Style:** `.github/rules/code-style.md`
- **Architecture:** `.github/context/architecture.md`
