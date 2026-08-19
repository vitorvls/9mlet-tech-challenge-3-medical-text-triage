"""FastAPI application for medical report triage.

Endpoints:
  GET  /health   — liveness check
  POST /predict  — classify a report text
  GET  /metrics  — Prometheus metrics (populated after /predict calls)
"""

from __future__ import annotations

import logging
import time
from contextlib import asynccontextmanager
from pathlib import Path

from fastapi import FastAPI, HTTPException, Request
from fastapi.responses import PlainTextResponse
from prometheus_client import (
    CONTENT_TYPE_LATEST,
    Counter,
    Histogram,
    generate_latest,
)
from pydantic import BaseModel, field_validator

logger = logging.getLogger("triage.api")

# ---------------------------------------------------------------------------
# Prometheus instruments
# ---------------------------------------------------------------------------

_REQUEST_COUNT = Counter(
    "triage_requests_total",
    "Total prediction requests",
    ["label"],
)
_REQUEST_LATENCY = Histogram(
    "triage_request_duration_seconds",
    "End-to-end prediction latency in seconds",
)
_ERROR_COUNT = Counter(
    "triage_errors_total",
    "Total prediction errors",
    ["error_type"],
)

# ---------------------------------------------------------------------------
# Schemas
# ---------------------------------------------------------------------------


class PredictRequest(BaseModel):
    text: str

    @field_validator("text")
    @classmethod
    def text_must_not_be_blank(cls, v: str) -> str:
        if not v or not v.strip():
            raise ValueError("text must not be empty or blank")
        return v


class PredictResponse(BaseModel):
    label: str
    confidence: float


class HealthResponse(BaseModel):
    status: str
    model_loaded: bool


# ---------------------------------------------------------------------------
# Model loading (lazy, once per process)
# ---------------------------------------------------------------------------

_MODEL_PATH = Path(__file__).resolve().parents[2] / "models" / "baseline.joblib"
_model_loaded: bool = False
_model_error: str | None = None


def _try_load_model() -> None:
    """Attempt to warm up the model cache at startup."""
    global _model_loaded, _model_error
    try:
        from triage.predict import get_pipeline

        get_pipeline(_MODEL_PATH)
        _model_loaded = True
        logger.info("Model loaded from %s", _MODEL_PATH)
    except Exception as exc:  # noqa: BLE001
        _model_error = str(exc)
        logger.warning("Model not loaded at startup: %s", exc)


@asynccontextmanager
async def lifespan(application: FastAPI):  # noqa: ARG001
    _try_load_model()
    yield


app = FastAPI(
    title="Medical Text Triage",
    description="Classifies a medical report as normal / atenção / urgente.",
    version="1.0.0",
    lifespan=lifespan,
)


# ---------------------------------------------------------------------------
# Endpoints
# ---------------------------------------------------------------------------


@app.get("/health", response_model=HealthResponse, tags=["ops"])
def health() -> HealthResponse:
    return HealthResponse(status="ok", model_loaded=_model_loaded)


@app.post("/predict", response_model=PredictResponse, tags=["inference"])
def predict_endpoint(payload: PredictRequest, request: Request) -> PredictResponse:
    start = time.perf_counter()
    try:
        result = _run_predict(payload.text)
    except HTTPException:
        _ERROR_COUNT.labels(error_type="http").inc()
        raise
    except Exception:
        _ERROR_COUNT.labels(error_type="internal").inc()
        raise
    finally:
        _REQUEST_LATENCY.observe(time.perf_counter() - start)

    _REQUEST_COUNT.labels(label=result["label"]).inc()
    return PredictResponse(**result)


def _run_predict(text: str) -> dict:
    if not _model_loaded:
        # retenta carregar em caso de cold start sem modelo
        _try_load_model()
    if not _model_loaded:
        raise HTTPException(
            status_code=503,
            detail="Model unavailable. Run: python src/triage/train.py",
        )
    try:
        from triage.predict import predict

        return predict(text, model_path=_MODEL_PATH)
    except FileNotFoundError as exc:
        raise HTTPException(status_code=503, detail=str(exc)) from exc
    except (TypeError, ValueError) as exc:
        raise HTTPException(status_code=422, detail=str(exc)) from exc


@app.get("/metrics", tags=["ops"])
def metrics() -> PlainTextResponse:
    return PlainTextResponse(
        content=generate_latest().decode("utf-8"),
        media_type=CONTENT_TYPE_LATEST,
    )
