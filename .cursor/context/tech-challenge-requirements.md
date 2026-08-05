# Tech Challenge Requirements — Fonte de Verdade

## Objetivo deste arquivo

Este arquivo é a **fonte de verdade tipada** dos requisitos do Tech Challenge Fase 3 para agentes e humanos.

**Hierarquia de autoridade:**

1. PDF oficial FIAP (`MLET - Tech Challenge Fase 3.pdf`)
2. Este arquivo (derivado do PDF + classificações explícitas)
3. Decisões explícitas do projeto (marcadas como DECISÃO DO PROJETO)
4. Demais arquivos em `.cursor/`

Em qualquer conflito, prevalece o PDF. Se este arquivo divergir do PDF, corrija este arquivo.

**Não implementar o projeto a partir deste arquivo sozinho sem ler `project-goals.md` e `architecture.md`.**  
**Não transformar EXEMPLO FIAP ou RECOMENDAÇÃO em obrigação.**

---

## Categorias (usar sempre estas labels)

| Categoria | Significado |
|-----------|-------------|
| **OBRIGATÓRIO** | Exigido pelo PDF; deve existir na entrega |
| **EXEMPLO FIAP** | Ilustração do PDF; alternativa válida é permitida se cumprir o obrigatório |
| **RECOMENDAÇÃO** | Orientação do PDF; não é obrigação estrita |
| **DECISÃO DO PROJETO** | Escolha interna documentada (não vem do PDF como obrigação) |
| **PENDENTE DE DECISÃO** | Ainda não escolhido; agentes **não** devem decidir sozinhos |
| **FORA DO ESCOPO** | Não exigir; não apresentar como requisito FIAP |

---

## 1. Tema e domínio

| Item | Categoria | Detalhe |
|------|-----------|---------|
| Tema: Deploy de modelo com CI/CD, monitoramento e otimização de latência | OBRIGATÓRIO (contexto) | Foco do desafio |
| Triagem automática de laudos/exames de texto por urgência | OBRIGATÓRIO (contexto) | Problema clínico do PDF |
| Classes `normal` / `atenção` / `urgente` | EXEMPLO FIAP | PDF usa “ex.:”; labels finais dependem do dataset (PENDENTE se dataset não definido) |
| Classificador de texto NLP **leve** | OBRIGATÓRIO | Modelo central |
| Serviço via API REST em container Docker | OBRIGATÓRIO | Inferência servida |

---

## 2. Bibliotecas / tecnologias exigidas pelo PDF

| Item | Categoria | Detalhe |
|------|-----------|---------|
| FastAPI | OBRIGATÓRIO | Construção da API |
| prometheus_client (Prometheus-client) | OBRIGATÓRIO | Instrumentação de métricas |
| Airflow | OBRIGATÓRIO | Orquestração de tarefas (treino/retreino) |
| Scikit-Learn **ou** framework de preferência | OBRIGATÓRIO (com liberdade) | Modelo base de classificação de texto |
| TF-IDF + Random Forest | EXEMPLO FIAP | “ou modelo leve similar” |
| Framework/modelo concreto do projeto | PENDENTE DE DECISÃO | Não escolher silenciosamente |
| Docker (Dockerfile do serviço de inferência) | OBRIGATÓRIO | |
| Docker Compose (API + Prometheus + Grafana) | OBRIGATÓRIO | Stack local de monitoramento |
| Prometheus | OBRIGATÓRIO | Parte da stack de monitoramento |
| Grafana | OBRIGATÓRIO | Dashboard com ≥3 painéis |
| GitHub Actions | OBRIGATÓRIO | CI/CD |
| Python | DECISÃO DO PROJETO / implícito | Linguagem do ecossistema FastAPI/sklearn; adotada pelo projeto |

---

## 3. Repositório e CI/CD

| Item | Categoria | Detalhe |
|------|-----------|---------|
| Pipeline CI/CD básico com GitHub Actions | OBRIGATÓRIO | |
| Pelo menos **2 automações** no CI/CD | OBRIGATÓRIO | |
| Sequência lint → test → build | EXEMPLO FIAP | Não é a única sequência válida |
| Testes simples (ex.: pytest) + lint no push | EXEMPLO FIAP | pytest e lint são exemplos do PDF |
| Histórico de commits semântico e organizado | OBRIGATÓRIO | |
| Conventional Commits | DECISÃO DO PROJETO | Forma interna de atender commits semânticos |

---

## 4. API e inferência (Etapa 1)

| Item | Categoria | Detalhe |
|------|-----------|---------|
| API FastAPI que recebe texto do laudo e retorna classificação | OBRIGATÓRIO | |
| Empacotar API em container Docker | OBRIGATÓRIO | |
| Medir baseline de latência local | OBRIGATÓRIO | Tempo de resposta |
| Contrato exato de endpoint/schema JSON | PENDENTE DE DECISÃO | PDF define entrada/saída conceitualmente, não o schema |

---

