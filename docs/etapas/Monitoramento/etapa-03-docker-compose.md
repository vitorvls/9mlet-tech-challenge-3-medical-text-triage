# Etapa 03 — Docker Compose (API + Prometheus + Grafana)

**Trilha:** Monitoramento — Fernando  
**Data:** 2026-08-18  
**Branch:** `feature/monitoring`  
**Atividade:** `F3` do `docs/TODO.md`

---

## 1. Objetivo da etapa

Orquestrar a solução completa de monitoramento através do **Docker Compose**, unindo em uma única rede local os três componentes da arquitetura:
1. **API FastAPI (`api`)**: Serviço de inferência de triagem médica.
2. **Prometheus (`prometheus`)**: Servidor de coleta de métricas a cada 5 segundos.
3. **Grafana (`grafana`)**: Servidor de visualização com provisionamento 100% automático de *data source* e *dashboard*.

---

## 2. Problema que estamos resolvendo

Rodar cada container individualmente (com flags de porta, rede manual e volumes) é propenso a falhas de configuração e retrabalho para o time e avaliadores. 

Com o `docker-compose.yml`, toda a infraestrutura sobe de forma determinística com um único comando (`docker compose up -d`), com resolução interna de nomes DNS (`api`, `prometheus`, `grafana`) e provisionamento *zero-touch*.

---

## 3. O que foi implementado

### 3.1 Arquivo `docker-compose.yml`

```yaml
services:
  api:
    build:
      context: .
      dockerfile: Dockerfile
    container_name: triage-api
    ports:
      - "8000:8000"
    restart: unless-stopped
    healthcheck:
      test: ["CMD-SHELL", "python -c \"import urllib.request; urllib.request.urlopen('http://localhost:8000/health')\" || exit 1"]
      interval: 10s
      timeout: 5s
      retries: 3
      start_period: 5s

  prometheus:
    image: prom/prometheus:v2.53.0
    container_name: triage-prometheus
    ports:
      - "9090:9090"
    volumes:
      - ./monitoring/prometheus/prometheus.yml:/etc/prometheus/prometheus.yml:ro
    command:
      - "--config.file=/etc/prometheus/prometheus.yml"
      - "--storage.tsdb.path=/prometheus"
      - "--web.enable-lifecycle"
    restart: unless-stopped
    depends_on:
      api:
        condition: service_healthy

  grafana:
    image: grafana/grafana:11.1.0
    container_name: triage-grafana
    ports:
      - "3000:3000"
    environment:
      - GF_SECURITY_ADMIN_USER=admin
      - GF_SECURITY_ADMIN_PASSWORD=admin
      - GF_USERS_ALLOW_SIGN_UP=false
      - GF_AUTH_ANONYMOUS_ENABLED=true
      - GF_AUTH_ANONYMOUS_ORG_ROLE=Admin
    volumes:
      - ./monitoring/grafana/provisioning/datasources:/etc/grafana/provisioning/datasources:ro
      - ./monitoring/grafana/provisioning/dashboards:/etc/grafana/provisioning/dashboards:ro
      - ./monitoring/grafana/dashboards:/var/lib/grafana/dashboards:ro
    restart: unless-stopped
    depends_on:
      - prometheus
```

### 3.2 Tabela de Portas e Serviços

| Serviço | Container Name | Porta Host | Porta Container | Descrição |
|---|---|---|---|---|
| **API** | `triage-api` | `8000` | `8000` | API FastAPI (`/health`, `/predict`, `/metrics`, `/docs`) |
| **Prometheus** | `triage-prometheus` | `9090` | `9090` | Interface Web e API do Prometheus |
| **Grafana** | `triage-grafana` | `3000` | `3000` | Dashboards visuais em tempo real |

---

## 4. Como executar a stack

### Subir os serviços:
```bash
docker compose up -d --build
```

### Verificar status dos containers:
```bash
docker compose ps
```

### Visualizar logs:
```bash
# Todos os logs
docker compose logs -f

# Apenas da API
docker compose logs -f api
```

### Parar e remover os containers:
```bash
docker compose down
```

---

## 5. Próximo passo

Prosseguir para a **Etapa 04 (F4)**: Detalhamento dos painéis do Grafana, provisionamento automático e testes com carga de tráfego.
