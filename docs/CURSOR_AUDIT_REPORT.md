# Cursor Audit Report

**Data da auditoria:** 2026-08-05  
**Projeto:** `9mlet-tech-challenge-3-medical-text-triage`  
**Fonte de verdade principal:** `D:\Projetos\FIAP\Tech Challenge 03\MLET - Tech Challenge Fase 3.pdf`  
**Escopo auditado:** pasta `.cursor/` (27 arquivos)  
**Alterações em `.cursor`:** nenhuma (somente leitura)

---

## 1. Resumo Executivo

A pasta `.cursor` está em estado **parcialmente inicializado e fortemente contaminado por template legado**. Existe um núcleo correto de contexto de negócio em `context/project-goals.md` (e trechos espelhados em `rules/business-rules.md` e alguns commands), mas a maior parte dos arquivos técnicos ainda descreve um **CLI Node.js/TypeScript da SetAI** (`@setai/cli`, npm publish, Commander.js, Vitest, ESLint, JWT, banco `templates.none`, framework `Nenhum`).

**Alinhamento com o Tech Challenge:** baixo a médio. O problema clínico e várias restrições técnicas obrigatórias aparecem em texto corrido em poucos arquivos; **não há fonte de verdade estruturada** que separe obrigatório / exemplo FIAP / decisão do projeto / ainda não decidido. Os arquivos que um agente consultaria para implementar (architecture, tech-stack, deployment, allowed-libs, code-style) **contradizem o PDF** e o próprio `project-goals.md`.

**Pontos fortes:**
- `project-goals.md` captura bem problema, importância, non-goals e restrições técnicas do desafio.
- Separação estrutural `context/`, `rules/`, `libs/`, `commands/` é navegável.
- Não há resíduos de churn prediction nem recommender/filmes.

**Principais problemas:**
- Framework documentado como `Nenhum` em vez de FastAPI.
- Banco `templates.none`, JWT, RBAC, Express, Redis, npm — inventados ou herdados.
- `deployment.md` inteiro é publish de CLI npm (`@setai/cli`).
- `allowed-libs.md` / `forbidden-libs.md` são 100% ecossistema Node/CLI.
- Ausência de checklist estruturado dos entregáveis (DAG, Compose, Grafana ≥3 painéis, vídeo STAR, decisão cloud no README, comparação de latência).
- Exemplos do PDF (TF-IDF+RF, ONNX, lint→test→build) não estão tipados como exemplos; ONNX aparece embutido em listas de restrição sem marcar “exemplo”.

**Riscos mais importantes:**
1. Agente implementar stack Node/CLI ou exigir JWT/banco fora do escopo.
2. Agente ignorar FastAPI, Docker Compose (API+Prometheus+Grafana), Airflow e otimização de latência.
3. Superengenheirar (K8s, Redis, RBAC, escala de produção) em detrimento dos critérios avaliados.

**Nota geral da `.cursor`: 3.8/10**

---

## 2. Fonte de Verdade e Metodologia

### Fonte principal

Foi lido integralmente o PDF oficial:

`D:\Projetos\FIAP\Tech Challenge 03\MLET - Tech Challenge Fase 3.pdf` (7 páginas).

Tema central do documento: *Deploy de Modelo em Produção com Pipeline CI/CD, Monitoramento e Otimização de Latência*, no contexto de triagem automática de laudos (ex.: normal / atenção / urgente).

### Fontes secundárias de comparação

- Decisões de contexto fornecidas no prompt da auditoria (problema, usuários por inferência de produto, objetivos, fora de escopo).
- Consistência interna entre arquivos da própria `.cursor`.

### Metodologia

1. Extração dos requisitos do PDF, classificando cada item como **obrigatório**, **exemplo**, **recomendação** ou **entregável**.
2. Inventário completo dos 27 arquivos em `.cursor/` (incluindo `.setai/`).
3. Leitura integral de cada arquivo.
4. Cruzamento arquivo ↔ PDF ↔ contexto do prompt ↔ demais arquivos.
5. Identificação de contradições, inventados, ausentes, legado e riscos para agentes.
6. Atribuição de notas por arquivo conforme propósito específico (não se exige que todo arquivo contenha todos os requisitos).
7. Produção exclusiva deste relatório em `docs/CURSOR_AUDIT_REPORT.md` — **sem alteração em `.cursor`**.

### Extração condensada do PDF (checklist)

| Item | Natureza no PDF |
|------|-----------------|
| Classificador NLP leve + API REST FastAPI | Obrigatório |
| Entrada: texto do laudo; saída: classificação | Obrigatório |
| Dockerfile do serviço de inferência | Obrigatório |
| Baseline de latência local | Obrigatório (Etapa 1) |
| Scikit-Learn **ou** framework de preferência | Obrigatório (escolha livre) |
| TF-IDF + Random Forest | **Exemplo** |
| GitHub Actions; ≥2 automações | Obrigatório |
| lint → test → build / pytest + lint no push | **Exemplo** de fluxo |
| DAG Airflow treino/retreino | Obrigatório |
| load → train → save | **Exemplo** de fluxo |
| prometheus_client + Prometheus + Grafana + Docker Compose | Obrigatório |
| Métricas: tempo de requisição + contagem de chamadas | Obrigatório |
| Grafana ≥3 painéis | Obrigatório |
| total req / latência / taxa de erro | **Exemplo** de painéis |
| ≥1 técnica de otimização (ONNX, quantização, pruning) | Obrigatório; técnicas são **exemplos** |
| Comparar latência original vs otimizado | Obrigatório |
| Documentar no README estratégia cloud (batch vs real-time); AWS/Azure/GCP | Obrigatório documental; cloud real **não** exigida; provedores são **exemplos** |
| Dataset público tabular texto+target ≥2000 | **Recomendação** |
| Medical Abstracts / MIMIC-III | **Exemplos** de dataset |
| Vídeo ≤5 min método STAR | Obrigatório |
| Commits semânticos/organizados | Obrigatório |
| README com arquitetura cloud + instruções de execução | Obrigatório (critério Documentação 15%) |

**Pesos oficiais de avaliação:** Modelagem/Otimização 20% · CI/CD 15% · Airflow 15% · Monitoramento 20% · README 15% · Vídeo STAR 15%.

---

## 3. Matriz de Requisitos do Tech Challenge

