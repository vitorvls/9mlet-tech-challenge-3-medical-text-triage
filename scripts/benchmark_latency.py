"""Benchmark sklearn vs ONNX inference latency for the triage model.

The script compares the original joblib model with the exported ONNX artifact on a
fixed batch of 1,000 samples and prints the percentage gain in speed.
"""

from __future__ import annotations

import argparse
import json
import statistics
import time
from pathlib import Path

import joblib
import numpy as np
import onnxruntime as ort

ROOT = Path(__file__).resolve().parents[1]
DEFAULT_MODEL_PATH = ROOT / "models" / "baseline.joblib"
DEFAULT_ONNX_PATH = ROOT / "models" / "baseline.onnx"

SAMPLE_TEXTS = [
    "Diagnosis: SEPSIS\nSex: F\nAge: 70\nAbnormal lab results:\n- White Blood Cells: 18.2 K/uL (abnormal)\n- Lactate: 4.1 mmol/L (abnormal)\n- Creatinine: 2.1 mg/dL (abnormal)",
    "Diagnosis: RECURRENT LEFT CAROTID STENOSIS, PRE HYDRATION\nSex: M\nAge: 76\nAbnormal lab results:\n- Creatinine: 1.4 mg/dL (abnormal)\n- Glucose: 145 mg/dL (abnormal)",
    "Diagnosis: VF ARREST\nSex: F\nAge: 79\nAbnormal lab results:\n- Creatine Kinase (CK): 4127 IU/L (abnormal)\n- Glucose: 183 mg/dL (abnormal)",
]


def _make_batch(size: int) -> list[str]:
    return (SAMPLE_TEXTS * ((size // len(SAMPLE_TEXTS)) + 1))[:size]


def _benchmark_sklearn(model, texts: list[str]) -> float:
    start = time.perf_counter()
    model.predict(texts)
    return time.perf_counter() - start


def _benchmark_onnx(session, texts: list[str]) -> float:
    input_name = session.get_inputs()[0].name
    start = time.perf_counter()
    # Perform batched inference instead of loop to match sklearn.predict behavior
    session.run(None, {input_name: np.array(texts, dtype=object).reshape(-1, 1)})
    return time.perf_counter() - start


def compare_latency(
    model_path: Path = DEFAULT_MODEL_PATH,
    onnx_path: Path = DEFAULT_ONNX_PATH,
    samples: int = 1000,
) -> dict[str, float]:
    if not model_path.exists():
        raise FileNotFoundError(f"Missing sklearn model: {model_path}")
    if not onnx_path.exists():
        raise FileNotFoundError(f"Missing ONNX model: {onnx_path}")

    model = joblib.load(model_path)
    session = ort.InferenceSession(str(onnx_path), providers=[
                                   "CPUExecutionProvider"])
    texts = _make_batch(samples)

    sklearn_time = _benchmark_sklearn(model, texts)
    onnx_time = _benchmark_onnx(session, texts)
    gain_pct = ((sklearn_time - onnx_time) / sklearn_time) * \
        100 if sklearn_time else 0.0

    return {
        "samples": samples,
        "sklearn_seconds": round(sklearn_time, 6),
        "onnx_seconds": round(onnx_time, 6),
        "gain_percent": round(gain_pct, 2),
        "speedup_factor": round(sklearn_time / onnx_time, 2) if onnx_time else 0.0,
    }


def parse_args(argv: list[str] | None = None) -> argparse.Namespace:
    parser = argparse.ArgumentParser(
        description="Compare sklearn vs ONNX latency.")
    parser.add_argument("--model-path", type=Path, default=DEFAULT_MODEL_PATH)
    parser.add_argument("--onnx-path", type=Path, default=DEFAULT_ONNX_PATH)
    parser.add_argument("--samples", type=int, default=1000)
    return parser.parse_args(argv)


def main(argv: list[str] | None = None) -> None:
    args = parse_args(argv)
    result = compare_latency(args.model_path, args.onnx_path, args.samples)
    print(json.dumps(result, ensure_ascii=False, indent=2))


if __name__ == "__main__":
    raise SystemExit(main())
