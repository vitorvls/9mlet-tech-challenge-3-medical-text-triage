# TODO do Projeto — Medical Text Triage

Guia prático do time para executar o **Tech Challenge Fase 3 (FIAP)** de forma assíncrona.

**Objetivo em uma frase:** criar um serviço que lê o texto de um laudo médico e responde se o caso parece **normal**, **atenção** ou **urgente** (ou labels equivalentes do dataset escolhido), com API, Docker, CI/CD, Airflow, monitoramento e otimização de latência.

> Este documento é o quadro operacional do time. Requisitos tipados ficam em `.cursor/context/`. Em caso de conflito com o PDF oficial da FIAP, **prevalece o PDF**.

---

## Como usar este arquivo

1. Marque `[x]` quando a atividade estiver **feita e revisável** (código no repo + evidência se pedir).
2. Não avance um checkpoint sem o time alinhar o que está bloqueando.
3. Se algo estiver marcado como **PENDENTE DE DECISÃO**, **não escolha sozinho** — leve para o sync do time.
4. Guarde evidências na pasta combinada (sugestão: `evidencias/`) para o vídeo.

### Legenda rápida

| Símbolo | Significado |
|---------|-------------|
| `[ ]` | Pendente |
| `[x]` | Concluído |
| **Dono** | Quem lidera a entrega |
| **Apoio** | Quem ajuda / valida |
| **Bloqueia** | Sem isso, a próxima atividade trava |
| **Entregável** | O que precisa existir no final da atividade |

---

## Time e papéis

| Pessoa | Papel principal | Em linguagem simples |
|--------|-----------------|----------------------|
| **Vítor** | Modelo NLP + otimização | Ensina o computador a classificar o texto e deixa isso mais rápido |
| **Vini** | API FastAPI + Docker + baseline | Cria a “janela” (API) por onde o texto entra e a classificação sai |
| **Fernando** | Monitoramento (Prometheus + Grafana + Compose) | Mostra números: quantas chamadas, quanto demora, erros |
| **Edu** | Airflow + CI/CD + README cloud + **vídeo STAR** | Automatiza treino e checagens; fecha documentação e vídeo |

### Pesos da nota (para priorizar esforço)

| Critério | Peso | Dono principal |
|----------|------|----------------|
| Modelagem e otimização | 20% | Vítor |
| Monitoramento | 20% | Fernando |
| CI/CD (GitHub Actions) | 15% | Edu |
| Orquestração (Airflow) | 15% | Edu |
| Documentação (README) | 15% | Edu (+ apoio do time) |
| Vídeo STAR | 15% | Edu |

---

## Glossário (para quem está começando)

| Termo | O que é |
|-------|---------|
| **Laudo / exame de texto** | Texto médico que será classificado |
| **Classificador NLP** | Programa que lê texto e escolhe uma classe (ex.: urgente) |
| **API** | Porta de entrada HTTP: você manda JSON e recebe JSON |
| **FastAPI** | Biblioteca Python para criar a API |
| **Docker** | “Caixa” que empacota a API para rodar igual em qualquer máquina |
| **Docker Compose** | Sobe vários containers juntos (API + Prometheus + Grafana) |
| **Latência** | Tempo de resposta (quanto demora para classificar) |
| **Baseline** | Medição inicial, antes de otimizar |
| **prometheus_client** | Biblioteca que expõe métricas da API |
| **Prometheus** | Sistema que coleta essas métricas |
| **Grafana** | Telas (painéis) com gráficos das métricas |
| **Airflow / DAG** | Orquestrador: sequência de tarefas (carregar dados → treinar → salvar) |
| **CI/CD (GitHub Actions)** | Robô no GitHub que roda lint/testes ao dar push |
| **Otimização** | Técnica para o modelo responder mais rápido (ex.: ONNX) |
| **Batch vs real-time** | Processar muitos de uma vez (batch) vs responder na hora (real-time) |
| **STAR** | Roteiro do vídeo: Situation, Task, Action, Result |

---

## O que NÃO vamos fazer (fora de escopo)

Não gastar tempo com:

- Frontend / site bonito
- Banco de dados
- Login, JWT, permissões
- Kubernetes, Redis, microserviços
- Deploy real em AWS/Azure/GCP (só **texto** no README)
- Diagnóstico médico, prescrição ou “substituir o médico”

Se alguém quiser incluir algo disso, precisa de **decisão explícita do time** e justificativa.

---

# FASE 0 — Kickoff do time (todos)

**Objetivo:** destravar o trabalho paralelo. Sem isso, cada um inventa um contrato diferente.

**Duração sugerida:** 1 sync de 45–60 min + registro por escrito neste TODO.

