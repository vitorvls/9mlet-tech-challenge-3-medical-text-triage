# Code Style Rules

## Objective

Padrões de código para o projeto Python do Tech Challenge.  
**Não** há gate obrigatório de ESLint, Prettier, TypeScript ou `package.json`.

---

## Project Context

- **Language:** Python
- **API:** FastAPI
- **Linter/formatter concretos:** PENDENTE DE DECISÃO (não impor ruff/black/etc. sem aprovação humana)

---

## General Rules

### Python conventions

- Seguir PEP 8 como orientação geral
- `snake_case` para funções/variáveis; `PascalCase` para classes; `UPPER_SNAKE_CASE` para constantes
- Type hints recomendados em APIs públicas e funções de domínio (não bloquear o projeto por tipagem perfeita)

### Language of code vs comments (DECISÃO DO PROJETO)

- **Código** (nomes, mensagens de log/erro em código, docstrings): inglês
- **Comentários inline** explicativos: pt-BR quando necessários
- **Documentação de usuário** (README): pode ser pt-BR

### Comments

- Comentar o “porquê”, não o óbvio
- Evitar código comentado commitado

### Structure

- Preferir módulos pequenos e responsabilidades claras (API / modelo / métricas / treino)
- Não criar camadas enterprise (repository/UoW/etc.) sem necessidade

---

## Formatting & Lint

- Quando um linter/formatter for escolhido (PENDENTE), documentar em `tech-stack.md` e scripts do projeto
- Até lá: código legível e consistente manualmente é suficiente para iniciar
- CI deve ter verificação de código como uma das ≥2 automações (EXEMPLO FIAP: lint) — ferramenta concreta PENDENTE

**Proibido como regra deste projeto:**

- Exigir ESLint / Prettier / TypeScript / `package.json` scripts de frontend/Node

---

## Prohibited Patterns

- Hardcodar secrets
- `eval` / execução insegura de input
- Introduzir stack Node/Express para a API do desafio
- Abstrações prematuras e overengineering

---

## Related Documentation

- **Tech Stack:** `.github/context/tech-stack.md`
- **Testing:** `.github/rules/testing-rules.md`
- **Git:** `.github/rules/git-rules.md`
- **Requirements:** `.github/context/tech-challenge-requirements.md`
