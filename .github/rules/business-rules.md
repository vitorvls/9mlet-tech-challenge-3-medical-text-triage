# Business Rules

## Objective

Regras de domínio e comportamento da solução de triagem por NLP.  
Requisitos tipados: `.github/context/tech-challenge-requirements.md`.

---

## Project Context (resumo)

- Classificar texto de laudo por urgência (apoio à priorização)
- Não é diagnóstico, tratamento nem substituto de profissional de saúde
- Usuários formais: não definidos pela FIAP (ver `project-goals.md`)

---

## Domain Rules

### BR-1 — Escopo da classificação

- O sistema classifica **texto** (laudo/exame em texto) quanto a **nível de urgência / target de classificação**.
- Não emite diagnóstico clínico, conduta terapêutica nem priorização operacional além da label de classificação.

### BR-2 — Labels de urgência

- O PDF exemplifica: `normal` / `atenção` / `urgente` (**EXEMPLO FIAP**).
- Labels finais do modelo: **PENDENTE DE DECISÃO** (dependem do dataset). Até lá, não fixar contrato definitivo além do exemplo.

### BR-3 — Entrada e saída da API

- Entrada: texto do laudo.
- Saída: classificação (urgência/target).
- Schema JSON, paths e códigos HTTP detalhados: **PENDENTE DE DECISÃO**.

### BR-4 — Validação de input

- Rejeitar inputs inválidos de forma clara (ex.: texto ausente, tipo incorreto, payload malformado).
- Mensagens de erro acionáveis; sem stack traces para o cliente.

### BR-5 — Inferência determinística quanto ao contrato

- Dado o mesmo modelo versionado e o mesmo texto, o comportamento de classificação deve ser estável para fins de teste/demo (salvo decisão explícita em contrário).

### BR-6 — Latência e otimização

- Deve existir baseline de latência e comparação original vs otimizado (OBRIGATÓRIO do desafio).
- Técnica de otimização concreta: **PENDENTE**.

### BR-7 — Observabilidade mínima

- Contagem de chamadas e tempo de requisição expostos via prometheus_client (OBRIGATÓRIO).

---

## Explicitamente NÃO são regras deste projeto

Não tratar como obrigatório:

- Autenticação de todas as requests / JWT / RBAC
- Transações de banco / optimistic locking
- Quotas de usuário / rate limiting de produto
- Persistência de laudos em banco
- Regras hospitalares de SLA não definidas no PDF

---

## Edge Cases (mínimos)

1. Texto vazio ou só whitespace → erro de validação
2. Texto extremamente longo → comportamento **PENDENTE** (definir limite na implementação com decisão explícita)
3. Classe/label desconhecida no treino → não inventar taxonomia clínica fora do dataset

---

## Related Documentation

- **Requirements:** `.github/context/tech-challenge-requirements.md`
- **Project Goals:** `.github/context/project-goals.md`
- **Security:** `.github/rules/security-rules.md`
