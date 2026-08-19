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

**Documentação por etapa (obrigatória):** cada integrante grava o histórico didático em `docs/etapas/` (ver `docs/etapas/README.md`). Código sem o `etapa-NN.md` correspondente **não** está concluído.

- Vítor: [`docs/etapas/Modelagem e otimização/TODO.md`](etapas/Modelagem%20e%20otimização/TODO.md) — lista **linear** de execução
- Vini: `docs/etapas/API e Docker/`
- Fernando: `docs/etapas/Monitoramento/`
- Edu: `docs/etapas/CI-CD Airflow e documentacao/`

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

Não gastar tempo com (não são requisito FIAP):

- Banco de dados
- Login, JWT, permissões
- Kubernetes, Redis, microserviços
- Deploy real em AWS/Azure/GCP (só **texto** no README)
- Diagnóstico médico, prescrição ou “substituir o médico”
- Frontend como entrega da rubrica (a API + Swagger já demonstram o serviço)

**Exceção explícita:** uma page de demo (formulário + conversa) ficou no [backlog opcional](#backlog-opcional--só-depois-do-obrigatório), **somente se sobrar tempo**. Não altera modelo, JSON nem endpoints. Sem essa folga, **não fazer**.

---

# FASE 0 — Kickoff do time (todos)

**Objetivo:** destravar o trabalho paralelo. Sem isso, cada um inventa um contrato diferente.

**Duração sugerida:** 1 sync de 45–60 min + registro por escrito neste TODO.

## 0.1 Decisões obrigatórias do time

| # | Decisão | Status | Quem registra |
|---|---------|--------|---------------|
| 1 | Dataset concreto (fonte + link) | `[x]` FECHADO — ver 0.2 | Vítor (2026-08-15) |
| 2 | Labels finais | `[x]` FECHADO — `normal` / `atenção` / `urgente` | Vítor (2026-08-15) |
| 3 | Algoritmo / framework do modelo | `[x]` FECHADO — TF-IDF + Logistic Regression (sklearn) | Vítor (2026-08-15) |
| 4 | Técnica de otimização | `[ ]` PROPOSTO por Vítor: ONNX Runtime (Semana C) — não bloqueia Fase 1 | Vítor propõe; time confirma |
| 5 | Contrato da API (path + HTTP) | `[x]` PARCIAL — JSON in/out fechado (0.2); path/códigos HTTP: Vini | Vítor (JSON) / Vini (HTTP) |
| 6 | Layout mínimo de pastas | `[x]` PARCIAL — trilha do modelo fechada (0.2); resto do repo: time | Vítor (modelo) |
| 7 | Onde o modelo salvo fica e como a API carrega | `[x]` FECHADO — `models/baseline.joblib` | Vítor (2026-08-15) |
| 8 | Linter/formatter e ferramenta de teste | `[ ]` PENDENTE | Edu propõe |
| 9 | Provedor cloud **só para o texto** do README | `[ ]` PENDENTE | Edu propõe |
| 10 | Pasta de evidências (sugestão: `evidencias/`) | `[ ]` PENDENTE | Edu |
| 11 | Page de demo (form + chat) | OPCIONAL — só se sobrar tempo; ver backlog. **Não** bloqueia ninguém | Vítor propõe; Vini hospeda na API |

> Itens 1–3, 7 e o JSON de `predict` estão fechados para a trilha do Vítor começar. Discordância: avisar no chat do grupo. Enquanto não houver discordância, **não reabrir** esses itens sem necessidade.

### 0.2 Decisões fechadas em 2026-08-15 (Vítor — Dia 0)

Registradas para desbloquear o modelo, a API e a DAG. Não são requisito FIAP nomeado; são **DECISÃO DO PROJETO**.

#### Dataset

- **Fonte:** [MIMIC-III Clinical Database (Open Access) no Kaggle](https://www.kaggle.com/datasets/ihssanened/mimic-iii-clinical-databaseopen-access) (recorte público da demo MIMIC-III; não é o MIMIC completo com credencial PhysioNet).
- **Arquivos usados:** `ADMISSIONS.csv`, `PATIENTS.csv`, `LABEVENTS.csv`, `D_LABITEMS.csv`, `structured_medical_records.csv`.
- **Texto (`text`):** laudo simulado em `medical_report`, **sem** campos que vazem o rótulo (não deixar `Admission Type`, óbito etc. no texto de treino/inferência).
- **Tamanho aproximado:** ~100 pacientes, ~129 internações; milhares de laudos simulados (várias linhas podem ser a mesma internação).
- **Licença:** Kaggle marca Unknown; a demo PhysioNet correspondente usa ODbL. Documentar em `docs/dataset.md` na V1.
- **Limitação consciente:** o PDF *recomenda* ≥ 2.000 amostras com texto+target nativos. Este dataset não traz coluna de urgência pronta; o target é **derivado**. Split treino/teste **por internação** (`hadm_id`), não por linha solta.

#### Labels (saída do modelo e da API)

Mapeamento a partir de `ADMISSIONS.admission_type`:

| Campo no MIMIC | Label do projeto |
|----------------|------------------|
| `ELECTIVE` | `normal` |
| `URGENT` | `atenção` |
| `EMERGENCY` | `urgente` |

Valores válidos de `label`: **somente** `normal`, `atenção`, `urgente`. Não inventar outras classes.

Isto **não** é diagnóstico clínico: é um proxy acadêmico do tipo de admissão já registrado no hospital.

#### Algoritmo (Fase 1 / baseline)

- **scikit-learn** `TfidfVectorizer` + `LogisticRegression` (com `class_weight="balanced"` por desbalanceamento: a maioria das admissões é `EMERGENCY`).
- Um único `Pipeline` sklearn salvo em disco (vetorizador + classificador juntos).
- Métrica principal de qualidade: **F1 macro** (accuracy sozinha mente neste dataset).
- Random Forest (exemplo do PDF) **não** é o baseline escolhido: com poucos pacientes, memoriza fácil. Continua válido como alternativa se o time quiser comparar depois.

#### Artefato do modelo (contrato Vítor ↔ Vini ↔ Edu)

- **Path:** `models/baseline.joblib`
- A API carrega **esse** arquivo (joblib do Pipeline).
- A DAG do Edu deve terminar salvando **no mesmo path** (ou chamar o script de treino que já salva aí).
- Não mudar esse path sem avisar Vini e Edu.

#### Função `predict` (contrato de saída)

```python
predict(text: str) -> {"label": str, "confidence": float}
```

- `label`: uma de `normal` | `atenção` | `urgente`
- `confidence`: probabilidade da classe escolhida, entre 0 e 1

#### JSON que a API deve espelhar (Vini)

**Entrada (fechada):**

```json
{
  "text": "texto do laudo médico aqui"
}
```

**Saída de sucesso (fechada):**

```json
{
  "label": "urgente",
  "confidence": 0.91
}
```

**Ainda com o Vini (não bloqueia o modelo):** path HTTP (sugestão: `POST /predict`), `GET /health`, códigos HTTP de validação, `GET /metrics`.

#### Layout mínimo da trilha do modelo (Vítor pode criar já)

```
src/triage/          # prepare_data.py, train.py, predict.py
data/raw/            # CSVs do Kaggle (não precisa versionar o zip bruto)
data/processed/      # train.csv / test.csv (colunas text,label)
models/              # baseline.joblib
docs/dataset.md      # fonte, labels, limitações
```

O restante do repositório (API, compose, dags, CI) o time encaixa sem quebrar esses paths.

### Contrato HTTP (o que ainda é do Vini)

> JSON de negócio está fechado acima. Path e status codes: Vini propõe e registra aqui.

**Path sugerido:** `POST /predict`  
**Métricas:** `GET /metrics` (Prometheus)  
**Health sugerido:** `GET /health`

### Checklist Fase 0

- [x] Dataset escolhido e documentado (nome + link + tamanho aproximado)
- [x] Labels definidas
- [x] Algoritmo proposto e aceito (baseline da trilha do Vítor)
- [ ] Técnica de otimização proposta e aceita (ONNX proposto; confirmação do time)
- [x] Contrato JSON de entrada/saída do `predict` escrito neste arquivo
- [ ] Path HTTP / códigos de status (Vini)
- [x] Estrutura de pastas da trilha do modelo combinada
- [x] Path do artefato do modelo combinado (`models/baseline.joblib`)
- [ ] Ferramentas de lint/teste combinadas (Edu)
- [ ] Estratégia cloud documental (provedor + batch vs real-time) esboçada (Edu)
- [ ] Pasta `evidencias/` criada (Edu)

### Checkpoint 0 — “Podemos trabalhar em paralelo”

**Critério de pronto:** todas as decisões da tabela acima marcadas (ou explicitamente adiadas com prazo).

- Trilha **Vítor**: desbloqueada (dataset, labels, algoritmo, path, `predict`).
- Trilha **Vini**: JSON de saída conhecido; falta só fechar path/HTTP se quiser — pode começar com `POST /predict`.
- Trilha **Edu**: itens 4 (confirmar ONNX), 8, 9 e 10 ainda abertos — **não** bloqueiam o modelo.

- [ ] Checkpoint 0 aprovado pelo time (falta Edu + confirmação silenciosa do grupo)

---

# FASE 1 — Trilhas em paralelo (Semana A)

Cada um avança **sem esperar o modelo perfeito**. Onde faltar o modelo real, use **mock** (resposta fake controlada) até o Vítor entregar o artefato.

---

## Vítor — Modelo e treino (base)

### Em linguagem simples

Você pega um conjunto de textos já classificados (dataset), treina um modelo leve e salva o arquivo do modelo para a API usar.

### Atividades

#### V1. Preparar o dataset

Fonte fechada na seção 0.2 (Kaggle MIMIC-III Open Access).

- [x] Baixar o dataset escolhido (ou usar os CSVs já locais)
- [x] Montar `text` + `label` conforme 0.2 (limpar vazamento de `Admission Type` no texto)
- [x] Documentar em `docs/dataset.md` (fonte, tamanho, licença/uso, mapeamento das labels)
- [x] Separar treino / teste **por `hadm_id`** (não misturar a mesma internação)

**Entregável:** dados prontos no repo (ou script que baixa) + `docs/dataset.md`.

#### V2. Pipeline de treino

- [x] Script Python de treino (carregar → treinar → avaliar → salvar)
- [x] Métricas básicas de qualidade: **F1 macro** (+ accuracy e matriz de confusão)
- [x] Salvar modelo em `models/baseline.joblib`
- [x] README curto: como rodar o treino localmente

**Entregável:** script de treino + arquivo do modelo (ou comando que gera).

#### V3. Interface para a API

- [x] Função `predict(text: str) -> {"label": str, "confidence": float}` (contrato 0.2)
- [x] Documentar como carregar `models/baseline.joblib` (1 exemplo de uso)

**Bloqueia:** Vini (inferência real) e Edu (DAG chama este fluxo).

**Entregável:** módulo/função utilizável pela API e pela DAG.

### Checkpoint Vítor A — “Modelo baseline existe”

- [x] Modelo treinado salva e carrega
- [x] `predict` funciona em pelo menos 3 textos de exemplo
- [x] Path do artefato alinhado: `models/baseline.joblib`

---

## Vini — API + Docker + baseline

### Em linguagem simples

Você cria o serviço web: alguém manda o texto do laudo e recebe a classificação. Depois coloca isso numa “caixa” Docker e mede quanto tempo demora.

### Atividades

#### N1. Skeleton da API (pode começar com mock)

- [x] Projeto FastAPI mínimo
- [x] Endpoint de health (ex.: `GET /health`) — recomendado
- [x] Endpoint de classificação conforme o contrato (ex.: `POST /predict`)
- [x] Validação do input (texto vazio, tipo errado, etc.)
- [x] Enquanto o modelo não chega: mock previsível (ex.: sempre uma label fixa ou regra simples)

**Entregável:** API rodando localmente com o contrato fechado.

#### N2. Integração com o modelo do Vítor

- [x] Trocar mock pelo `predict` real
- [x] Tratar erro se o modelo não carregar
- [x] Testar com textos reais do dataset

**Bloqueia:** Fernando (métricas reais em cima da API) e baseline séria.

#### N3. Docker da API

- [x] `Dockerfile` funcional
- [x] Documentar: build + run
- [x] Confirmar que a API responde **dentro** do container

**Entregável:** API empacotada em Docker.

#### N4. Baseline de latência (Etapa 1 do desafio)

- [x] Definir método de medição (ex.: N requisições locais e média/p95)
- [x] Medir latência da API em Docker (modelo ainda sem otimização final)
- [x] Registrar números em `evidencias/` (tabela simples)

**Entregável:** números de baseline documentados.

### Checkpoint Vini A — “API sobe e responde”

- [x] Contrato da API estável
- [x] Docker build/run ok
- [x] Baseline de latência registrada

---

## Fernando — Monitoramento

### Em linguagem simples

Você faz a API “contar” chamadas e tempos, o Prometheus coleta esses números e o Grafana mostra gráficos. Tudo sobe junto com Docker Compose.

### Atividades

#### F1. Instrumentar a API com `prometheus_client`

> Trabalhe junto com o Vini no mesmo serviço (PR coordenada).

- [x] Expor `GET /metrics`
- [x] Métrica de **contagem de requisições**
- [x] Métrica de **tempo de requisição** (latência)
- [x] (Recomendado) métrica de erros / status HTTP para um painel útil

**Entregável:** API instrumentada.

#### F2. Prometheus

- [x] Configurar Prometheus para fazer scrape da API
- [x] Confirmar que as métricas aparecem no Prometheus

#### F3. Docker Compose (API + Prometheus + Grafana)

- [x] `docker-compose.yml` sobe os 3 serviços juntos
- [x] Documentar portas e como acessar
- [x] Time consegue subir com um comando combinado

**Entregável:** Compose funcional.

#### F4. Grafana (≥ 3 painéis) — pode começar o layout cedo

- [x] Dashboard com **pelo menos 3 painéis**
- [x] Exemplos válidos (FIAP): total de requisições, latência, taxa de erro
- [x] Exportar JSON do dashboard **ou** print claro
- [x] Salvar em `evidencias/`

**Entregável:** dashboard + evidência visual/JSON.

### Checkpoint Fernando A — “Stack de monitoramento sobe”

- [x] Compose sobe API + Prometheus + Grafana
- [x] `/metrics` populando após algumas chamadas
- [x] ≥ 3 painéis visíveis (8 painéis implementados)

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
| C0 | Kickoff | Decisões pendentes fechadas | `[ ]` PARCIAL — modelo desbloqueado; falta Edu |
| CA-Vítor | Modelo baseline | Treina, salva, `predict` ok | `[x]` 2026-08-15 |
| CA-Vini | API + Docker + baseline | API em Docker + latência inicial | `[x]` 2026-08-18 |
| CA-Fernando | Monitoramento | Compose + ≥3 painéis | `[x]` 2026-08-18 |
| CA-Edu | CI + DAG + cloud draft | Actions ≥2 + DAG + texto cloud | `[ ]` |
| C2 | Integração | Texto→classe real + métricas + DAG + CI | `[ ]` |
| CC-Vítor | Otimização | Original vs otimizado documentado | `[ ]` |
| CC-Demo | Demo local | Compose estável para apresentação | `[ ]` |
| CC-Edu | Entrega final | README + evidências + vídeo STAR | `[ ]` |

---

# Contratos entre pessoas (para não se bloquear)

| De → Para | O que entregar | Formato mínimo |
|-----------|----------------|----------------|
| **Vítor → Vini** | Modelo + como prever | `models/baseline.joblib` + `predict(text) -> {label, confidence}` |
| **Vítor → Edu** | Treino automatizável | Script: dados → treinar → salvar em `models/baseline.joblib` |
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

Não fazer autenticação, banco, deploy cloud nem extras de Grafana **antes** de fechar C2 + otimização + vídeo.

A page abaixo é o único extra de interface que o time **já combinou como ideia**. Continua **fora da rubrica**.

---

## Extra Opcional — Page de demo (formulário + atendente)

**Status:** `[ ]` não iniciada · **só começar se sobrar tempo depois do obrigatório**  
**Dono:** Vini (a page vive junto da API) · **Apoio:** Vítor (formato do texto do laudo, igual à Etapa 02) · **Uso no vídeo:** Edu (se existir)

**Por que existe:** diferencial de demo / STAR (“parece um produto”). **Zero peso na nota.**

### Regras duras (não negociar na implementação)

1. **Não interferir** em nada já feito ou já combinado: `prepare_data`, `train.py`, `models/baseline.joblib`, labels, JSON `{"text"}` → `{"label","confidence"}`, paths HTTP que o Vini fechar, métricas, Compose, DAG, CI.
2. **Só consumir** a API e os endpoints **já existentes**. Sem endpoint novo “de chat”, sem segundo classificador, sem mudar o contrato.
3. A page **não classifica**. Quem classifica é sempre o `POST /predict` (ou o path equivalente que o Vini registrar). O front só **monta o `text`** e mostra a resposta.
4. Sem React, npm, Node, banco, JWT, OpenRouter obrigatório. Uma página estática (HTML/CSS/JS) servida pelo FastAPI **ou** aberta contra a API já no ar.
5. Se não der tempo, **não fazer**. A entrega acadêmica permanece completa sem esta page.

### Pré-requisitos (todos `[x]` antes de abrir a primeira linha de HTML)

- [ ] Checkpoint Vítor A (`predict` + `baseline.joblib`)
- [ ] Checkpoint Vini A (API sobe e responde no contrato)
- [ ] Time confirma, no sync, que o obrigatório da rubrica está encaminhado e há folga

### O que seria a page (se formos fazer)

Duas entradas, o mesmo JSON:

| Aba | O usuário | O front | A API |
|-----|-----------|---------|-------|
| Formulário | diagnóstico, sexo, idade, labs | concatena o laudo no formato da Etapa 02 | `POST /predict` |
| Conversa (“atendente”) | responde perguntas curtas | monta **o mesmo** laudo | **o mesmo** `POST /predict` |

A conversa **v1** é roteiro fixo (sem LLM, funciona offline no Compose).  
LLM (OpenRouter etc.) é um **segundo extra** em cima desta page: só conversa; a label **não** pode ser inventada pelo chat.

### Fora desta extra

- Não criar pasta `docs/etapas/Frontend/` como trilha obrigatória.
- Se a page for feita: documentar em `docs/etapas/API e Docker/` (é UI da API), sem reabrir as etapas 01–07 da modelagem.

### Critério de conclusão (somente se o time optar)

- [ ] Page não altera arquivos de modelo/treino nem o contrato JSON
- [ ] Formulário e conversa chamam só endpoints já existentes
- [ ] Demo reproduzível sem chave de LLM
- [ ] `.md` didático na pasta do Vini (`docs/etapas/API e Docker/`)

---

## Outros opcionais (não priorizar)

- [ ] Autenticação
- [ ] Banco de dados / histórico de laudos
- [ ] Deploy real em cloud
- [ ] Extra de métricas de qualidade do modelo no Grafana
- [ ] LLM de verdade no atendente (só depois da page v1, se ainda sobrar tempo)

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
| Vítor | CA-Vítor fechado; próximo = otimização (Semana C / Etapas 06–07) | — | CC-Vítor |
| Vini | CA-Vini fechado; próximo = integração (Semana B) | — | C2 |
| Fernando | CA-Fernando fechado; stack Compose + Prometheus + Grafana pronta | — | C2 |
| Edu | | | CA-Edu |

---

## Referências internas

- Requisitos tipados: `.cursor/context/tech-challenge-requirements.md`
- Objetivos: `.cursor/context/project-goals.md`
- Arquitetura: `.cursor/context/architecture.md`
- Stack: `.cursor/context/tech-stack.md`
- Deploy/execução: `.cursor/context/deployment.md`
- Documentação por etapa: `docs/etapas/README.md` (regra: `.cursor/rules/documentation-rules.md`)
- TODO linear do Vítor: `docs/etapas/Modelagem e otimização/TODO.md`