## 5. Airflow (Etapa 2)

| Item | Categoria | Detalhe |
|------|-----------|---------|
| Script ou DAG Airflow simples de treino/retreino | OBRIGATÓRIO | |
| DAG funcional | OBRIGATÓRIO | |
| Fluxo: carregamento de dados → treino → salvamento do modelo | EXEMPLO FIAP | Estrutura ilustrativa |
| Task ler CSV + task treinar/salvar | EXEMPLO FIAP | |

---

## 6. Monitoramento (Etapa 3)

| Item | Categoria | Detalhe |
|------|-----------|---------|
| Instrumentar API com prometheus_client | OBRIGATÓRIO | |
| Métricas básicas: tempo de requisição + contagem de chamadas | OBRIGATÓRIO | |
| docker-compose sobe API + Prometheus + Grafana juntos | OBRIGATÓRIO | |
| Dashboard Grafana | OBRIGATÓRIO | |
| Pelo menos **3 painéis** no Grafana | OBRIGATÓRIO | |
| Painéis: total de requisições, latência, taxa de erro | EXEMPLO FIAP | Outros painéis válidos desde que ≥3 e úteis |
| Entrega: Compose funcional + print/JSON do dashboard | OBRIGATÓRIO (entregável) | |

---

## 7. Modelo, otimização e latência (Etapa 4)

| Item | Categoria | Detalhe |
|------|-----------|---------|
| Treinar o classificador de texto | OBRIGATÓRIO | |
| Aplicar **pelo menos uma** técnica de otimização de latência | OBRIGATÓRIO | Vista em aula / alinhada ao curso |
| ONNX / quantização / pruning | EXEMPLO FIAP | Técnicas ilustrativas |
| Técnica concreta de otimização | PENDENTE DE DECISÃO | |
| Comparar latência: modelo original vs otimizado | OBRIGATÓRIO | |
| Documentar resultados comparativos | OBRIGATÓRIO (entregável) | |

---

## 8. Cloud e README

| Item | Categoria | Detalhe |
|------|-----------|---------|
| Analisar estratégia de deploy em nuvem e documentar **textualmente no README** | OBRIGATÓRIO | Inclui batch vs real-time |
| AWS / Azure / GCP | EXEMPLO FIAP | Provedores ilustrativos |
| Provedor cloud concreto | PENDENTE DE DECISÃO | Apenas para a análise documental |
| Deploy real em cloud | FORA DO ESCOPO | Não exigido pelo PDF |
| README com instruções claras de execução | OBRIGATÓRIO | Critério Documentação 15% |

---

## 9. Dataset

| Item | Categoria | Detalhe |
|------|-----------|---------|
| Dataset público de classificação de textos médicos/triagem | RECOMENDAÇÃO | |
| Coluna de texto + coluna target; ≥ 2.000 amostras | RECOMENDAÇÃO | Critérios sugeridos pelo PDF |
| Medical Abstracts TC Corpus (Kaggle) | EXEMPLO FIAP | |
| Recortes do MIMIC-III (open access) | EXEMPLO FIAP | |
| Dataset concreto escolhido pelo projeto | PENDENTE DE DECISÃO | Não escolher silenciosamente |

---

## 10. Vídeo STAR

| Item | Categoria | Detalhe |
|------|-----------|---------|
| Vídeo ≤ 5 minutos, método STAR | OBRIGATÓRIO | |
| **Situation:** problema clínico e importância da triagem rápida | OBRIGATÓRIO | |
| **Task:** requisitos técnicos (latência, CI/CD, monitoramento) | OBRIGATÓRIO | |
| **Action:** arquitetura, otimização do modelo, configuração da monitoração | OBRIGATÓRIO | |
| **Result:** pipeline funcionando, latência alcançada, lições aprendidas | OBRIGATÓRIO | |
| Preservar evidências para o vídeo (prints, métricas, latências) | DECISÃO DO PROJETO | Facilita a entrega; não é o vídeo em si |

---

## 11. Critérios oficiais de avaliação (pesos)

| Critério | Peso | O que o PDF descreve |
|----------|------|----------------------|
| Modelagem e Otimização | **20%** | Modelo NLP funcional, otimização bem-sucedida, melhoria de latência demonstrada |
| CI/CD (GitHub Actions) | **15%** | Workflow configurado e rodando testes básicos |
| Orquestração (Airflow) | **15%** | DAG funcional (ingestão e treino) |
| Monitoramento | **20%** | Compose (API + Prometheus + Grafana) + dashboard com métricas |
| Documentação (README) | **15%** | Arquitetura em nuvem escolhida + instruções claras de execução |
| Vídeo STAR | **15%** | Clareza técnica e impacto (≤ 5 min) |

Agentes devem priorizar esforço conforme esses pesos. Evitar funcionalidades sem valor para a avaliação.

---

## 12. Entregáveis por etapa

### Etapa 1 — Decisão arquitetural e API inicial

