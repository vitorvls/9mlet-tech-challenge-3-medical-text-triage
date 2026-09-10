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


def _benchmark_model(model, inputs: list[str], repeats: int = 1000) -> float:
    times: list[float] = []
    for _ in range(repeats):
        start = time.perf_counter()
        for text in inputs:
            model.predict([text])
        times.append(time.perf_counter() - start)
    return statistics.mean(times)


def _benchmark_onnx(session, inputs: list[str], repeats: int = 1000) -> float:
    input_name = session.get_inputs()[0].name
    times: list[float] = []
    for _ in range(repeats):
        start = time.perf_counter()
        for text in inputs:
            session.run(None, {input_name: np.array([text], dtype=object)})
        times.append(time.perf_counter() - start)
    return statistics.mean(times)


def compare_latency(
    model_path: Path = DEFAULT_MODEL_PATH,
    onnx_path: Path = DEFAULT_ONNX_PATH,
    samples: int = 1000,
) -> dict[str, float]:
    pipeline = joblib.load(model_path)
    session = ort.InferenceSession(str(onnx_path), providers=[
                                   "CPUExecutionProvider"])
    texts = (SAMPLE_TEXTS * ((samples // len(SAMPLE_TEXTS)) + 1))[:samples]

    sk_time = _benchmark_model(pipeline, texts, repeats=1)
    onnx_time = _benchmark_onnx(session, texts, repeats=1)
    gain_pct = ((sk_time - onnx_time) / sk_time) * 100 if sk_time else 0.0

    return {
        "sklearn_mean_seconds": round(sk_time, 6),
        "onnx_mean_seconds": round(onnx_time, 6),
        "gain_percent": round(gain_pct, 2),
    }


def parse_args(argv: list[str] | None = None) -> argparse.Namespace:
    parser = argparse.ArgumentParser(
        description="Compare sklearn vs ONNX latency.")
    parser.add_argument("--model-path", type=Path, default=DEFAULT_MODEL_PATH)
    parser.add_argument("--onnx-path", type=Path, default=DEFAULT_ONNX_PATH)
    parser.add_argument("--samples", type=int, default=1000)
    return parser.parse_args(argv)


def main(argv: list[str] | None = None) -> int:
    args = parse_args(argv)
    result = compare_latency(args.model_path, args.onnx_path, args.samples)
    print(json.dumps(result, ensure_ascii=False, indent=2))
    return 0


if __name__ == "__main__":
    raise SystemExit(main())