| Requisito | Representado na `.cursor`? | Arquivos relacionados | Status | Observações |
|-----------|---------------------------|----------------------|--------|-------------|
| Classificador NLP leve (texto médico → urgência) | Parcial | `context/project-goals.md`, `rules/business-rules.md`, commands com descrição | PARCIAL | Presente no texto de negócio; ausente em architecture/tech-stack/libs |
| Classes exemplo normal/atenção/urgente | Sim (como exemplo de domínio) | `project-goals.md` e espelhamentos | OK | PDF usa “ex.:”; `.cursor` trata de forma adequada no goals |
| FastAPI como framework da API | Conflito | goals/business dizem FastAPI; architecture/tech-stack/code-style/commands dizem `Nenhum` | CONFLITO | Fonte de verdade técnica aponta framework inexistente |
| API recebe texto e retorna classificação | Parcial | goals, business, kickoff | PARCIAL | Não há contrato de endpoint documentado |
| Dockerfile serviço de inferência | Ausente / contradito | `deployment.md` fala npm/pkg | AUSENTE | Deploy documentado é publish npm |
| Baseline de latência local | Ausente | — | AUSENTE | Não aparece como entregável guiado |
| Scikit-Learn ou framework de preferência | Parcial | goals/business (menciona) | PARCIAL | Não está em allowed-libs/tech-stack; decisão do projeto não registrada |
| TF-IDF + RF como exemplo (não obrigação) | Ausente | — | AUSENTE | Nem como exemplo tipado; risco baixo de obrigação indevida deste item |
| GitHub Actions ≥2 automações | Parcial | goals/business; deployment menciona GA mas com npm | PARCIAL | Misturado com GitLab/CircleCI “recommended”; pipeline npm |
| lint → test → build como exemplo | Parcial/confuso | deployment (npm lint/test/build) | PARCIAL | Fluxo npm/ESLint, não Python/pytest |
| DAG Airflow treino/retreino | Parcial | goals/business/challenge-solution | PARCIAL | Só em prosa; sem orientação de estrutura/DAG |
| Fluxo load→train→save como exemplo | Ausente | — | AUSENTE | Não tipado como exemplo |
| prometheus_client + Prometheus + Grafana | Parcial | goals/business; architecture cita Grafana+Prometheus como “recommended tool” genérico | PARCIAL | Não há stack Compose como obrigação operacional |
| Docker Compose: API + Prometheus + Grafana | Ausente como requisito claro | — | AUSENTE | deployment não descreve compose médico/ML |
| Métricas: latência + contagem de chamadas | Ausente | architecture lista métricas genéricas de produção | AUSENTE | Não amarra ao prometheus_client da API |
| Grafana ≥3 painéis | Parcial (só em prosa de constraints) | goals/business | PARCIAL | Exemplos de painéis não tipados |
| ≥1 otimização de latência | Parcial | goals/business (ONNX/quant/pruning na mesma frase) | PARCIAL | Não diferencia exemplo vs obrigação; sem decisão do projeto |
| Comparação latência baseline vs otimizado | Ausente | — | AUSENTE | Entregável crítico da Etapa 4 |
| Decisão arquitetural cloud no README (batch vs RT) | Ausente | deployment “To be defined” + npm | AUSENTE | Critério 15% de documentação |
| Dataset ≥2000 (recomendação) | Ausente | — | AUSENTE | OK não obrigar; falta orientação de recomendação |
| Vídeo STAR ≤5 min (S/T/A/R) | Ausente | — | AUSENTE | 15% da nota; zero cobertura |
| Commits semânticos | Parcial | `rules/git-rules.md` (Conventional Commits) | OK | Adequado ao espírito do PDF; extras inventados (TDD no PR) |
| README com instruções de execução | Ausente na `.cursor` como planejamento | — | AUSENTE | generate-docs não prioriza README do desafio |
| Fora de escopo: não diagnóstico / sem frontend obrigatório / sem cloud real | Parcial | project-goals non-goals | PARCIAL | Contradito por JWT, DB, escala K8s em architecture/security |
| Critérios/pesos de avaliação | Ausente | — | AUSENTE | Agentes não são direcionados aos 20/15/15/20/15/15 |
| Diferenciação obrigatório vs exemplo vs decisão | Ausente | — | AUSENTE | Falha sistêmica de governança de requisitos |

---

## 4. Avaliação Individual dos Arquivos

### `.cursor/README.md`

**Nota: 5.5/10**

**Propósito identificado:** Índice de navegação da pasta `.cursor` para humanos e agentes.

**Pontos positivos:**
- Estrutura clara (`context`, `rules`, `libs`, `commands`).
- Princípios úteis (contexto explícito, regras duras, AI propõe / humano aprova).

**Problemas encontrados:**
- Não aponta o PDF do Tech Challenge como fonte de verdade.
- Não alerta que vários arquivos ainda são template SetAI/Node.
- Orienta “configure lint before starting” apontando para `code-style.md` (ESLint/Prettier/TS) — inadequado para Python/FastAPI.
- Não lista entregáveis do desafio nem critérios de avaliação.

**Requisitos ausentes ou incorretos:**
- Falta mapa “o que é obrigatório FIAP vs decisão do projeto”.
- Falta menção a FastAPI, Airflow, Prometheus/Grafana, vídeo STAR.

**Recomendação:**
- Reescrever como índice do Tech Challenge Fase 3, com link ao PDF, aviso de arquivos legados e ordem de leitura para agentes (`project-goals` → requisitos FIAP → decisões → libs Python).

---

### `.cursor/context/project-goals.md`

**Nota: 7.8/10**

**Propósito identificado:** Contexto de negócio, objetivos, restrições e non-goals.

**Pontos positivos:**
- Melhor arquivo da pasta; alinhado ao PDF e ao contexto do prompt.
- Non-goals corretos (não diagnóstico, sem UI obrigatória, sem cloud real obrigatória).
- Restrições técnicas listam FastAPI, Docker, GHA, Airflow, Prometheus/Grafana, otimização.

**Problemas encontrados:**
- Usuários finais descritos por inferência sem rótulo claro “decisão/contexto de produto, não requisito FIAP” (há nuance, mas ambígua).
- ONNX/quantização/pruning e “lint e testes” aparecem na mesma frase das restrições sem marcar **exemplo**.
- Não cobre vídeo STAR, dataset recomendado, decisão cloud no README, pesos de avaliação, comparação de latência.
- Não declara o que ainda **não foi decidido** (dataset concreto, técnica de otimização, arquitetura de pastas, etc.).

