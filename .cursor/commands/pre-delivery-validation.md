# Pre-Delivery Validation (Tech Challenge)

## Objective

Checklist final de **pré-entrega do Tech Challenge** (não “deploy de produção hospitalar”).

Substitui o antigo `pre-deploy-validation` focado em auth/produção.

## Project Context

- Fonte: `.cursor/context/tech-challenge-requirements.md`
- Deployment: `.cursor/context/deployment.md`
- Pesos: Modelagem 20% · Monitoramento 20% · CI/CD 15% · Airflow 15% · README 15% · Vídeo 15%

## Instructions

Do not change code. Validate evidence against the checklist below.  
Mark each item: OK / MISSING / PARTIAL / N/A (with reason).

### Etapa 1
- [ ] API FastAPI: texto → classificação
- [ ] Dockerfile do serviço de inferência
- [ ] Baseline de latência local documentada
- [ ] README com estratégia cloud (batch vs real-time)

### Etapa 2
- [ ] GitHub Actions workflow no repositório
- [ ] ≥2 automações (ex.: verificação de código + testes)
- [ ] DAG/script Airflow de treino/retreino (arquivo `.py`)

### Etapa 3
- [ ] `prometheus_client`: tempo de requisição + contagem de chamadas
- [ ] Docker Compose: API + Prometheus + Grafana juntos
- [ ] Grafana com ≥3 painéis
- [ ] Print/JSON do dashboard

### Etapa 4
- [ ] Modelo treinado
- [ ] ≥1 técnica de otimização aplicada
- [ ] Comparação de latência original vs otimizado
- [ ] Resultados documentados
- [ ] Vídeo STAR ≤5 min (Situation / Task / Action / Result)

### Transversal
- [ ] Histórico de commits semântico/organizado
- [ ] README com instruções claras de execução
- [ ] Sem requisitos inventados bloqueando a entrega (JWT/DB/K8s obrigatórios etc.)
- [ ] Evidências suficientes para gravar/demonstrar o vídeo

## Constraints

- Prioritize critical gaps that lose evaluation points
- Do not demand production auth/HTTPS/K8s
- Distinguish missing OBRIGATÓRIO vs missing polish

## Output

- Checklist with status per item
- Critical blockers
- Suggested fix order by evaluation weight

## Related Documentation

- `.cursor/context/tech-challenge-requirements.md`
- `.cursor/context/deployment.md`
- `.cursor/rules/security-rules.md`
- `.cursor/rules/testing-rules.md`
