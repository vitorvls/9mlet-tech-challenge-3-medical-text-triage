from __future__ import annotations

import argparse
import json
import sys
from pathlib import Path

import joblib
import numpy as np
import onnxruntime as ort
from skl2onnx import convert_sklearn
from skl2onnx.common.data_types import StringTensorType

ROOT = Path(__file__).resolve().parents[2]
DEFAULT_MODEL_PATH = ROOT / "models" / "baseline.joblib"
DEFAULT_ONNX_PATH = ROOT / "models" / "baseline.onnx"


def export_model_to_onnx(
    model_path: str | Path = DEFAULT_MODEL_PATH,
    onnx_path: str | Path = DEFAULT_ONNX_PATH,
    overwrite: bool = True,
) -> Path:
    """Export a scikit-learn Pipeline to the ONNX format."""
    model_path = Path(model_path)
    onnx_path = Path(onnx_path)

    if not model_path.exists():
        raise FileNotFoundError(f"Model not found: {model_path}")

    pipeline = joblib.load(model_path)
    onnx_model = convert_sklearn(
        pipeline,
        initial_types=[("input", StringTensorType([None]))],
    )

    onnx_path.parent.mkdir(parents=True, exist_ok=True)
    if onnx_path.exists() and not overwrite:
        return onnx_path

    onnx_path.write_bytes(onnx_model.SerializeToString())
    return onnx_path


def predict_onnx(text: str, model_path: str | Path = DEFAULT_ONNX_PATH) -> dict[str, float | str]:
    """Run a single inference using the exported ONNX model."""
    if not isinstance(text, str) or not text.strip():
        raise ValueError("text must be a non-empty string")

    session = ort.InferenceSession(str(model_path), providers=[
                                   "CPUExecutionProvider"])
    input_name = session.get_inputs()[0].name
    output = session.run(None, {input_name: np.array([text], dtype=object)})[0]
    index = int(np.argmax(output, axis=1)[0])
    classes = session.get_outputs()[0].name
    _ = classes
    probabilities = output[0]
    labels = ["normal", "atenção", "urgente"]
    label = labels[index]
    confidence = float(probabilities[index])
    return {"label": label, "confidence": round(confidence, 4)}


def parse_args(argv: list[str] | None = None) -> argparse.Namespace:
    parser = argparse.ArgumentParser(
        description="Export the sklearn pipeline as ONNX.")
    parser.add_argument("--model-path", type=Path, default=DEFAULT_MODEL_PATH)
    parser.add_argument("--onnx-path", type=Path, default=DEFAULT_ONNX_PATH)
    parser.add_argument("--text", type=str, default=None,
                        help="Optional text to test inference")
    return parser.parse_args(argv)


def main(argv: list[str] | None = None) -> int:
    args = parse_args(argv)
    output_path = export_model_to_onnx(args.model_path, args.onnx_path)
    print(f"ONNX export written to {output_path}")

    if args.text is not None:
        print(json.dumps(predict_onnx(args.text, output_path), ensure_ascii=False))
    return 0


if __name__ == "__main__":
    sys.exit(main())