## 0.1 Decisões obrigatórias do time

| # | Decisão | Status | Quem registra |
|---|---------|--------|---------------|
| 1 | Dataset concreto (fonte + link) | `[ ]` PENDENTE | Time |
| 2 | Labels finais (ex.: normal / atenção / urgente **ou** as do dataset) | `[ ]` PENDENTE | Time |
| 3 | Algoritmo / framework do modelo (ex.: TF-IDF + Random Forest) | `[ ]` PENDENTE | Time (Vítor propõe) |
| 4 | Técnica de otimização (ex.: ONNX / quantização / pruning) | `[ ]` PENDENTE | Time (Vítor propõe) |
| 5 | Contrato da API: path, JSON de entrada, JSON de saída, códigos HTTP | `[ ]` PENDENTE | Time (Vini propõe) |
| 6 | Layout mínimo de pastas do repositório | `[ ]` PENDENTE | Time |
| 7 | Onde o modelo salvo fica e como a API carrega | `[ ]` PENDENTE | Vítor + Vini |
| 8 | Linter/formatter (ex.: ruff) e ferramenta de teste (ex.: pytest) | `[ ]` PENDENTE | Edu propõe |
| 9 | Provedor cloud **só para o texto** do README (AWS/Azure/GCP) | `[ ]` PENDENTE | Edu propõe |
| 10 | Pasta de evidências (sugestão: `evidencias/`) | `[ ]` PENDENTE | Edu |

### Contrato mínimo sugerido da API (para discutir e fechar)

> Isto é **proposta de discussão**, não decisão final até marcar o item 5 acima.

**Entrada (exemplo):**

```json
{
  "text": "texto do laudo médico aqui"
}
```

**Saída (exemplo):**

```json
{
  "label": "urgente",
  "confidence": 0.91
}
```

**Path sugerido:** `POST /predict`  
**Métricas:** `GET /metrics` (Prometheus)

### Checklist Fase 0

- [ ] Dataset escolhido e documentado (nome + link + tamanho aproximado)
- [ ] Labels definidas
- [ ] Algoritmo proposto e aceito
- [ ] Técnica de otimização proposta e aceita
- [ ] Contrato da API escrito (pode ser neste arquivo ou no README)
- [ ] Estrutura de pastas combinada
- [ ] Path do artefato do modelo combinado
- [ ] Ferramentas de lint/teste combinadas
- [ ] Estratégia cloud documental (provedor + batch vs real-time) esboçada
- [ ] Pasta `evidencias/` criada (ou caminho equivalente)

### Checkpoint 0 — “Podemos trabalhar em paralelo”

**Critério de pronto:** todas as decisões da tabela acima marcadas (ou explicitamente adiadas com prazo).

- [ ] Checkpoint 0 aprovado pelo time

---

# FASE 1 — Trilhas em paralelo (Semana A)

Cada um avança **sem esperar o modelo perfeito**. Onde faltar o modelo real, use **mock** (resposta fake controlada) até o Vítor entregar o artefato.

---

## Vítor — Modelo e treino (base)

### Em linguagem simples

Você pega um conjunto de textos já classificados (dataset), treina um modelo leve e salva o arquivo do modelo para a API usar.

### Atividades

#### V1. Preparar o dataset

- [ ] Baixar o dataset escolhido
- [ ] Confirmar colunas: texto + target (rótulo)
- [ ] Documentar no README ou em `docs/` (fonte, tamanho, licença/uso)
- [ ] Separar treino / teste (mesmo que simples)

**Entregável:** dados prontos no repo (ou script que baixa) + nota de como usar.

#### V2. Pipeline de treino

- [ ] Script Python de treino (carregar → treinar → avaliar → salvar)
- [ ] Métricas básicas de qualidade (ex.: accuracy / F1 — o que fizer sentido)
- [ ] Salvar modelo no path combinado com o Vini
- [ ] README curto: como rodar o treino localmente

**Entregável:** script de treino + arquivo do modelo (ou comando que gera).

#### V3. Interface para a API

- [ ] Função clara tipo `predict(text: str) -> label` (e confiança, se combinado)
- [ ] Documentar como carregar o modelo (1 exemplo de uso)

**Bloqueia:** Vini (inferência real) e Edu (DAG chama este fluxo).

**Entregável:** módulo/função utilizável pela API e pela DAG.

### Checkpoint Vítor A — “Modelo baseline existe”

- [ ] Modelo treinado salva e carrega
- [ ] `predict` funciona em pelo menos 3 textos de exemplo
- [ ] Path do artefato alinhado com Vini/Edu

---

