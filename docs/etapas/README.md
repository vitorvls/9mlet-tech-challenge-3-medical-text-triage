# Trilha de etapas (documentação obrigatória)

Cada integrante tem **uma pasta**. Cada passo de implementação gera um `etapa-NN.md` **antes** de a tarefa ser considerada feita.

```
docs/etapas/
├── Modelagem e otimização/        # Vítor
├── API e Docker/                  # Vini
├── Monitoramento/                 # Fernando
└── CI-CD Airflow e documentacao/  # Edu
```

| Pasta | Dono | O que entra aqui |
|-------|------|------------------|
| `Modelagem e otimização/` | Vítor | Dataset processado, treino, `predict`, ONNX, latência do modelo |
| `API e Docker/` | Vini | FastAPI, contrato HTTP, Dockerfile, baseline de latência da API |
| `Monitoramento/` | Fernando | `prometheus_client`, Compose, Grafana |
| `CI-CD Airflow e documentacao/` | Edu | GitHub Actions, DAG, README cloud, evidências do vídeo STAR |

Não criar pasta `Frontend/` como trilha obrigatória. Uma page de demo (form + chat) é **extra opcional** no `docs/TODO.md` (backlog): só se sobrar tempo, só consome a API já existente, documentar em `API e Docker/` se for feita. Não misturar trilhas no mesmo `etapa-NN.md`.

Regra dura: `.cursor/rules/documentation-rules.md` (espelho em `.github/rules/`).

TODO executável da modelagem: [`Modelagem e otimização/TODO.md`](Modelagem%20e%20otimização/TODO.md).