**Requisitos ausentes ou incorretos:**
- Entregáveis Etapas 1–4 incompletos.
- Critérios oficiais de avaliação ausentes.

**Recomendação:**
- Tornar este (ou um novo `tech-challenge-requirements.md`) a fonte de verdade tipada: Obrigatório / Exemplo / Recomendação / Decisão / Pendente.
- Separar restrições FIAP de decisões internas.

---

### `.cursor/context/architecture.md`

**Nota: 1.5/10**

**Propósito identificado:** Fonte de verdade da arquitetura do sistema.

**Pontos positivos:**
- Bloco inicial de Description/Users copia o domínio médico corretamente.
- Menciona estilo Layered + REST + stateless (razoável como ponto de partida).

**Problemas encontrados:**
- **Framework: `Nenhum`** — placeholder não resolvido; contradiz FastAPI obrigatório.
- **Database `templates.none` como source of truth** — inventado; PDF não exige banco.
- JWT, RBAC, Express middleware, helmet.js, zod/joi, Prisma/TypeORM, Redis, Kubernetes, circuit breaker, PagerDuty, escalas 100–10k users — **superengenharia e legado Node**.
- Package registry npm/pnpm; runtime inconsistente.
- Monitoring recomenda New Relic/Datadog; Prometheus+Grafana aparecem como opção genérica, não como stack obrigatória Compose.
- Trade-off “Nenhum over alternatives” é nonsense operacional.

**Requisitos ausentes ou incorretos:**
- Ausentes: API de inferência, modelo NLP, Docker, Airflow, Compose, otimização, baseline/comparação de latência, decisão cloud teórica.
- Incorreto: arquitetura centrada em DB + auth.

**Recomendação:**
- Reescrever do zero para arquitetura mínima do desafio: API FastAPI → modelo → métricas; Compose; DAG; CI; decisão cloud documental. Remover todo template Express/npm/DB.

---

### `.cursor/context/deployment.md`

**Nota: 0.8/10**

**Propósito identificado:** Infraestrutura e processo de deploy.

**Pontos positivos:**
- Menciona GitHub Actions como opção de CI/CD (ainda que genérico).

**Problemas encontrados:**
- Documento **inteiro** descreve publicação do pacote npm `@setai/cli`.
- Ambientes Staging/Production via tags npm; `npm link`, `npm publish`, 2FA npm.
- Monitoring = download stats / GitHub stars — irrelevante.
- Binary distribution Node (pkg/nexe).
- CI pipeline com `npm install/test/build`.
- Contradiz Docker Compose + Dockerfile exigidos pelo PDF.

**Requisitos ausentes ou incorretos:**
- Dockerfile, docker-compose (API+Prometheus+Grafana), baseline latência, decisão cloud batch vs real-time no README — **todos ausentes**.

**Recomendação:**
- Substituir por guia de execução local Docker/Compose, CI GHA Python, e seção de **estratégia teórica de cloud** (não deploy real obrigatório).

---

### `.cursor/context/tech-stack.md`

**Nota: 1.2/10**

**Propósito identificado:** Stack tecnológica do projeto.

**Pontos positivos:**
- Language: Python (correto).

**Problemas encontrados:**
- Runtime: `Node.js (if applicable)` — inconsistente.
- Version: `0.0.1` sem sentido como versão de runtime.
- Framework: `Nenhum`; Database: `templates.none`.
- Ferramentas: ESLint, Prettier, TypeScript, Vitest/Jest, Playwright — stack JS.
- Não lista FastAPI, scikit-learn (ou escolha), prometheus_client, Airflow, Docker, Grafana, Prometheus, onnxruntime/etc., pytest, ruff/black.

**Requisitos ausentes ou incorretos:**
- Quase toda a stack obrigatória do PDF ausente.

**Recomendação:**
- Reescrever com stack Python do desafio; marcar opcionais vs obrigatórios; registrar decisões pendentes.

---

### `.cursor/rules/business-rules.md`

**Nota: 5.0/10**

**Propósito identificado:** Regras de negócio mandatórias.

**Pontos positivos:**
- Contexto do projeto e non-goals alinhados ao goals/PDF.
- Validação de input e tratamento de erro são razoáveis.

**Problemas encontrados:**
- “All requests must be authenticated (unless public endpoint)” — **inventado**; conflita com non-goals e com o PDF.
- Rules 1–4 misturam DB transactions, caching, auth com texto colado das technical constraints (uso incorreto de “performance requirements”).
- Edge cases falam de rate limiting/quotas/transactions sem base no desafio.
- Não define regras de domínio da classificação (texto vazio, labels válidos, formato de resposta).

**Requisitos ausentes ou incorretos:**
- Regras de classificação de urgência / contrato da API ausentes.
- Auth obrigatória inventada.

**Recomendação:**
- Substituir regras genéricas de API/CRUD por regras do domínio de triagem + validações da API de inferência; marcar auth como não exigida pela FIAP.

---

### `.cursor/rules/ai-usage-rules.md`

**Nota: 4.0/10**

**Propósito identificado:** Governança de uso de IA no desenvolvimento.

**Pontos positivos:**
- Princípios sólidos (IA não decide sozinha; código gerado entra em review/testes).
- Proibições de decisões de segurança/financeiras sem humano são úteis.

**Problemas encontrados:**
- “Mandatory Standardization” exige ESLint, Prettier, TypeScript, `package.json` — **bloqueia uso de IA** em projeto Python.
- Modelos recomendados desalinhados/irrelevantes ao desafio.
- Não instrui a priorizar requisitos do Tech Challenge / pesos de avaliação.
- Não proíbe inventar requisitos médicos/diagnóstico.

**Requisitos ausentes ou incorretos:**
- Gate de lint JS incorreto.
- Falta regra: validar contra PDF antes de implementar.

**Recomendação:**
- Trocar pré-requisitos para tooling Python (ruff/black/pytest conforme decisão do projeto); adicionar “não contradizer o PDF”.

---

### `.cursor/rules/security-rules.md`

**Nota: 2.5/10**

**Propósito identificado:** Regras de segurança mandatórias.

**Pontos positivos:**
- Não commit de secrets, validação de input, não expor stack traces — práticas válidas em geral.

