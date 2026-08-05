# Allowed Libraries

## Objective

Allowlist coerente com Python e o Tech Challenge.  
Classificação alinhada a `.cursor/context/tech-challenge-requirements.md`.

**Não escolher bibliotecas opcionais silenciosamente.**  
Se algo estiver PENDENTE, pedir aprovação humana antes de adicionar ao projeto.

---

## REQUIRED BY CHALLENGE

| Biblioteca / tecnologia | Uso |
|-------------------------|-----|
| `fastapi` | API REST |
| `uvicorn` (ou ASGI server equivalente) | Servir a API — usual com FastAPI; se outro ASGI for usado, documentar como decisão |
| `prometheus_client` | Métricas (latência + contagem) |
| `apache-airflow` (Airflow) | DAG de treino/retreino |
| Scikit-Learn **ou** framework de preferência | Classificador NLP leve |

Prometheus e Grafana entram como serviços no Docker Compose (não necessariamente “libs Python” da API).

Docker / Docker Compose / GitHub Actions: ferramentas de entrega (ver `tech-stack.md` / `deployment.md`).

---

## EXEMPLO FIAP (caminho natural, não obrigação única)

| Item | Notas |
|------|--------|
| `scikit-learn` | Caminho explícito do PDF |
| TF-IDF + Random Forest | Pipeline ilustrativo |
| `pytest` | Exemplo de testes no CI |
| ONNX / quantização / pruning (+ libs associadas) | Exemplos de otimização — só adicionar após DECISÃO |

---

## PROJECT DECISION

Nenhuma lib opcional de domínio foi fechada ainda além do que o PDF exige.

Quando o time decidir, mover itens de PENDENTE para cá e atualizar `tech-stack.md`.

---

## OPTIONAL (somente com decisão explícita)

| Área | Exemplos | Status |
|------|----------|--------|
| Validação | `pydantic` (já usado por FastAPI) | Aceitável via FastAPI |
| Dados / treino | `pandas`, `numpy` | Comum com sklearn; confirmar na implementação |
| Otimização | `onnx`, `onnxruntime`, libs de quantização/pruning | Condicional à técnica escolhida (PENDENTE) |
| Lint/format | `ruff`, `black`, `isort`, `flake8` | PENDENTE DE DECISÃO |
| HTTP client em testes | `httpx` | Comum com FastAPI TestClient; decidir na implementação |
| Empacotamento | `pip`+requirements, `poetry`, `uv` | PENDENTE DE DECISÃO |

---

## DEV TOOLING

| Item | Notas |
|------|--------|
| Python packaging tools | Conforme decisão de empacotamento |
| Editor / Cursor | Fora do runtime da API |

---

## Update Policy

1. Nova dependência → classificar (REQUIRED / DECISÃO / OPTIONAL)
2. Se não for REQUIRED BY CHALLENGE → justificativa + aprovação humana
3. Atualizar este arquivo e `tech-stack.md`
4. Preferir poucas dependências

---

## Related Documentation

- **Forbidden:** `.cursor/libs/forbidden-libs.md`
- **Tech Stack:** `.cursor/context/tech-stack.md`
- **Requirements:** `.cursor/context/tech-challenge-requirements.md`
