# AI Coding Assistants (not the product NLP model)

## Objective

Este arquivo trata de **LLMs usados para assistir o desenvolvimento** (Cursor e similares).

**Não** define o classificador NLP do produto.  
O modelo de triagem (sklearn ou framework de preferência, otimização, etc.) está em:

- `.cursor/context/tech-challenge-requirements.md`
- `.cursor/context/tech-stack.md`
- `.cursor/libs/allowed-libs.md`

**Stack do produto:** Python + FastAPI + classificador NLP leve (+ Docker, Airflow, Prometheus/Grafana).

---

## Usage Rules

- Sempre validar saídas contra `tech-challenge-requirements.md`
- Não aceitar arquitetura gerada que introduza JWT/DB/K8s/Node sem pedido explícito
- Não deixar o assistente escolher PENDENTES (dataset, otimização, etc.)
- Preferir modelos com bom contexto de repositório para implementação diária

---

## Suggested use by phase (orientação, não obrigação FIAP)

| Fase | Uso sugerido do assistente |
|------|----------------------------|
| Planejamento / arquitetura | Revisar aderência às 4 etapas; detectar overengineering |
| Implementação | FastAPI, testes, Docker, métricas, DAG |
| Documentação | README cloud + instruções; evidências de latência |
| Debug | Logs, falhas de CI, Compose |

Escolha concreta de modelo de LLM no Cursor: preferência do time (DECISÃO DO PROJETO operacional). Não é critério de avaliação da FIAP.

---

## Related Documentation

- **AI Usage Rules:** `.cursor/rules/ai-usage-rules.md`
- **Requirements:** `.cursor/context/tech-challenge-requirements.md`
- **Commands:** `.cursor/commands/`
