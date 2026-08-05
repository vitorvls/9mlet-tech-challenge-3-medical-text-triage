# Security Rules

## Objective

Segurança **proporcional** a um protótipo acadêmico de inferência NLP.  
Não transformar o projeto em plataforma hospitalar certificada.

Requisitos tipados: `.cursor/context/tech-challenge-requirements.md`.

---

## 1. Princípios

- Validar todo input externo
- Não commitar secrets
- Não expor stack traces / internals ao cliente
- Não registrar conteúdo sensível de laudos sem necessidade
- Não inventar auth/JWT/RBAC como requisito FIAP

---

## 2. Input Validation

- Validar payload da API antes da inferência
- Rejeitar tipos incorretos e campos obrigatórios ausentes
- Evitar `eval` ou execução dinâmica de input do usuário

---

## 3. Secrets

- Usar variáveis de ambiente para segredos
- Não commitar `.env` com credenciais reais
- Não hardcodar API keys, tokens ou senhas
- Tokens de CI apenas em GitHub Secrets (quando necessário)

---

## 4. Error Handling

- Respostas de erro genéricas/seguras para o cliente
- Detalhes técnicos apenas em logs controlados
- Sem stack traces na resposta HTTP

---

## 5. Dados de laudos (cuidado mínimo)

- Laudos podem conter informações sensíveis em cenários reais
- **Não** logar o texto completo do laudo por padrão em produção-like demos, salvo necessidade explícita de debug local
- Não versionar datasets com PII real se evitável; preferir datasets públicos recomendados pelo desafio

---

## 6. Dependencies

- Preferir libs da allowlist (`.cursor/libs/allowed-libs.md`)
- Revisar dependências novas; não adicionar stacks paralelas sem justificativa

---

## 7. Explicitamente NÃO obrigatório neste desafio

Não exigir na implementação padrão:

- JWT / OAuth / session auth
- RBAC
- ORM / SQL injection hardening como foco (não há DB obrigatório)
- HTTPS termination complexa / mTLS
- Rate limiting de produto
- Helmet/Express ou equivalentes Node
- Certificações LGPD “completas” como escopo de entrega (respeitar bom senso; não inventar módulo de compliance)

Se no futuro auth for desejada: registrar como **DECISÃO DO PROJETO** com justificativa — não como requisito FIAP.

---

## Security Checklist (pré-entrega)

- [ ] Inputs da API validados
- [ ] Nenhum secret no repositório
- [ ] Erros sem stack trace ao cliente
- [ ] Logs não vazam laudos desnecessariamente
- [ ] Dependências alinhadas à allowlist

---

## Related Documentation

- **Requirements:** `.cursor/context/tech-challenge-requirements.md`
- **Business Rules:** `.cursor/rules/business-rules.md`
- **Deployment:** `.cursor/context/deployment.md`
