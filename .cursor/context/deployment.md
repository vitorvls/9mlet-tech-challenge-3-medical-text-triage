# Deployment & Execution

## Objective

Como o projeto é **executado e entregue** no contexto do Tech Challenge.  
Não descreve deploy de produção hospitalar nem publish de pacotes npm.

Fonte tipada: `.cursor/context/tech-challenge-requirements.md`.

---

## 1. Modelo de entrega do desafio

| Ambiente | Papel |
|----------|--------|
| Local (Docker / Compose) | Ambiente principal de demonstração e avaliação |
| GitHub (Actions) | CI automatizado |
| README | Estratégia cloud **documental** + instruções de execução |
| Cloud real (AWS/Azure/GCP) | FORA DO ESCOPO — análise teórica apenas |

---

## 2. Execução local — serviço de inferência

**OBRIGATÓRIO:**

1. API FastAPI empacotada em **Dockerfile** funcional
2. Medição de **baseline de latência** local (Etapa 1)
3. Stack de monitoramento via **Docker Compose**: API + Prometheus + Grafana

Comandos concretos e nomes de serviços: a definir na implementação (não inventar aqui como obrigação).

---

## 3. Docker Compose (Etapa 3)

Compose deve permitir subir **conjuntamente**:

- API (com `prometheus_client`)
- Prometheus
- Grafana

Dashboard Grafana: **≥3 painéis** (EXEMPLO FIAP: total de requisições, latência, taxa de erro).

Entregável: Compose funcional + print/JSON do dashboard.

---

## 4. CI/CD — GitHub Actions

**OBRIGATÓRIO:**

- Workflow no repositório
- Pelo menos **2 automações**

**EXEMPLO FIAP:** lint → test → build; testes simples (ex.: pytest) e lint no push.

Não tornar uma sequência ou ferramenta de lint específica obrigatória além do que o PDF exige (≥2 automações / verificações).

Ferramentas concretas de lint/test: ver PENDENTE em `tech-stack.md`.

---

## 5. Airflow

DAG/script de treino/retreino (arquivo `.py`).

**EXEMPLO FIAP:** carregar dados → treinar → salvar modelo.

Execução do Airflow no desafio é para demonstrar a DAG funcional; detalhe de setup local: implementação futura (não superengenheirar com cluster Airflow de produção).

---

## 6. Estratégia cloud (documental — Etapa 1 / README)

**OBRIGATÓRIO no README:**

- Qual estratégia de deploy em nuvem seria adequada ao cenário
- Considerar **batch vs real-time**
- Justificativa arquitetural em texto

**EXEMPLO FIAP de provedores:** AWS, Azure, GCP.

**PENDENTE:** provedor e desenho textual escolhidos pelo time.

**FORA DO ESCOPO:** implementar infra real, Terraform, clusters, etc., apenas para “cumprir cloud”.

---

## 7. Evidências para entrega e vídeo STAR

Preservar (DECISÃO DO PROJETO — facilita avaliação e vídeo):

- Baseline e comparação de latência (números)
- Print/JSON do dashboard Grafana
- Workflow CI passando
- Demonstração da DAG
- Link do vídeo ≤5 min (STAR)

Checklist completo: `.cursor/commands/pre-delivery-validation.md`.

---

## 8. O que este arquivo NÃO cobre

- Publish npm / registry / tags
- Binários Node (pkg, nexe)
- Deploy automático em cloud
- Secrets de provedores cloud como requisito

---

## Related Documentation

- **Requirements:** `.cursor/context/tech-challenge-requirements.md`
- **Architecture:** `.cursor/context/architecture.md`
- **Tech Stack:** `.cursor/context/tech-stack.md`
- **Pre-delivery:** `.cursor/commands/pre-delivery-validation.md`
