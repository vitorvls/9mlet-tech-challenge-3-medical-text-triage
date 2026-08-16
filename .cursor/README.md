# `.cursor` — Contexto para Agentes e Desenvolvedores

## 1. Propósito

Esta pasta é o **sistema de contexto** do projeto `9mlet-tech-challenge-3-medical-text-triage`.

Serve para que humanos e agentes de IA compreendam:

- o problema e o domínio;
- o que a FIAP exige vs. o que é apenas exemplo;
- decisões já tomadas e decisões pendentes;
- stack, regras, libs e comandos reutilizáveis;
- como entregar o Tech Challenge **sem superengenharia**.

Esta pasta **não** contém a implementação da API, modelo, DAG ou infraestrutura. Documenta o que deve ser construído.

---

## 2. Fonte de verdade

| Prioridade | Fonte |
|------------|--------|
| 1 (máxima) | PDF oficial: `MLET - Tech Challenge Fase 3.pdf` |
| 2 | `.cursor/context/tech-challenge-requirements.md` |
| 3 | Decisões explícitas do projeto (marcadas nos arquivos de context) |
| 4 | Demais arquivos `.cursor/` |

Em conflito: **PDF > requirements tipados > decisões explícitas > resto**.

---

## 3. Ordem recomendada de leitura (agentes)

1. Este `README.md`
2. `context/tech-challenge-requirements.md` ← **começar sempre por aqui antes de implementar**
3. `context/project-goals.md`
4. `context/architecture.md`
5. `context/tech-stack.md`
6. `context/deployment.md`
7. `rules/*` (regras duras — incluir `documentation-rules.md`)
8. `libs/*` (dependências)
9. O `commands/*` relevante à tarefa
10. TODO da trilha em `docs/etapas/<pasta>/TODO.md` quando for implementar

---

## 4. Hierarquia de autoridade e tipos de arquivo

| Pasta | Papel |
|-------|--------|
| `context/` | Como o projeto pensa: requisitos, goals, arquitetura, stack, deploy |
| `rules/` | Regras duras (contrato com a IA) |
| `libs/` | Allowlist / denylist / modelos de IA de assistência |
| `commands/` | Prompts executáveis reutilizáveis |

---

## 5. Requisitos vs decisões

- **OBRIGATÓRIO / EXEMPLO FIAP / RECOMENDAÇÃO / FORA DO ESCOPO** → ver `tech-challenge-requirements.md`
- **DECISÃO DO PROJETO** → escolha interna documentada (não inventar como requisito FIAP)
- **PENDENTE DE DECISÃO** → agentes **não** escolhem sozinhos; pedem aprovação humana ou deixam marcado

Nunca transformar exemplo do PDF (ex.: ONNX, TF-IDF+RF, lint→test→build) em única opção obrigatória.

---

## 6. Onde estão as decisões pendentes

Lista canônica em:

`context/tech-challenge-requirements.md` → seção **Decisões pendentes**

Inclui (enquanto não forem decididas): técnica de otimização (ONNX proposto), linter/formatter, path HTTP, provedor cloud documental, etc. Dataset, labels, algoritmo e artefato do modelo: ver `docs/TODO.md` §0.2 (fechados).

---

## 7. Regra anti-overengineering

Privilegiar a **solução mais simples** que cumpra as 4 etapas e os critérios de avaliação (Modelagem 20%, Monitoramento 20%, CI/CD 15%, Airflow 15%, README 15%, Vídeo 15%).

Não introduzir frontend, banco, JWT, Redis, Kubernetes, microserviços ou deploy cloud real **sem** necessidade concreta, decisão explícita e justificativa.

Não interpretar o sistema como diagnóstico médico ou substituto de profissionais de saúde.

---

## 8. Estrutura

```
.cursor/
├── README.md
├── context/
│   ├── tech-challenge-requirements.md  # fonte tipada FIAP
│   ├── project-goals.md
│   ├── architecture.md
│   ├── tech-stack.md
│   └── deployment.md
├── rules/
│   ├── ai-usage-rules.md
│   ├── business-rules.md
│   ├── code-style.md
│   ├── git-rules.md
│   ├── security-rules.md
│   ├── testing-rules.md
│   └── documentation-rules.md   # docs/etapas obrigatória por trilha
├── libs/
│   ├── allowed-libs.md
│   ├── forbidden-libs.md
│   └── ai-models.md
└── commands/
    ├── kickoff-project.md
    ├── architecture-review.md
    ├── extract-business-rules.md
    ├── test-strategy.md
    ├── generate-boilerplate.md
    ├── refactor-controlled.md
    ├── generate-docs.md
    ├── review-pr.md
    ├── challenge-solution.md
    └── pre-delivery-validation.md
```

---

## 9. Princípios

- Contexto explícito > prompt genérico
- Classificar requisitos antes de implementar
- IA propõe; humanos aprovam decisões arquiteturais e pendentes
- Documentação viva: atualizar `.cursor` quando decisões mudarem
- **Documentação por etapa:** código sem `docs/etapas/<trilha>/etapa-NN.md` **não** está concluído (ver `rules/documentation-rules.md`)
