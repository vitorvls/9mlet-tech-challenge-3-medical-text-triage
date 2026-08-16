# Documentação por etapas (regra dura)

## Objective

Toda implementação neste repositório **só está concluída** quando o código **e** o `.md` da etapa existem. Documentação não é atividade posterior.

---

## Pastas canônicas

```
docs/etapas/
├── Modelagem e otimização/     # Vítor — critério FIAP 20%
├── API e Docker/               # Vini — Etapa 1 FIAP (API, Docker, baseline de latência)
├── Monitoramento/              # Fernando — Prometheus, Grafana, Compose
└── CI-CD Airflow e documentacao/  # Edu — Actions, DAG, README cloud, vídeo STAR
```

Não criar pastas `Frontend/`, `Backend/` genéricas nem outras trilhas **sem** decisão do time. Os nomes acima são as responsabilidades **reais**.

TODO linear da modelagem: `docs/etapas/Modelagem e otimização/TODO.md`.

---

## O que o agente deve fazer

Antes de implementar, identificar **de quem é a trilha**. Depois:

1. Usar (ou criar) a pasta correspondente em `docs/etapas/`.
2. Executar **uma** etapa do TODO linear por vez (não pular dependência).
3. Implementar o código da etapa.
4. Criar ou atualizar `etapa-NN.md` **na mesma pasta**, de forma didática (leigo consegue estudar e reproduzir).
5. Só então marcar `- [x]` no TODO da trilha.
6. Se a etapa mudar depois, atualizar o TODO **e** o `.md`.

**Nenhuma etapa está completa sem o `.md`.**

---

## Conteúdo mínimo de cada `etapa-NN.md`

- Objetivo da etapa
- Problema que estamos resolvendo
- O que foi implementado
- Como funciona internamente
- Tecnologias/bibliotecas e **por que** foram escolhidas
- Alternativas consideradas e por que foram descartadas
- Impacto no resto do sistema (API, DAG, contratos)
- Exemplos práticos
- Configurações e estrutura de arquivos
- Fluxo dos dados
- Limitações e melhorias futuras

Se a etapa for **modelagem / dados / treino / experimento / otimização**, incluir também: dataset, origem, pré-processamento, modelo, hiperparâmetros, split, métricas **explicadas em linguagem simples** (não só o número), resultados, interpretação, experimentos, riscos.

Não documentar diagnóstico médico, prescrição ou frontend/DB/JWT como se fossem requisitos FIAP.

---

## Related

- `docs/etapas/README.md`
- `docs/TODO.md` (quadro do time)
- `.cursor/commands/generate-docs.md`
