# syntax=docker/dockerfile:1

# ── Stage 1: builder ─────────────────────────────────────────────────────────
FROM python:3.11-slim AS builder

WORKDIR /app

# instala dependências num virtualenv para copiar depois
COPY pyproject.toml ./
COPY src/ ./src/

RUN python -m venv /opt/venv && \
    /opt/venv/bin/pip install --no-cache-dir -e .

# ── Stage 2: runtime ─────────────────────────────────────────────────────────
FROM python:3.11-slim

WORKDIR /app

# copia apenas o venv e o código-fonte da API
COPY --from=builder /opt/venv /opt/venv
COPY --from=builder /app/src ./src

# copia o artefato do modelo
COPY models/baseline.joblib ./models/baseline.joblib

ENV PATH="/opt/venv/bin:$PATH" \
    PYTHONUNBUFFERED=1 \
    # evita criação de .pyc no container
    PYTHONDONTWRITEBYTECODE=1

EXPOSE 8000

# usuário não-root para segurança
RUN useradd --create-home appuser
USER appuser

CMD ["uvicorn", "triage.api:app", "--host", "0.0.0.0", "--port", "8000"]