**Problemas encontrados:**
- Define **JWT como método de autenticação do projeto** — inventado.
- Stack Express (helmet, express-rate-limit, express-validator), Prisma/TypeORM, zod/joi.
- Database `templates.none`.
- File uploads, XSS de frontend, SQL injection como foco principal — desalinhados ao serviço de inferência sem DB obrigatório.
- Checklist “before deploying” assume produção autenticada.

**Requisitos ausentes ou incorretos:**
- Não cobre cuidados de dados médicos/texto de laudo em logs (parcialmente em “não logar PII”, mas fraco).
- Auth/DB apresentados como obrigatórios sem base no PDF.

**Recomendação:**
- Reduzir a regras mínimas: validação de payload, secrets, não logar conteúdo sensível de laudos, dependências; marcar JWT/RBAC/DB como fora do escopo FIAP salvo decisão explícita.

---

### `.cursor/rules/git-rules.md`

**Nota: 6.5/10**

**Propósito identificado:** Commits, branches e PRs.

**Pontos positivos:**
- Conventional Commits alinham-se a “histórico semântico” do PDF.
- Proíbe force push, secrets, commit direto em main.

**Problemas encontrados:**
- Exemplo `feat(auth): add JWT authentication` reforça auth inventada.
- Exige TDD no checklist de PR (não é requisito FIAP).
- Branch `develop`, limites de tamanho de PR, rebase proibido — regras internas rígidas sem vínculo ao desafio.
- “No console.logs” residual de JS.

**Requisitos ausentes ou incorretos:**
- Nenhum requisito FIAP crítico ausente neste arquivo (escopo é git).

**Recomendação:**
- Manter Conventional Commits; suavizar TDD/JWT; exemplos do domínio (predict/inference/metrics).

---

### `.cursor/rules/testing-rules.md`

**Nota: 3.5/10**

**Propósito identificado:** Estratégia e regras de teste.

**Pontos positivos:**
- Pirâmide de testes e AAA são conceitos válidos.
- Menciona pytest-cov como opção de coverage.

**Problemas encontrados:**
- **TDD obrigatório** com linguagem CRITICAL — inventado; pode atrasar entrega do desafio.
- Exemplos em TypeScript; naming `*.test.ts`.
- Placeholder `{{TEST_COVERAGE}}` não resolvido; depois exige 70/100/80/90% — inventado.
- Integração com DB/auth flows como foco.
- E2E browser — fora do escopo típico do desafio (sem frontend obrigatório).

**Requisitos ausentes ou incorretos:**
- Não prioriza testes simples de API/modelo exigidos pelo exemplo do PDF (pytest).
- Não menciona testes de latência/comparação como evidência da Etapa 4 (decisão útil, não obrigação tipada no PDF como suite).

**Recomendação:**
- pytest como padrão; TDD como opcional/recomendado interno; coberturas realistas; foco em API + classificação + regressão de contrato.

---

### `.cursor/rules/code-style.md`

**Nota: 2.0/10**

**Propósito identificado:** Padrões mandatórios de código.

**Pontos positivos:**
- Projeto identificado como Python.
- Regra código EN / comentários pt-BR pode ser decisão interna válida se consistente.

**Problemas encontrados:**
- Framework: `Nenhum`.
- Bloqueia desenvolvimento sem ESLint/Prettier/TypeScript/`package.json`.
- Naming mistura camelCase JS com Python.
- Proíbe “untyped code” / `any` — viés TypeScript.
- Contradiz stack Python do desafio.

**Requisitos ausentes ou incorretos:**
- Tooling Python (ruff, black, isort, mypy — se forem decisão) ausente.
- Gate incorreto impede começar o projeto “corretamente” segundo as próprias regras.

**Recomendação:**
- Reescrever para Python/FastAPI; remover bloqueio ESLint/TS.

---

### `.cursor/libs/allowed-libs.md`

**Nota: 0.5/10**

**Propósito identificado:** Lista branca de dependências.

**Pontos positivos:**
- Estrutura (lib → reason → use case) é boa.

**Problemas encontrados:**
- Conteúdo 100% CLI Node: Commander, Inquirer, fs-extra, Handlebars, chalk, ora, Vitest, tsup, pnpm.
- **Nenhuma** lib obrigatória do PDF (FastAPI, scikit-learn, prometheus_client, Airflow, etc.).

**Requisitos ausentes ou incorretos:**
- Todas as bibliotecas requeridas pelo PDF ausentes.

**Recomendação:**
- Substituir integralmente pela allowlist Python do desafio + opcionais tipados.

---

### `.cursor/libs/forbidden-libs.md`

**Nota: 0.5/10**

**Propósito identificado:** Lista negra de dependências.

**Pontos positivos:**
- Processo de aprovação documentado.

