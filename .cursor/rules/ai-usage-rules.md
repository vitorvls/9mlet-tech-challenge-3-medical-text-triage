# AI Usage Rules

## Objective

Onde e como a IA pode atuar neste Tech Challenge.  
Antes de implementar funcionalidade relevante, a IA **deve** consultar:

`.cursor/context/tech-challenge-requirements.md`

---

## Fundamental Rules

1. **PDF / requirements tipados > prompt genérico**  
   Não inventar requisitos. Não transformar EXEMPLO FIAP em obrigação.

2. **IA propõe; humanos aprovam** decisões arquiteturais, dataset, modelo, otimização e demais PENDENTES.

3. **Não introduzir requisitos médicos** não especificados (diagnóstico, conduta, LGPD “módulo completo”, etc.).

4. **Anti-overengineering:** solução mínima que cumpra as 4 etapas e os pesos de avaliação.

5. **Sem stack legada:** não reintroduzir Node/Express/npm CLI/SetAI/JWT/DB como padrão.

6. Código gerado entra no ciclo normal: review, testes, documentação.
7. **Documentação por etapa é obrigatória:** ao implementar, gravar `docs/etapas/<trilha>/etapa-NN.md` e só então marcar o TODO. Ver `rules/documentation-rules.md`. Trilhas: Modelagem e otimização (Vítor), API e Docker (Vini), Monitoramento (Fernando), CI-CD Airflow e documentacao (Edu).

---

## Before Implementing Checklist

- [ ] Li `tech-challenge-requirements.md` para o item em questão
- [ ] Classifiquei: OBRIGATÓRIO / EXEMPLO / RECOMENDAÇÃO / DECISÃO / PENDENTE / FORA DO ESCOPO
- [ ] Se PENDENTE: parei e pedi decisão humana (não escolhi silenciosamente)
- [ ] A mudança ajuda algum critério de avaliação (pesos)?
- [ ] Não estou adicionando frontend/DB/auth/K8s sem justificativa explícita
- [ ] Vou criar/atualizar `docs/etapas/<trilha>/etapa-NN.md` nesta mesma etapa (senão a tarefa não está concluída)

---

## Where AI Can Act

- Explorar alternativas e trade-offs (com revisão humana)
- Implementar código alinhado à stack Python/FastAPI
- Escrever testes (pytest como caminho natural)
- Documentar README, evidências de latência, dashboards
- Documentar cada etapa em `docs/etapas/` (didático; modelagem com métricas explicadas)
- Refatorar sem mudar comportamento
- Validar aderência às 4 etapas (`architecture-review`, `pre-delivery-validation`)

---

## Where AI Must Not Decide Alone

- Escolher dataset, algoritmo final, técnica de otimização
- Definir labels clínicas além do exemplo do PDF sem dataset
- Introduzir auth, banco, cloud real, microserviços
- Alterar classificação de requisitos (ex.: tornar ONNX obrigatório)
- “Corrigir” o domínio para diagnóstico médico

---

## Tooling Prerequisites

**Não** exigir ESLint, Prettier, TypeScript ou `package.json` para autorizar uso de IA.

Pré-requisitos reais:

- Contexto `.cursor` atualizado
- Alinhamento com `tech-challenge-requirements.md`
- Stack Python do projeto

Linter/formatter Python: PENDENTE DE DECISÃO.

---

## Models for coding assistance

Ver `.cursor/libs/ai-models.md` (LLMs de assistência ao desenvolvimento — **não** confundir com o classificador NLP do produto).

---

## Related Documentation

- **Requirements:** `.cursor/context/tech-challenge-requirements.md`
- **Code Style:** `.cursor/rules/code-style.md`
- **Testing:** `.cursor/rules/testing-rules.md`
- **AI Models (assistants):** `.cursor/libs/ai-models.md`
- **Documentation:** `.cursor/rules/documentation-rules.md`
