"""Load models/baseline.joblib once and expose predict(text) -> {label, confidence}.

This is the Vítor → Vini/Edu contract. The API should call `predict`; it should
not reimplement TF-IDF or load the Pipeline on every request.
"""

from __future__ import annotations

import argparse
import json
import sys
from pathlib import Path
from typing import Any

import joblib
from sklearn.pipeline import Pipeline

ROOT = Path(__file__).resolve().parents[2]
DEFAULT_MODEL_PATH = ROOT / "models" / "baseline.joblib"
LABELS = frozenset({"normal", "atenção", "urgente"})

_pipeline: Pipeline | None = None
_pipeline_path: Path | None = None

EXAMPLE_TEXTS = (
    (
        "eletiva / normal (cirurgia programada, sem /SDA)",
        "Diagnosis: RECURRENT LEFT CAROTID STENOSIS, PRE HYDRATION\n"
        "Sex: M\n"
        "Age: 76\n"
        "Abnormal lab results:\n"
        "- Creatinine: 1.4 mg/dL (abnormal)\n"
        "- Glucose: 145 mg/dL (abnormal)\n"
        "- Hemoglobin: 13.7 g/dL (abnormal)",
    ),
    (
        "urgência / atenção (parada, infarto)",
        "Diagnosis: VF ARREST\n"
        "Sex: F\n"
        "Age: 79\n"
        "Abnormal lab results:\n"
        "- Creatine Kinase (CK): 4127 IU/L (abnormal)\n"
        "- Glucose: 183 mg/dL (abnormal)\n"
        "- White Blood Cells: 14.1 K/uL (abnormal)",
    ),
    (
        "emergência / urgente (sepse)",
        "Diagnosis: SEPSIS\n"
        "Sex: F\n"
        "Age: 70\n"
        "Abnormal lab results:\n"
        "- White Blood Cells: 18.2 K/uL (abnormal)\n"
        "- Lactate: 4.1 mmol/L (abnormal)\n"
        "- Creatinine: 2.1 mg/dL (abnormal)",
    ),
)


def get_pipeline(model_path: Path | None = None) -> Pipeline:
    """Load the sklearn Pipeline once per process (and per path)."""
    global _pipeline, _pipeline_path
    path = (model_path or DEFAULT_MODEL_PATH).resolve()
    if _pipeline is not None and _pipeline_path == path:
        return _pipeline
    if not path.exists():
        raise FileNotFoundError(
            f"Model not found: {path}. Run: python src/triage/train.py"
        )
    loaded = joblib.load(path)
    if not isinstance(loaded, Pipeline):
        raise TypeError(f"Expected sklearn Pipeline in {path}, got {type(loaded)}")
    _pipeline = loaded
    _pipeline_path = path
    return _pipeline


def predict(text: str, model_path: Path | None = None) -> dict[str, Any]:
    """Classify a report. Returns {"label": str, "confidence": float}."""
    if not isinstance(text, str):
        raise TypeError("text must be a string")
    cleaned = text.strip()
    if not cleaned:
        raise ValueError("text must be a non-empty string")

    pipeline = get_pipeline(model_path)
    label = str(pipeline.predict([cleaned])[0])
    if label not in LABELS:
        raise ValueError(f"Model returned unexpected label: {label!r}")

    # confidence = probabilidade da classe escolhida (não é certeza clínica).
    proba = pipeline.predict_proba([cleaned])[0]
    classes = list(pipeline.classes_)
    confidence = float(proba[classes.index(label)])
    return {"label": label, "confidence": round(confidence, 4)}


def parse_args(argv: list[str] | None = None) -> argparse.Namespace:
    parser = argparse.ArgumentParser(
        description="Classify a medical report with models/baseline.joblib."
    )
    parser.add_argument("--text", type=str, default=None, help="Report text to classify")
    parser.add_argument("--model-path", type=Path, default=DEFAULT_MODEL_PATH)
    parser.add_argument(
        "--examples",
        action="store_true",
        help="Run the three documented example reports",
    )
    return parser.parse_args(argv)


def main(argv: list[str] | None = None) -> int:
    args = parse_args(argv)
    if args.text is not None:
        print(json.dumps(predict(args.text, model_path=args.model_path), ensure_ascii=False))
        return 0

    print(f"Model: {args.model_path}")
    for title, sample in EXAMPLE_TEXTS:
        result = predict(sample, model_path=args.model_path)
        print(f"\n# {title}")
        print(json.dumps(result, ensure_ascii=False))
    return 0


if __name__ == "__main__":
    sys.exit(main())
