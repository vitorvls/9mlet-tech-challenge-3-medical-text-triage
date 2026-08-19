# Etapa 02 — Configuração do Prometheus

**Trilha:** Monitoramento — Fernando  
**Data:** 2026-08-18  
**Branch:** `feature/monitoring`  
**Atividade:** `F2` do `docs/TODO.md`

---

## 1. Objetivo da etapa

Configurar o **Prometheus** como servidor de coleta (time-series database) para realizar o *scrape* contínuo do endpoint `/metrics` da API FastAPI, armazenando o histórico temporal de métricas para posterior visualização em painéis no Grafana.

---

## 2. Problema que estamos resolvendo

A API expõe números atuais através de `/metrics`, mas ela não guarda o histórico nem faz agregações temporais (por exemplo: taxa por segundo nos últimos 5 minutos, percentil 95 de latência móvel, contagem cumulativa ao longo do tempo).

O Prometheus resolve isso através do modelo de **coleta periódica (*pull model*)**: em intervalos regulares, ele consulta a API, armazena cada amostra com *timestamp* e disponibiliza a linguagem **PromQL** para realizar cálculos estatísticos e agregações em tempo real.

---

## 3. O que foi implementado

### 3.1 Arquivo de configuração: `monitoring/prometheus/prometheus.yml`

```yaml
global:
  scrape_interval: 5s
  evaluation_interval: 5s

scrape_configs:
  - job_name: "medical-text-triage-api"
    metrics_path: "/metrics"
    static_configs:
      - targets: ["api:8000"]
```

### 3.2 Explicação dos parâmetros

- **`scrape_interval: 5s`**: O Prometheus busca novas métricas da API a cada 5 segundos. Para um ambiente acadêmico/demonstração e para o vídeo STAR, esse intervalo curto garante que os gráficos no Grafana atualizem quase que instantaneamente após o envio de requisições.
- **`job_name: "medical-text-triage-api"`**: Rótulo identificador do serviço dentro do ecossistema Prometheus.
- **`metrics_path: "/metrics"`**: Rota HTTP exposta pela aplicação FastAPI.
- **`targets: ["api:8000"]`**: Endereço e porta de rede interna do container da API definido no Docker Compose.

---

## 4. Como validar se o scrape está funcionando

Quando a stack estiver em execução (via Docker Compose ou local):

1. Acesse o Prometheus em [http://localhost:9090](http://localhost:9090).
2. Vá no menu **Status → Targets**:
   - O target `medical-text-triage-api (1/1 up)` deve estar com estado **UP** (em verde).
3. Na aba **Graph**, teste consultas PromQL como:
   - `triage_requests_total`: exibe a contagem de predições por classe.
   - `triage_request_duration_seconds_count`: número de amostras de latência.
   - `rate(triage_requests_total[1m])`: taxa de requisições por segundo.

---

## 5. Próximo passo

Prosseguir para a **Etapa 03 (F3)**: Criar o `docker-compose.yml` para orquestrar os 3 serviços (API + Prometheus + Grafana) de forma unificada e plug-and-play.