- OBRIGATÓRIO: decisão de cloud documentada no README (batch vs real-time)
- OBRIGATÓRIO: API FastAPI (texto → classificação)
- OBRIGATÓRIO: Docker da API
- OBRIGATÓRIO: baseline de latência local
- Entregável: API em Docker + texto de decisão arquitetural no README

### Etapa 2 — CI/CD e pipeline automatizado

- OBRIGATÓRIO: workflow GitHub Actions (≥2 automações; testes + verificação de código são o caminho natural)
- OBRIGATÓRIO: DAG/script Airflow de treino/retreino
- Entregável: YAML do workflow + arquivo `.py` da DAG

### Etapa 3 — Monitoramento

- OBRIGATÓRIO: prometheus_client (tempo de requisição + contagem)
- OBRIGATÓRIO: docker-compose (API + Prometheus + Grafana)
- OBRIGATÓRIO: dashboard Grafana (≥3 painéis)
- Entregável: Compose funcional + print/JSON do dashboard

### Etapa 4 — Otimização e entrega

- OBRIGATÓRIO: modelo treinado
- OBRIGATÓRIO: ≥1 técnica de otimização
- OBRIGATÓRIO: comparação de latência original vs otimizado
- OBRIGATÓRIO: vídeo STAR
- Entregável: modelo otimizado + resultados + link do vídeo

---

## 13. Fora do escopo (não apresentar como requisito FIAP)

| Item | Categoria |
|------|-----------|
| Sistema de diagnóstico médico | FORA DO ESCOPO |
| Substituto de profissionais de saúde | FORA DO ESCOPO |
| Sistema de recomendação de tratamentos | FORA DO ESCOPO |
| Sistema hospitalar completo | FORA DO ESCOPO |
| Frontend / interface gráfica | FORA DO ESCOPO (não obrigatório) |
| Banco de dados | FORA DO ESCOPO (não obrigatório) |
| JWT / autenticação complexa | FORA DO ESCOPO (não obrigatório) |
| RBAC | FORA DO ESCOPO (não obrigatório) |
| Redis | FORA DO ESCOPO (não obrigatório) |
| Kubernetes / arquitetura distribuída / microserviços | FORA DO ESCOPO (não obrigatório) |
| Integração com sistemas hospitalares reais | FORA DO ESCOPO |
| Deploy real em AWS/Azure/GCP / infra de produção | FORA DO ESCOPO (não obrigatório) |
| Stack Node.js / Express / npm CLI / SetAI | FORA DO ESCOPO |

**Regra de introdução de tecnologia extra:**

> Não introduzir itens FORA DO ESCOPO sem necessidade concreta, decisão arquitetural explícita documentada e justificativa. Privilegiar a solução mais simples que cumpra integralmente o Tech Challenge.

---

## 14. Contexto de produto (não é requisito FIAP)

| Item | Categoria | Detalhe |
|------|-----------|---------|
| Usuários: profissionais/equipes de triagem e análise de exames | DECISÃO DO PROJETO (contexto de produto) | O PDF **não** define usuários finais formalmente |
| Objetivo de apoiar priorização mais rápida e consistente | DECISÃO DO PROJETO / alinhado ao contexto | Interpretação do problema do PDF |

---

## 15. Decisões pendentes (agentes NÃO devem decidir sozinhos)

1. Dataset concreto
2. Framework/algoritmo concreto do classificador (além da liberdade sklearn-ou-preferência)
3. Labels finais de urgência (se diferentes do exemplo do PDF)
4. Técnica concreta de otimização (ONNX vs quantização vs pruning vs outra válida)
5. Linter/formatter Python concretos
6. Provedor e desenho detalhado da estratégia cloud documental
7. Contrato detalhado da API (paths, schemas, códigos HTTP)
8. Layout exato de pastas do repositório
9. Versões pinadas de dependências

Quando uma decisão for tomada, atualizar este arquivo (mover de PENDENTE para DECISÃO DO PROJETO) e alinhar `tech-stack.md` / `allowed-libs.md`.

---

## 16. Anti-padrões para agentes

- Não tratar EXEMPLO FIAP como única opção permitida
- Não inventar requisitos médicos, clínicos ou regulatórios não presentes no PDF
- Não implementar diagnóstico, prescrição ou recomendações de tratamento
- Não portar contexto legado (Node, SetAI, JWT obrigatório, DB obrigatório)
- Não superengenheirar (K8s, Redis, microserviços) antes de cumprir as 4 etapas
- Não escolher dataset/modelo/otimização silenciosamente — registrar como PENDENTE ou pedir aprovação humana

---

## Related Documentation

- **Project Goals:** `.cursor/context/project-goals.md`
- **Architecture:** `.cursor/context/architecture.md`
- **Tech Stack:** `.cursor/context/tech-stack.md`
- **Deployment:** `.cursor/context/deployment.md`
- **PDF oficial:** fora do repositório — `MLET - Tech Challenge Fase 3.pdf`
