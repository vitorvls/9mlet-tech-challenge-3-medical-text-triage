# Testing Rules

## Objective

Estratégia de testes alinhada ao Tech Challenge.  
O PDF exige testes no pipeline de CI (ex.: pytest), **não** exige TDD nem percentual mínimo de cobertura.

---

## What the challenge requires

- CI com automações incluindo testes (EXEMPLO FIAP: pytest no push)
- Testes básicos suficientes para o workflow GitHub Actions (critério CI/CD 15%)

## What is NOT required by FIAP

- TDD obrigatório
- Cobertura mínima (70%, 80%, 100%, etc.)
- Suite E2E de browser
- Testes de autenticação/DB (não há auth/DB obrigatórios)

---

## Priority of tests

Ordene esforço pelo valor na entrega:

1. **API:** texto válido → classificação; inputs inválidos → erro claro
2. **Validação** de payload
3. **Inferência:** modelo retorna label do conjunto esperado (quando modelo existir)
4. **Integração essencial:** app sobe; endpoint de predição responde; `/metrics` expõe métricas (quando existir)
5. **Regressões críticas** após otimização (mesmo contrato de saída)

Testes de latência/comparação: evidência da Etapa 4 (scripts ou docs), não necessariamente a mesma suite unitária.

---

## Tools

- **pytest:** EXEMPLO FIAP e escolha natural para Python — tratar como caminho preferencial, não como dogma se o time decidir equivalente com justificativa
- Framework concreto/versão: alinhar a `tech-stack.md` / decisão pendente

Arquivos de teste: padrão Python comum (`tests/`, `test_*.py` ou `*_test.py`).

---

## Patterns

- Testes isolados e determinísticos
- Nomes descritivos
- AAA (Arrange, Act, Assert) quando ajudar
- Não usar dados de produção sensíveis
- Mock de I/O externo quando necessário

---

## CI Integration

- Testes devem rodar no GitHub Actions
- Falha de testes deve falhar o workflow
- PRs/commits devem manter o CI verde na medida do fluxo do time

---

## Explicitly removed from template legacy

- TDD CRITICAL / Red-Green-Refactor obrigatório
- Exemplos TypeScript / Jest / Vitest como stack de teste do produto
- Pirâmide E2E browser como obrigação
- Placeholders `{{TEST_COVERAGE}}`

TDD pode ser usado como **preferência pessoal** de um dev; não é regra do projeto nem da FIAP.

---

## Related Documentation

- **Requirements:** `.cursor/context/tech-challenge-requirements.md`
- **Code Style:** `.cursor/rules/code-style.md`
- **Git Rules:** `.cursor/rules/git-rules.md`