**Problemas encontrados:**
- Proíbe Yargs/Meow em favor de Commander — irrelevante.
- “Axios NOT ALLOWED (CLI doesn't make HTTP requests)” — domínio errado.
- Prefere Vitest; rejeita Mocha — stack errada.
- Pode induzir agente a rejeitar libs Python legítimas por ausência na allowlist cruzada.

**Requisitos ausentes ou incorretos:**
- Não protege contra libs fora do escopo médico/diagnóstico; protege contra alternativas de CLI.

**Recomendação:**
- Reescrever: proibir frameworks web JS, ORMs/DB desnecessários, libs de diagnóstico clínico inventadas; permitir stack do PDF.

---

### `.cursor/libs/ai-models.md`

**Nota: 4.5/10**

**Propósito identificado:** Quais modelos de IA usar em cada fase de desenvolvimento assistido.

**Pontos positivos:**
- Separação por fase (arquitetura, implementação, debug) é útil.
- Reforça review humano.

**Problemas encontrados:**
- Stack header: `Python + Nenhum + templates.none`.
- Não diferencia modelos de **LLM de desenvolvimento** do **modelo NLP do produto** — risco semântico de ambiguidade para agentes (“ai-models”).
- Irrelevante ao cumprimento direto do PDF.

**Requisitos ausentes ou incorretos:**
- Não lista o classificador do produto (scikit-learn/etc.) — e talvez não deva; mas o nome do arquivo induz confusão.

**Recomendação:**
- Renomear/clarear “LLM assistants for coding”; remover Nenhum/templates.none; apontar decisões do modelo de produto em tech-stack.

---

### `.cursor/commands/kickoff-project.md`

**Nota: 4.5/10**

**Propósito identificado:** Prompt de alinhamento inicial de negócio/arquitetura.

**Pontos positivos:**
- Embedding correto de problema, goals e constraints técnicas do desafio.
- Constraints “don't generate code” adequadas ao kickoff.

**Problemas encontrados:**
- Stack: `Python + Nenhum + templates.none`.
- Project-Specific Notes: focar em DB operations + authentication — **induz fora de escopo**.
- Não pede diferenciação obrigatório/exemplo/decisão.
- Não referencia pesos STAR/avaliação.

**Recomendação:**
- Remover auth/DB; pedir checklist do PDF e lista de pendências de decisão.

---

### `.cursor/commands/architecture-review.md`

**Nota: 3.5/10**

**Propósito identificado:** Validar decisões arquiteturais.

**Pontos positivos:**
- Contexto de negócio correto no header.
- Foco em trade-offs e acoplamento é útil.

**Problemas encontrados:**
- Stack Nenhum + templates.none.
- Notes: “database interactions”, “scalability” genérica — risco de overengineering.
- Não valida contra entregáveis Compose/Airflow/otimização/cloud README.

**Recomendação:**
- Checklist de conformidade com Etapas 1–4 e pesos; flag de overengineering como critério explícito.

---

### `.cursor/commands/extract-business-rules.md`

**Nota: 6.0/10**

**Propósito identificado:** Extrair regras de negócio explícitas/implícitas.

**Pontos positivos:**
- Contexto e goals corretos.
- Boa estrutura de saída (explícitas / implícitas / ambíguas).

**Problemas encontrados:**
- Não instrui a separar regra FIAP vs decisão de produto vs inventada.
- Sem âncora no PDF.

**Recomendação:**
- Exigir classificação de cada regra por origem (PDF / decisão / código / ambígua).

---

### `.cursor/commands/test-strategy.md`

**Nota: 4.0/10**

**Propósito identificado:** Planejar estratégia de testes.

**Pontos positivos:**
- Estrutura de cenários/unit/integration/edge cases.

**Problemas encontrados:**
- Stack Nenhum + templates.none.
- TDD mandatory reforçado.
- Não prioriza pytest/API/modelo do desafio.

**Recomendação:**
- Alinhar a testing-rules corrigidas; incluir testes de contrato da API e smoke da stack Compose como opcional útil.

---

### `.cursor/commands/generate-boilerplate.md`

**Nota: 3.0/10**

**Propósito identificado:** Gerar boilerplate conforme padrões.

**Pontos positivos:**
- “Don't introduce new abstractions” — bom antídoto a overengineering.

**Problemas encontrados:**
- Aponta para allowed-libs/code-style **errados** → boilerplate Node/CLI ou inválido.
- Stack Nenhum + templates.none.
- Sem template alvo (FastAPI app, Dockerfile, compose, DAG).

**Recomendação:**
- Só reativar após corrigir libs/architecture; listar boilerplates permitidos do desafio.

---

### `.cursor/commands/refactor-controlled.md`

**Nota: 6.5/10**

**Propósito identificado:** Refatoração sem mudança de comportamento.

**Pontos positivos:**
- Constraints corretas (não alterar comportamento; manter testes).
- Pouco acoplado a requisitos inventados além do header de stack.

**Problemas encontrados:**
- Header `Nenhum + templates.none`.
- Depende de code-style incorreto.

**Recomendação:**
- Corrigir stack no header; manter o restante.

---

### `.cursor/commands/generate-docs.md`

**Nota: 4.5/10**

**Propósito identificado:** Gerar documentação técnica de módulos.

**Pontos positivos:**
- Estrutura responsibility/data flow/dependencies/decisions.

**Problemas encontrados:**
- Não prioriza README exigido (cloud + instruções de execução).
- Não cobre roteiro do vídeo STAR nem comparação de latência.
- Stack placeholder.

**Recomendação:**
- Adicionar modo “Tech Challenge README + evidências Etapas 1–4”.

---

### `.cursor/commands/review-pr.md`

**Nota: 5.5/10**

**Propósito identificado:** Review de PR educacional.

**Pontos positivos:**
- Critérios de clareza, regras de negócio, testes e impacto futuro.

**Problemas encontrados:**
- TDD mandatory; stack placeholder.
- Não verifica conformidade com requisitos do desafio (métricas, Docker, etc.).

**Recomendação:**
- Incluir checklist FIAP no review.

---

### `.cursor/commands/challenge-solution.md`

**Nota: 6.8/10**

**Propósito identificado:** Desafiar soluções propostas (anti-bias / anti-overengineering).

**Pontos positivos:**
- Constraints técnicas do desafio corretamente embutidas.
- Foco explícito em overengineering e alternativas mais simples — **muito alinhado** ao risco atual da `.cursor`.

**Problemas encontrados:**
- Stack `Nenhum + templates.none` no header.
- Não tipifica exemplos vs obrigatórios dentro das constraints.
- Nome “challenge-solution” pode ser confundido com “resolver o Tech Challenge” vs “desafiar a solução”.

**Recomendação:**
- Corrigir stack; renomear ou esclarecer propósito; usar como comando P0 após limpeza.

---

### `.cursor/commands/pre-deploy-validation.md`

**Nota: 3.0/10**

**Propósito identificado:** Validação final pré-deploy.

**Pontos positivos:**
- Inclui observabilidade (logs/métricas/monitoring) — relevante.

**Problemas encontrados:**
- Assume deploy de produção com auth/authorization.
- Aponta para `deployment.md` npm/SetAI.
- Não valida entregáveis do desafio (Compose up, 3 painéis Grafana, DAG, vídeo, comparação latência, texto cloud no README).

**Recomendação:**
- Transformar em “pre-delivery validation” do Tech Challenge (checklist das 4 etapas + STAR).

---

### `.cursor/.setai/README.md`

**Nota: 2.0/10**

**Propósito identificado:** Documentar configuração do gerador SetAI CLI usado para criar a estrutura.

**Pontos positivos:**
- Explica origem da pasta.
- Alerta para não commitar secrets.

**Problemas encontrados:**
- Legado puro; sem relação com triagem médica.
- Pode confundir agentes sobre o que é o “projeto”.
- Afirma conter API keys reais; no `config.json` local há placeholders (`anthropic-key`), mas a mensagem é alarmante.

**Recomendação:**
- Remover do contexto ativo dos agentes ou isolar; não usar como fonte de arquitetura.

---

### `.cursor/.setai/config.json`

**Nota: 3.0/10**

**Propósito identificado:** Configuração do SetAI (keys/idioma).

**Pontos positivos:**
- Idioma questions pt-BR / files en — consistente com code-style de comentários.
- Keys aparentam placeholders, não segredos reais.

**Problemas encontrados:**
- Irrelevante ao Tech Challenge.
- Risco de alguém colar keys reais depois.

**Recomendação:**
- Manter fora do git; não referenciar em rules/context do produto.

---

### `.cursor/.setai/.gitignore`

**Nota: 7.0/10**

**Propósito identificado:** Ignorar `config.json` com possíveis secrets.

**Pontos positivos:**
- Ignora `config.json` corretamente.
- Comentários claros.

**Problemas encontrados:**
- Não ignora a pasta inteira; README ainda versionável (ok).
- Propósito legado SetAI.

**Recomendação:**
- Aceitável como hygiene; opcionalmente ignorar toda `.setai/` se não for necessária.

---

## 5. Contradições Encontradas

### `.cursor` vs PDF

| Conflito | Arquivos | Detalhe |
|----------|----------|---------|
| Framework da API | `architecture.md`, `tech-stack.md`, `code-style.md`, commands vs PDF | PDF exige FastAPI; `.cursor` diz `Nenhum` |
| Persistência | `architecture.md`, `security-rules.md` vs PDF | PDF não exige DB; `.cursor` define DB como source of truth |
| Deploy | `deployment.md` vs PDF | PDF: Docker/Compose; `.cursor`: npm publish `@setai/cli` |
| Auth | `security-rules.md`, `business-rules.md`, `architecture.md` vs PDF | JWT/RBAC obrigatórios na `.cursor`; ausentes no PDF |
| Stack de libs | `allowed-libs.md` vs PDF | Node/CLI vs Python/ML/API |
| Monitoramento | `deployment.md` / architecture genérica vs PDF | PDF obriga Prometheus+Grafana+Compose; deployment monitora npm downloads |
| Tooling | `code-style.md`, `ai-usage-rules.md` vs PDF | ESLint/TS obrigatórios vs projeto Python |

### Arquivo vs arquivo

| Conflito | Arquivos |
|----------|----------|
| FastAPI vs Nenhum | `project-goals.md` / `business-rules.md` vs `architecture.md` / `tech-stack.md` / commands |
| Sem cloud real / sem auth complexa (non-goals) vs JWT+RBAC+produção | `project-goals.md` vs `security-rules.md` / `architecture.md` / `pre-deploy-validation.md` |
| Python vs Node/npm | `project-goals.md` (Python implícito via FastAPI) / language Python vs `deployment.md`, `allowed-libs.md`, `tech-stack.md` |
| Sem DB (non-goals implícito) vs DB transactions | `project-goals.md` vs `business-rules.md` Rule 1 |
| CI GitHub Actions obrigatório vs “GA recommended / GitLab / CircleCI” | goals vs `architecture.md` / `deployment.md` |
| TDD mandatory vs PDF (pytest como exemplo, não TDD) | `testing-rules.md` vs PDF |

### Requisito vs decisão arquitetural

- Autenticação, banco, Redis, K8s, npm CLI e TDD estão tratados como **regras duras**, não como decisões opcionais documentadas.
- Técnica de otimização e dataset **não** estão decididos, mas ONNX aparece embutido em listas de “restrições” sem status.

### Escopo vs implementação sugerida

- Non-goals dizem não construir sistema hospitalar/produção cloud; architecture sugere escala horizontal, on-call, PagerDuty, read replicas.

---

## 6. Requisitos Obrigatórios Ausentes

Itens do PDF **não adequadamente representados** como orientação operacional na `.cursor`:

1. **Dockerfile funcional** do serviço de inferência como entregável guiado.
2. **Medição de baseline de latência local** (Etapa 1).
3. **Docker Compose** subindo API + Prometheus + Grafana juntos.
4. Instrumentação explícita com **prometheus_client** (latência + contagem).
5. **Dashboard Grafana ≥3 painéis** como requisito (com exemplos tipados).
6. **DAG Airflow** com orientação mínima de estrutura (exemplo load→train→save tipado).
7. **Workflow GitHub Actions** Python (lint/test) com ≥2 automações — tipado corretamente.
8. **Otimização de latência** com decisão do projeto + **comparação original vs otimizado**.
9. **Documentação no README** da estratégia cloud (batch vs real-time); provedores como exemplos.
10. **Vídeo STAR ≤5 min** com estrutura S/T/A/R.
11. **Critérios e pesos de avaliação** para priorização do desenvolvimento.
12. **Fonte de verdade tipada** obrigatório vs exemplo vs recomendação vs decisão.
13. Stack/libs **FastAPI / sklearn-or-choice / prometheus_client / Airflow** em `tech-stack` e `allowed-libs`.
14. Instruções claras de execução do projeto como objetivo documental (README).

Dataset ≥2000: é **recomendação** do PDF — ausência é falha de orientação, não de requisito estrito.

---

## 7. Requisitos ou Restrições Inventadas

Tratados como obrigatórios/mandatórios na `.cursor` **sem base no PDF**:

| Item inventado | Onde aparece |
|----------------|--------------|
| Framework `Nenhum` | architecture, tech-stack, code-style, commands, ai-models |
| Database `templates.none` como source of truth | architecture, tech-stack, security |
| JWT authentication obrigatória | architecture, security, business-rules, git examples |
| RBAC / roles admin-user-guest | architecture, security |
| Express / helmet / express-rate-limit / opossum | architecture, security |
| Redis cache, CDN, Kubernetes auto-scaling | architecture |
| Escalas de usuários/RPM/data volume | architecture |
| TDD obrigatório (CRITICAL) | testing-rules, git-rules, test-strategy, review-pr |
| Coberturas mínimas 70/100/80/90% | testing-rules |
| ESLint + Prettier + TypeScript + package.json como gate | code-style, ai-usage-rules, README |
| Deploy via npm publish `@setai/cli` | deployment |
| Stack CLI: Commander, Inquirer, Vitest, tsup, pnpm | allowed/forbidden libs |
| Auth em todas as requests | business-rules |
| DB transactions / optimistic locking | business-rules |
| Branch `develop`, limites rígidos de PR, rebase proibido | git-rules |
| Modelos LLM específicos como política dura do projeto | ai-usage-rules, ai-models |
| E2E browser / Playwright | tech-stack, testing-rules |
| Package registry npm | architecture, deployment |

**Observação:** Conventional Commits, validação de input e não commit de secrets são práticas internas aceitáveis; o problema é quando se misturam com obrigações inventadas que desviam do desafio.

**Sobre exemplos do PDF:** ONNX/quantização/pruning e “lint e testes” aparecem em `project-goals`/`business-rules` dentro de “restrições técnicas” sem label **exemplo** — risco de agentes tratarem ONNX (ou lint específico) como única opção válida. Não é inventar requisito novo, mas **endurecer exemplo**.

---

## 8. Conteúdo Legado ou Irrelevante

### Resíduos SetAI / CLI Node.js (crítico)

- `.cursor/.setai/*` — gerador SetAI.
- `.cursor/context/deployment.md` — `@setai/cli`, npm tags, npm audit/publish.
- `.cursor/libs/allowed-libs.md` e `forbidden-libs.md` — CLI TypeScript.
- Placeholders `Nenhum`, `templates.none` — template não preenchido.

### Resíduos Node/Express/TypeScript

- ESLint, Prettier, Vitest, Jest, tsconfig, package.json gates.
- Express middleware, helmet.js, zod/joi, Prisma/TypeORM.
- Exemplos `*.test.ts`, `calculateTotal.ts`.

### Não encontrado (positivo)

- Não há referências a **churn**, **churn prediction**, **movie recommendation**, **recommender systems** ou recomendações de filmes.
- Domínio médico de triagem aparece nos arquivos de goals/business (correto).

### Template genérico de “API REST enterprise”

- architecture.md seções 4–7 (cache, RBAC, circuit breaker, PagerDuty) — herdado de boilerplate genérico, não do Tech Challenge 3.

---

## 9. Riscos para Agentes de IA

| Risco | Severidade | Causa | Efeito provável |
|-------|------------|-------|-----------------|
| Implementar CLI npm / Node em vez de FastAPI+Docker | **CRÍTICO** | deployment, allowed-libs, tech-stack | Descumprimento total do desafio |
| Usar framework `Nenhum` / falhar ao escolher FastAPI | **CRÍTICO** | architecture, tech-stack, code-style, commands | API inválida para avaliação |
| Introduzir JWT + DB + RBAC como MVP | **CRÍTICO** | security, architecture, business-rules, kickoff notes | Fora de escopo; atraso nos 70%+ de pesos técnicos |
| Ignorar Compose Prometheus+Grafana | **CRÍTICO** | ausência + deployment errado | Perde 20% (Monitoramento) |
| Ignorar Airflow DAG | **ALTO** | só prosa, sem comando/estrutura | Perde 15% |
| Ignorar otimização + comparação de latência | **ALTO** | ausência estruturada | Perde parte de 20% Modelagem |
| Ignorar vídeo STAR e README cloud | **ALTO** | ausência total | Perde até 30% combinados |
| Confundir ONNX como única otimização permitida | **MÉDIO** | constraints sem tipagem de exemplo | Pode ser ok se ONNX for escolhido; engessa alternativas válidas |
| Bloquear desenvolvimento por falta de ESLint/TS | **ALTO** | code-style, ai-usage-rules | Agente perde tempo em tooling JS |
| Aplicar TDD rígido e coberturas altas antes dos entregáveis | **MÉDIO** | testing-rules | Atraso; não é critério do PDF |
| Superengenheirar (K8s, Redis, APM comercial) | **ALTO** | architecture.md | Complexidade sem nota |
| Tratar usuários hospitalares como requisito FIAP | **BAIXO** | project-goals/users | Risco documental menor |
| Interpretar sistema como diagnóstico médico | **MÉDIO** | fraco se agent ignorar non-goals; non-goals existem | Mitigado parcialmente por project-goals |
| Usar allowed-libs e rejeitar FastAPI/sklearn | **CRÍTICO** | allowed/forbidden libs | Dependências corretas “proibidas” por omissão |
| Seguir pre-deploy com auth obrigatória | **MÉDIO** | pre-deploy-validation | Retrabalho de segurança desnecessária |
| Confundir `ai-models.md` com modelo NLP do produto | **MÉDIO** | nome/conteúdo | Decisões erradas de modelagem |

---

## 10. Recomendações Priorizadas

### P0 — Crítico

1. **Criar fonte de verdade única tipada** (ex.: `context/tech-challenge-requirements.md`) com colunas: Obrigatório / Exemplo FIAP / Recomendação / Decisão do projeto / Pendente — espelhando o PDF e os pesos.
2. **Reescrever** `architecture.md`, `tech-stack.md`, `deployment.md` removendo SetAI/npm/Nenhum/templates.none/JWT/DB.
3. **Substituir** `allowed-libs.md` e `forbidden-libs.md` pela stack Python do desafio.
4. **Corrigir** `code-style.md` e `ai-usage-rules.md` para tooling Python (sem gate ESLint/TS).
5. **Corrigir** `security-rules.md` e trechos de auth em `business-rules.md` / kickoff notes.
6. **Documentar entregáveis ausentes:** Compose, métricas, Grafana ≥3, DAG, baseline+comparação latência, README cloud, vídeo STAR.
7. **Alinhar headers** de todos os commands: remover `Nenhum + templates.none`; colocar `Python + FastAPI`.

### P1 — Importante

1. Expandir `project-goals.md` com critérios de avaliação e lista do que ainda não foi decidido (dataset, técnica de otimização, layout de pastas).
2. Tipificar explicitamente exemplos do PDF (TF-IDF+RF, ONNX, painéis, fluxo lint→test→build, datasets).
3. Transformar `pre-deploy-validation.md` em checklist de **pré-entrega FIAP**.
4. Ajustar `generate-docs.md` para priorizar README do desafio.
5. Suavizar TDD/coberturas em `testing-rules.md` para “recomendado interno” vs obrigatório FIAP.
6. Isolar ou remover `.setai/` do contexto ativo dos agentes.
7. Atualizar `.cursor/README.md` com ordem de leitura e aviso de legado até limpeza concluir.

### P2 — Melhoria

1. Reduzir duplicação do parágrafo longo de constraints/users entre goals, business-rules e commands (single source + referências).
2. Renomear/clarear `challenge-solution.md` vs solução do Tech Challenge.
3. Renomear `ai-models.md` para evitar confusão com modelo NLP.
4. Exemplos de Conventional Commits no domínio de inferência/métricas.
5. Diagramas mínimos (Mermaid) da stack Compose + fluxo de inferência em architecture.
6. Remover placeholders `{{TEST_COVERAGE}}` e “[To be defined]” órfãos após decisões.

---

## 11. Ranking dos Arquivos

| Arquivo | Nota /10 | Status | Prioridade de revisão |
|---------|----------|--------|----------------------|
| `.cursor/context/project-goals.md` | 7.8 | Bom | P1 |
| `.cursor/.setai/.gitignore` | 7.0 | Bom | P2 |
| `.cursor/commands/challenge-solution.md` | 6.8 | Aceitável | P1 |
| `.cursor/rules/git-rules.md` | 6.5 | Aceitável | P2 |
| `.cursor/commands/refactor-controlled.md` | 6.5 | Aceitável | P2 |
| `.cursor/commands/extract-business-rules.md` | 6.0 | Aceitável | P1 |
| `.cursor/README.md` | 5.5 | Fraco | P1 |
| `.cursor/commands/review-pr.md` | 5.5 | Fraco | P1 |
| `.cursor/rules/business-rules.md` | 5.0 | Fraco | P0 |
| `.cursor/commands/generate-docs.md` | 4.5 | Fraco | P1 |
| `.cursor/commands/kickoff-project.md` | 4.5 | Fraco | P0 |
| `.cursor/libs/ai-models.md` | 4.5 | Fraco | P2 |
| `.cursor/rules/ai-usage-rules.md` | 4.0 | Fraco | P0 |
| `.cursor/commands/test-strategy.md` | 4.0 | Fraco | P1 |
| `.cursor/rules/testing-rules.md` | 3.5 | Crítico | P0 |
| `.cursor/commands/architecture-review.md` | 3.5 | Crítico | P0 |
| `.cursor/.setai/config.json` | 3.0 | Crítico* | P2 (isolar) |
| `.cursor/commands/generate-boilerplate.md` | 3.0 | Crítico | P0 |
| `.cursor/commands/pre-deploy-validation.md` | 3.0 | Crítico | P0 |
| `.cursor/rules/security-rules.md` | 2.5 | Crítico | P0 |
| `.cursor/rules/code-style.md` | 2.0 | Crítico | P0 |
| `.cursor/.setai/README.md` | 2.0 | Crítico* | P1 (isolar) |
| `.cursor/context/architecture.md` | 1.5 | Crítico | P0 |
| `.cursor/context/tech-stack.md` | 1.2 | Crítico | P0 |
| `.cursor/context/deployment.md` | 0.8 | Crítico | P0 |
| `.cursor/libs/allowed-libs.md` | 0.5 | Crítico | P0 |
| `.cursor/libs/forbidden-libs.md` | 0.5 | Crítico | P0 |

\*Crítico por irrelevância/risco de contexto, não por erro de segurança imediato no conteúdo atual do `config.json` (placeholders).

**Legenda de faixas:** 9.0–10 Excelente · 8.0–8.9 Muito bom · 7.0–7.9 Bom · 6.0–6.9 Aceitável · 5.0–5.9 Fraco · &lt;5.0 Crítico.

**Nenhum arquivo atingiu 9+:** mesmo `project-goals.md` omite entregáveis e tipagem obrigatório/exemplo.

---

## 12. Veredito Final

**A pasta `.cursor` está pronta para orientar o desenvolvimento do Tech Challenge?**

### NÃO

**Justificativa:** Um agente novo que seguir a `.cursor` como sistema de contexto encontraria o domínio médico correto em `project-goals.md`, mas seria imediatamente desviado por `architecture.md`, `tech-stack.md`, `deployment.md` e `libs/*` para um mundo Node/SetAI/npm com JWT, banco e framework `Nenhum`. Isso contradiz o PDF (FastAPI, Docker, Compose Prometheus+Grafana, Airflow, otimização de latência) e os non-goals do próprio projeto. Faltam ainda orientação estruturada para vídeo STAR, decisão cloud no README, comparação de latência e pesos de avaliação. Enquanto os arquivos P0 não forem reescritos e uma fonte de verdade tipada não existir, a `.cursor` é **mais perigosa do que útil** para implementação assistida por IA.

**Estado recomendado após correções:** meta de veredito futuro = **SIM, COM AJUSTES** assim que P0 for aplicado; **SIM** somente após tipagem obrigatório/exemplo/decisão e commands alinhados.

---

## Apêndice A — Inventário completo (27 arquivos)

```
.cursor/README.md
.cursor/context/architecture.md
.cursor/context/deployment.md
.cursor/context/project-goals.md
.cursor/context/tech-stack.md
.cursor/rules/ai-usage-rules.md
.cursor/rules/business-rules.md
.cursor/rules/code-style.md
.cursor/rules/git-rules.md
.cursor/rules/security-rules.md
.cursor/rules/testing-rules.md
.cursor/libs/ai-models.md
.cursor/libs/allowed-libs.md
.cursor/libs/forbidden-libs.md
.cursor/commands/architecture-review.md
.cursor/commands/challenge-solution.md
.cursor/commands/extract-business-rules.md
.cursor/commands/generate-boilerplate.md
.cursor/commands/generate-docs.md
.cursor/commands/kickoff-project.md
.cursor/commands/pre-deploy-validation.md
.cursor/commands/refactor-controlled.md
.cursor/commands/review-pr.md
.cursor/commands/test-strategy.md
.cursor/.setai/README.md
.cursor/.setai/config.json
.cursor/.setai/.gitignore
```

Todos os arquivos acima foram lidos integralmente nesta auditoria.

## Apêndice B — Confirmações de execução

- [x] PDF oficial lido integralmente antes da avaliação.
- [x] Inventário completo de `.cursor` realizado.
- [x] Nenhum arquivo em `.cursor` foi modificado.
- [x] Relatório criado em `docs/CURSOR_AUDIT_REPORT.md`.

---

*Fim do Cursor Audit Report.*