## Vini — API + Docker + baseline

### Em linguagem simples

Você cria o serviço web: alguém manda o texto do laudo e recebe a classificação. Depois coloca isso numa “caixa” Docker e mede quanto tempo demora.

### Atividades

#### N1. Skeleton da API (pode começar com mock)

- [ ] Projeto FastAPI mínimo
- [ ] Endpoint de health (ex.: `GET /health`) — recomendado
- [ ] Endpoint de classificação conforme o contrato (ex.: `POST /predict`)
- [ ] Validação do input (texto vazio, tipo errado, etc.)
- [ ] Enquanto o modelo não chega: mock previsível (ex.: sempre uma label fixa ou regra simples)

**Entregável:** API rodando localmente com o contrato fechado.

#### N2. Integração com o modelo do Vítor

- [ ] Trocar mock pelo `predict` real
- [ ] Tratar erro se o modelo não carregar
- [ ] Testar com textos reais do dataset

**Bloqueia:** Fernando (métricas reais em cima da API) e baseline séria.

#### N3. Docker da API

- [ ] `Dockerfile` funcional
- [ ] Documentar: build + run
- [ ] Confirmar que a API responde **dentro** do container

**Entregável:** API empacotada em Docker.

#### N4. Baseline de latência (Etapa 1 do desafio)

- [ ] Definir método de medição (ex.: N requisições locais e média/p95)
- [ ] Medir latência da API em Docker (modelo ainda sem otimização final)
- [ ] Registrar números em `evidencias/` (tabela simples)

**Entregável:** números de baseline documentados.

### Checkpoint Vini A — “API sobe e responde”

- [ ] Contrato da API estável
- [ ] Docker build/run ok
- [ ] Baseline de latência registrada

---

## Fernando — Monitoramento

### Em linguagem simples

Você faz a API “contar” chamadas e tempos, o Prometheus coleta esses números e o Grafana mostra gráficos. Tudo sobe junto com Docker Compose.

### Atividades

#### F1. Instrumentar a API com `prometheus_client`

> Trabalhe junto com o Vini no mesmo serviço (PR coordenada).

- [ ] Expor `GET /metrics`
- [ ] Métrica de **contagem de requisições**
- [ ] Métrica de **tempo de requisição** (latência)
- [ ] (Recomendado) métrica de erros / status HTTP para um painel útil

**Entregável:** API instrumentada.

#### F2. Prometheus

- [ ] Configurar Prometheus para fazer scrape da API
- [ ] Confirmar que as métricas aparecem no Prometheus

#### F3. Docker Compose (API + Prometheus + Grafana)

- [ ] `docker-compose.yml` sobe os 3 serviços juntos
- [ ] Documentar portas e como acessar
- [ ] Time consegue subir com um comando combinado

**Entregável:** Compose funcional.

#### F4. Grafana (≥ 3 painéis) — pode começar o layout cedo

- [ ] Dashboard com **pelo menos 3 painéis**
- [ ] Exemplos válidos (FIAP): total de requisições, latência, taxa de erro
- [ ] Exportar JSON do dashboard **ou** print claro
- [ ] Salvar em `evidencias/`

**Entregável:** dashboard + evidência visual/JSON.

### Checkpoint Fernando A — “Stack de monitoramento sobe”

- [ ] Compose sobe API + Prometheus + Grafana
- [ ] `/metrics` populando após algumas chamadas
- [ ] ≥ 3 painéis visíveis

---

## Edu — CI/CD + Airflow + documentação base

### Em linguagem simples

Você faz o GitHub checar o código automaticamente, cria a “receita” (DAG) que treina o modelo em passos, escreve no README a ideia de cloud e, no fim, grava o vídeo.

### Atividades

#### E1. CI/CD com GitHub Actions (≥ 2 automações)

- [ ] Workflow no repositório (YAML)
- [ ] Automação 1 (ex.: lint)
- [ ] Automação 2 (ex.: testes)
- [ ] Confirmar que o workflow roda no push/PR
- [ ] Print ou link do run verde em `evidencias/`

**Entregável:** YAML do workflow + evidência de execução.

#### E2. Esqueleto da DAG Airflow

- [ ] Arquivo `.py` da DAG
- [ ] Estrutura mínima alinhada ao fluxo: carregar dados → treinar → salvar modelo  
  (forma exata pode seguir o exemplo FIAP; o obrigatório é **DAG funcional** de treino/retreino)
- [ ] Encaixar/chamar o script do Vítor (quando existir)

**Entregável:** DAG `.py` no repo.

#### E3. README — estratégia cloud (documental)

