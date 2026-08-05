# Git Rules

## Objective

Padrões de Git para `9mlet-tech-challenge-3-medical-text-triage`.

**Do PDF (OBRIGATÓRIO):** histórico de commits semântico e organizado.

**DECISÃO DO PROJETO:** Conventional Commits como forma de atender esse requisito.  
Isso **não** é um requisito nomeado pela FIAP.

---

## Commit Messages (DECISÃO DO PROJETO)

Formato Conventional Commits:

```
<type>(<scope>): <subject>
```

Types comuns: `feat`, `fix`, `docs`, `style`, `refactor`, `test`, `chore`, `ci`, `build`.

### Exemplos alinhados ao domínio

```
feat(api): add report classification endpoint

test(api): cover invalid payload rejection

ci: add pytest workflow on push

docs(readme): document cloud batch vs realtime strategy

perf(model): compare baseline and optimized latency
```

Não usar exemplos de JWT/auth como referência padrão.

---

## Branches

Sugestão interna (não é requisito FIAP):

- `main` — código estável para entrega
- `feature/...`, `fix/...` — trabalho incremental

Ajustar ao fluxo do grupo sem burocracia excessiva.

---

## Pull Requests (quando o time usar PRs)

- Descrever o que mudou e como testar
- CI verde quando houver workflow
- Preferir PRs focados
- Não exigir TDD como critério de merge (TDD não é regra FIAP/projeto)

---

## Prohibited

- Commitar secrets ou `.env` com credenciais
- Force push em branches compartilhadas sem acordo do time
- Commits vazios de significado (“update”, “fix”) de forma habitual
- Versionar binários grandes / modelos enormes sem necessidade (avaliar Git LFS ou artefatos externos se preciso — decisão futura)

---

## Related Documentation

- **Requirements:** `.cursor/context/tech-challenge-requirements.md`
- **Testing:** `.cursor/rules/testing-rules.md`
- **Code Style:** `.cursor/rules/code-style.md`
