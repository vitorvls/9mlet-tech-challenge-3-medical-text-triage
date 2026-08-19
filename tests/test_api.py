"""Tests for the FastAPI triage API — N2: real model integration."""

from __future__ import annotations

import pytest
from fastapi.testclient import TestClient

from triage.api import app

client = TestClient(app)

SEPSIS_REPORT = (
    "Diagnosis: SEPSIS\n"
    "Sex: F\n"
    "Age: 70\n"
    "Abnormal lab results:\n"
    "- White Blood Cells: 18.2 K/uL (abnormal)\n"
    "- Lactate: 4.1 mmol/L (abnormal)\n"
    "- Creatinine: 2.1 mg/dL (abnormal)"
)

ELECTIVE_REPORT = (
    "Diagnosis: RECURRENT LEFT CAROTID STENOSIS, PRE HYDRATION\n"
    "Sex: M\n"
    "Age: 76\n"
    "Abnormal lab results:\n"
    "- Creatinine: 1.4 mg/dL (abnormal)\n"
    "- Glucose: 145 mg/dL (abnormal)"
)

CARDIAC_ARREST_REPORT = (
    "Diagnosis: VF ARREST\n"
    "Sex: F\n"
    "Age: 79\n"
    "Abnormal lab results:\n"
    "- Creatine Kinase (CK): 4127 IU/L (abnormal)\n"
    "- Glucose: 183 mg/dL (abnormal)"
)


# ---------------------------------------------------------------------------
# Health
# ---------------------------------------------------------------------------


def test_health_returns_200():
    r = client.get("/health")
    assert r.status_code == 200
    body = r.json()
    assert body["status"] == "ok"
    assert isinstance(body["model_loaded"], bool)


# ---------------------------------------------------------------------------
# Predict — happy path
# ---------------------------------------------------------------------------


def test_predict_returns_valid_schema():
    r = client.post("/predict", json={"text": SEPSIS_REPORT})
    assert r.status_code == 200
    body = r.json()
    assert body["label"] in {"normal", "atenção", "urgente"}
    assert 0.0 <= body["confidence"] <= 1.0


def test_predict_sepsis_classified_as_urgente():
    """Sepsis texts should come out urgente with the trained baseline."""
    r = client.post("/predict", json={"text": SEPSIS_REPORT})
    assert r.status_code == 200
    assert r.json()["label"] == "urgente"


def test_predict_elective_classified_as_normal():
    r = client.post("/predict", json={"text": ELECTIVE_REPORT})
    assert r.status_code == 200
    assert r.json()["label"] == "normal"


def test_predict_confidence_is_float():
    r = client.post("/predict", json={"text": CARDIAC_ARREST_REPORT})
    assert r.status_code == 200
    assert isinstance(r.json()["confidence"], float)


# ---------------------------------------------------------------------------
# Predict — validation errors
# ---------------------------------------------------------------------------


def test_predict_rejects_empty_text():
    r = client.post("/predict", json={"text": ""})
    assert r.status_code == 422


def test_predict_rejects_blank_text():
    r = client.post("/predict", json={"text": "   "})
    assert r.status_code == 422


def test_predict_rejects_missing_text_field():
    r = client.post("/predict", json={})
    assert r.status_code == 422


def test_predict_rejects_non_string_text():
    r = client.post("/predict", json={"text": 123})
    assert r.status_code == 422


# ---------------------------------------------------------------------------
# Metrics
# ---------------------------------------------------------------------------


def test_metrics_endpoint_is_accessible():
    r = client.get("/metrics")
    assert r.status_code == 200
    assert "triage_requests_total" in r.text


def test_metrics_populated_after_predict():
    client.post("/predict", json={"text": SEPSIS_REPORT})
    r = client.get("/metrics")
    assert "triage_request_duration_seconds" in r.text