- [ ] Seção no README: batch vs real-time
- [ ] Escolher um provedor **só no texto** (AWS/Azure/GCP)
- [ ] Explicar por que faria sentido no cenário de triagem
- [ ] **Não** implementar infra real

**Entregável:** texto claro no README.

#### E4. Instruções de execução (vai crescendo)

- [ ] Como instalar / subir API
- [ ] Como subir Compose
- [ ] Como rodar treino / DAG (nível do time)
- [ ] Como ver Grafana

### Checkpoint Edu A — “Automação e DAG existem”

- [ ] ≥ 2 automações no Actions
- [ ] DAG `.py` no repo (mesmo que ainda integre o treino final depois)
- [ ] Rascunho da seção cloud no README

---

# FASE 2 — Integração (Semana B)

**Objetivo:** juntar as peças. O mock some. O Compose usa a API de verdade. A DAG treina de verdade.

### Checklist de integração (todos)

- [ ] Modelo do Vítor carrega na API do Vini
- [ ] Compose do Fernando sobe a API real com métricas
- [ ] DAG do Edu chama o treino do Vítor e salva no path combinado
- [ ] CI ainda passa após a integração
- [ ] README atualizado com o fluxo real

### Checkpoint 2 — “Pipeline ponta a ponta mínimo”

**Critério de pronto:**

1. Texto → API → classificação real  
2. Métricas aparecem no Grafana  
3. DAG de treino/retreino funcional  
4. Actions com ≥ 2 automações verdes  

- [ ] Checkpoint 2 aprovado pelo time

---

# FASE 3 — Otimização e fechamento (Semana C)

---

## Vítor — Otimização e comparação (Etapa 4)

### Em linguagem simples

Você pega o modelo que já funciona e aplica **pelo menos uma** técnica para ele responder mais rápido. Depois compara: antes vs depois.

### Atividades

#### V4. Aplicar otimização

- [ ] Implementar a técnica escolhida na Fase 0 (ex.: ONNX / quantização / pruning)
- [ ] Gerar artefato do modelo otimizado
- [ ] Garantir que a API (ou script de benchmark) consegue usar a versão otimizada

#### V5. Comparar latência

- [ ] Medir latência do modelo **original**
- [ ] Medir latência do modelo **otimizado**
- [ ] Tabela comparativa (mesmo hardware, mesmo método, N requisições)
- [ ] Salvar em `evidencias/` + trecho no README

**Entregável:** modelo otimizado + resultados comparativos documentados.

### Checkpoint Vítor C — “Otimização demonstrada”

- [ ] ≥ 1 técnica aplicada
- [ ] Números original vs otimizado registrados
- [ ] Time consegue reproduzir a medição

---

## Vini + Fernando — Estabilizar entrega técnica

### Atividades

- [ ] Compose final estável (subir do zero sem gambiarra)
- [ ] Baseline + comparação alinhadas (API com modelo original vs otimizado, se aplicável)
- [ ] Remover mocks / código morto óbvio
- [ ] Revisar erros de validação da API
- [ ] Confirmar ≥ 3 painéis Grafana com dados reais após carga de teste

### Checkpoint Vini/Fernando C — “Demo local confiável”

- [ ] `docker compose up` (ou comando combinado) sobe tudo
- [ ] Fluxo demo: chamar API → ver Grafana atualizar
- [ ] Evidências atualizadas

---

## Edu — Fechamento documental + vídeo STAR

### Em linguagem simples

Você junta as provas de que o projeto funciona e conta a história em até 5 minutos no formato STAR.

### Atividades

#### E5. Coleta de evidências (checklist do vídeo)

- [ ] Números de baseline de latência
- [ ] Tabela original vs otimizado
- [ ] Print/JSON do dashboard Grafana (≥ 3 painéis)
- [ ] Print/link do GitHub Actions verde
- [ ] Demo da DAG (print ou gravação curta)
- [ ] Trechos de arquitetura / Compose / API se precisar no vídeo

#### E6. README final

- [ ] Como executar tudo
- [ ] Estratégia cloud (batch vs real-time) completa
- [ ] Onde ver métricas
- [ ] Como treinar / retreinar
- [ ] Resultados de latência

#### E7. Vídeo STAR (≤ 5 min) — dono: Edu

Roteiro obrigatório:

| Parte | O que cobrir | Status |
|-------|--------------|--------|
| **S — Situation** | Problema clínico: triagem rápida de laudos importa | `[ ]` |
| **T — Task** | Requisitos: latência, CI/CD, monitoramento, etc. | `[ ]` |
| **A — Action** | Arquitetura, otimização, monitoramento | `[ ]` |
| **R — Result** | Pipeline funcionando, latência alcançada, lições | `[ ]` |

