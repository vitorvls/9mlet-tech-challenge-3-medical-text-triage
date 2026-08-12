# Forbidden / Discouraged Libraries

## Objective

Impedir stacks paralelas e dependências claramente incompatíveis com o Tech Challenge.  
**Não** é uma lista de preferências pessoais arbitrárias.

Regra geral: se não está na allowlist e não é REQUIRED BY CHALLENGE, **não adicionar** sem decisão explícita.

---

## 1. Stacks paralelas (não usar para este produto)

Estas tecnologias **não** devem ser a base da API/modelo deste desafio:

| Tecnologia | Motivo |
|------------|--------|
| Express / Nest / frameworks Node para a API | API deve ser FastAPI (Python) |
| Commander.js, Inquirer, CLI npm frameworks | Legado de template CLI; domínio errado |
| SetAI / `@setai/cli` como arquitetura do produto | Tooling externo legado; sem autoridade |
| Vitest / Jest / Mocha como suite principal | Projeto Python; pytest é o caminho natural do PDF |
| ESLint / Prettier / TypeScript como gate do projeto | Tooling JS; não se aplica |

Mencionar essas tecnologias **apenas** para proibir/rejeitar legado é permitido.

---

## 2. Complexidade fora de escopo (não introduzir sem decisão + justificativa)

Não são “proibidas para sempre”, mas **proibidas como default / sem ADR**:

- ORMs e bancos (Prisma, TypeORM, SQLAlchemy “por padrão”, etc.) quando não há requisito de DB
- Clientes JWT/OAuth como requisito de MVP
- Redis, Celery “enterprise”, Kubernetes clients, service meshes
- Frameworks de frontend (React/Vue/etc.) como entrega do desafio
- APM comercial obrigatório (Datadog/New Relic) no lugar de Prometheus+Grafana

Se algum item for necessário no futuro: documentar como **DECISÃO DO PROJETO** com justificativa e atualizar requirements/architecture.

---

## 3. Domínio médico indevido

Não adicionar libs cujo propósito principal seja:

- diagnóstico clínico automatizado como produto;
- prescrição / recomendação de tratamento;
- integração HIS/EMR hospitalar real;

salvo decisão explícita fora do escopo atual (não esperado neste desafio).

---

## 4. Duplicate / bloat

- Não adicionar segunda framework web além de FastAPI
- Não adicionar segundo orquestrador além de Airflow sem justificativa
- Evitar dependências grandes sem uso real na entrega

---

## Approval Process

Para usar algo desta lista (seção 2) ou fora da allowlist:

1. Justificar necessidade frente aos pesos do desafio
2. Aprovação humana
3. Registrar DECISÃO DO PROJETO em `tech-challenge-requirements.md` / `tech-stack.md`
4. Atualizar allowlist

---

## Related Documentation

- **Allowed:** `.github/libs/allowed-libs.md`
- **Tech Stack:** `.github/context/tech-stack.md`
- **Requirements:** `.github/context/tech-challenge-requirements.md`
