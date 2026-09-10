from pathlib import Path

from triage.predict import predict


def test_predict_returns_supported_label():
    result = predict(
        "Diagnosis: SEPSIS\nSex: F\nAge: 70\nAbnormal lab results:\n- Lactate: 4.1 mmol/L (abnormal)")
    assert result["label"] in {"normal", "atenção", "urgente"}
    assert 0.0 <= result["confidence"] <= 1.0


def test_onnx_export_helper_exists():
    from src.models.onnx_export import export_model_to_onnx

    assert callable(export_model_to_onnx)
    assert Path("models").exists()
    out = export_model_to_onnx(
        Path("models/baseline.joblib"), Path("models/test_export.onnx"))
    assert out.exists() and out.suffix == ".onnx"