- [ ] Vídeo gravado (≤ 5 minutos)
- [ ] Link do vídeo no README (ou local combinado pelo time)

### Checkpoint Edu C — “Entrega acadêmica fechada”

- [ ] README completo
- [ ] Evidências organizadas
- [ ] Vídeo STAR publicado/linkado

---

# Checkpoints gerais do projeto (visão rápida)

Use esta lista na daily / sync semanal.

| ID | Nome | Critério resumido | Status |
|----|------|-------------------|--------|
| C0 | Kickoff | Decisões pendentes fechadas | `[ ]` |
| CA-Vítor | Modelo baseline | Treina, salva, `predict` ok | `[ ]` |
| CA-Vini | API + Docker + baseline | API em Docker + latência inicial | `[ ]` |
| CA-Fernando | Monitoramento | Compose + ≥3 painéis | `[ ]` |
| CA-Edu | CI + DAG + cloud draft | Actions ≥2 + DAG + texto cloud | `[ ]` |
| C2 | Integração | Texto→classe real + métricas + DAG + CI | `[ ]` |
| CC-Vítor | Otimização | Original vs otimizado documentado | `[ ]` |
| CC-Demo | Demo local | Compose estável para apresentação | `[ ]` |
| CC-Edu | Entrega final | README + evidências + vídeo STAR | `[ ]` |

---

# Contratos entre pessoas (para não se bloquear)

| De → Para | O que entregar | Formato mínimo |
|-----------|----------------|----------------|
| **Vítor → Vini** | Modelo + como prever | Arquivo do modelo + `predict(text)` |
| **Vítor → Edu** | Treino automatizável | Script/função: dados → treinar → salvar |
| **Vini → Fernando** | API com métricas | `/metrics` + imagem/serviço no Compose |
| **Vini → Time** | Contrato HTTP estável | Path + JSON in/out |
| **Fernando → Edu** | Prova de monitoramento | Print/JSON Grafana |
| **Todos → Edu** | Evidências do vídeo | Arquivos em `evidencias/` |

### Regras de ouro do trabalho assíncrono

1. **Não quebre o contrato da API** sem avisar o time.
2. **Não mude o path do modelo** sem avisar Vini e Edu.
3. Prefira PRs pequenas por trilha.
4. Se estiver bloqueado > 1 dia, escreva no chat: bloqueio + o que precisa de quem.
5. Commits semânticos (ex.: Conventional Commits), histórico organizado.

---

# Mapa das 4 etapas oficiais da FIAP × donos

| Etapa FIAP | O que é | Quem lidera | Apoio |
|------------|---------|-------------|-------|
| **1** Decisão + API inicial | Cloud no README, FastAPI, Docker, baseline | Vini (API/Docker/baseline) + Edu (texto cloud) | Time nas decisões |
| **2** CI/CD + Airflow | Actions ≥2 + DAG treino/retreino | Edu | Vítor (script de treino) |
| **3** Monitoramento | prometheus_client + Compose + Grafana ≥3 | Fernando | Vini (API) |
| **4** Otimização + vídeo | Modelo otimizado, comparação, STAR | Vítor (modelo) + Edu (vídeo) | Todos (evidências) |

---

# Backlog opcional (só depois do obrigatório)

Não fazer antes de fechar C2 + otimização + vídeo:

- [ ] Autenticação
- [ ] Banco de dados / histórico de laudos
- [ ] Frontend
- [ ] Deploy real em cloud
- [ ] Extra de métricas de qualidade do modelo no Grafana

---

# Syncs mínimos recomendados

| Sync | Quando | Pauta |
|------|--------|-------|
| Kickoff | Início | Fase 0 — decisões |
| Meio | Após Semana A | Destravar integração (paths, contrato, Compose) |
| Pré-vídeo | Antes da gravação | Checklist de evidências + ensaio do roteiro STAR |
| Freeze | 24–48h antes da entrega | Só bug crítico; sem feature nova |

---

# Status do time (atualize aqui)

| Pessoa | Foco agora | Bloqueio | Próximo checkpoint |
|--------|------------|----------|--------------------|
| Vítor | | | CA-Vítor |
| Vini | | | CA-Vini |
| Fernando | | | CA-Fernando |
| Edu | | | CA-Edu |

---

## Referências internas

- Requisitos tipados: `.cursor/context/tech-challenge-requirements.md`
- Objetivos: `.cursor/context/project-goals.md`
- Arquitetura: `.cursor/context/architecture.md`
- Stack: `.cursor/context/tech-stack.md`
- Deploy/execução: `.cursor/context/deployment.md`
