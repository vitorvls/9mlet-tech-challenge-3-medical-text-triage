# Project Goals

## Objective

Contexto de negócio, objetivos e limites do projeto.  
Requisitos tipados (OBRIGATÓRIO / EXEMPLO / etc.): `.github/context/tech-challenge-requirements.md`.

---

## 1. Problem Statement

**Problema:** Automatizar a triagem de laudos médicos (exames de texto) com um classificador NLP leve que analisa o texto e determina um nível de urgência, apoiando a priorização dos casos que demandam maior atenção.

**Por que importa:** Em ambiente hospitalar, identificar rapidamente exames que exigem maior atenção acelera a priorização. A classificação automática busca tornar a triagem mais rápida e consistente.

**Exemplos de classes no PDF:** normal / atenção / urgente — são **EXEMPLO FIAP**, não contrato definitivo de labels até o dataset ser escolhido (PENDENTE).

---

## 2. Target Users

O PDF **não** define formalmente usuários finais.

**Contexto de produto (DECISÃO DO PROJETO — não é requisito FIAP):**  
profissionais e equipes responsáveis pela triagem e análise de exames podem ser apoiados pela classificação automática.

Não documentar isso como exigência explícita da FIAP.

---

## 3. Business / Delivery Objectives

Alinhados ao desafio e aos pesos de avaliação:

1. Classificador NLP + API REST FastAPI com baixa latência de inferência
2. Serviço containerizado (Docker) e baseline de latência
3. CI/CD com GitHub Actions (≥2 automações)
4. DAG Airflow de treino/retreino
5. Monitoramento: prometheus_client + Prometheus + Grafana via Docker Compose (≥3 painéis)
6. ≥1 técnica de otimização + comparação original vs otimizado
7. README com estratégia cloud (batch vs real-time) + instruções de execução
8. Vídeo STAR ≤5 min

**Pesos oficiais:** Modelagem/Otimização 20% · Monitoramento 20% · CI/CD 15% · Airflow 15% · README 15% · Vídeo STAR 15%.

Detalhes: `tech-challenge-requirements.md`.

---

## 4. Constraints

### Do desafio (resumo)

Ver classificação completa em `tech-challenge-requirements.md`. Em resumo:

- FastAPI, Docker, GitHub Actions, Airflow, prometheus_client, Prometheus, Grafana, Compose
- Classificador leve (Scikit-Learn **ou** framework de preferência)
- Otimização de latência + comparação
- Commits semânticos; vídeo STAR

### De negócio

O PDF não define orçamento, SLA, volume de exames ou regras hospitalares específicas.

---

## 5. Non-Goals / Fora do escopo

O projeto **não** é:

- sistema de diagnóstico médico;
- substituto de profissionais de saúde;
- sistema de recomendação de tratamentos;
- sistema hospitalar completo.

**Não são obrigatórios do desafio** (não introduzir sem decisão explícita e justificativa):

- frontend;
- banco de dados;
- JWT / RBAC / autenticação complexa;
- Redis, Kubernetes, microserviços;
- integração com sistemas hospitalares reais;
- deploy real em cloud / infra de produção.

---

## 6. Decisões pendentes

Lista canônica em `tech-challenge-requirements.md` §15.  
Agentes não devem escolher sozinhos dataset, algoritmo, técnica de otimização, linter, contrato detalhado da API, etc.

---

## Related Documentation

- **Requirements:** `.github/context/tech-challenge-requirements.md`
- **Architecture:** `.github/context/architecture.md`
- **Business Rules:** `.github/rules/business-rules.md`
