"""Train TF-IDF + Logistic Regression and save models/baseline.joblib.

Reads data/processed/train.csv and test.csv (columns: text, label).
The Pipeline (vectorizer + classifier) is stored as a single file so the API
and the Airflow DAG load one path.
"""

from __future__ import annotations

import argparse
import sys
from pathlib import Path

import joblib
import pandas as pd
from sklearn.feature_extraction.text import TfidfVectorizer
from sklearn.linear_model import LogisticRegression
from sklearn.metrics import (
    accuracy_score,
    classification_report,
    confusion_matrix,
    f1_score,
)
from sklearn.pipeline import Pipeline

ROOT = Path(__file__).resolve().parents[2]
DEFAULT_DATA_DIR = ROOT / "data" / "processed"
DEFAULT_MODEL_PATH = ROOT / "models" / "baseline.joblib"

LABELS = ("normal", "atenção", "urgente")
RANDOM_STATE = 42
MAX_ITER = 1000


def load_split(path: Path) -> tuple[pd.Series, pd.Series]:
    if not path.exists():
        raise FileNotFoundError(
            f"Missing {path}. Run: python src/triage/prepare_data.py"
        )
    df = pd.read_csv(path, encoding="utf-8")
    missing = [c for c in ("text", "label") if c not in df.columns]
    if missing:
        raise ValueError(f"{path} missing columns: {missing}")
    df = df.dropna(subset=["text", "label"])
    unknown = sorted(set(df["label"].astype(str)) - set(LABELS))
    if unknown:
        raise ValueError(f"{path} has unexpected labels: {unknown}")
    return df["text"].astype(str), df["label"].astype(str)


def build_pipeline() -> Pipeline:
    return Pipeline(
        steps=[
            (
                "tfidf",
                TfidfVectorizer(
                    lowercase=True,
                    ngram_range=(1, 1),
                    min_df=1,
                    stop_words="english",
                ),
            ),
            (
                "clf",
                LogisticRegression(
                    class_weight="balanced",
                    max_iter=MAX_ITER,
                    solver="lbfgs",
                    random_state=RANDOM_STATE,
                ),
            ),
        ]
    )


def evaluate(name: str, y_true: pd.Series, y_pred: list[str]) -> dict[str, float]:
    acc = accuracy_score(y_true, y_pred)
    f1_macro = f1_score(y_true, y_pred, average="macro", labels=list(LABELS), zero_division=0)
    print(f"\n=== {name} ===")
    print(f"n={len(y_true)}")
    print(f"accuracy={acc:.4f}")
    print(f"f1_macro={f1_macro:.4f}")
    print("confusion matrix (rows=true, cols=pred):")
    matrix = confusion_matrix(y_true, y_pred, labels=list(LABELS))
    print(pd.DataFrame(matrix, index=list(LABELS), columns=list(LABELS)).to_string())
    print("per-class report:")
    print(
        classification_report(
            y_true,
            y_pred,
            labels=list(LABELS),
            digits=4,
            zero_division=0,
        )
    )
    return {"accuracy": float(acc), "f1_macro": float(f1_macro)}


def parse_args(argv: list[str] | None = None) -> argparse.Namespace:
    parser = argparse.ArgumentParser(
        description="Train TF-IDF + Logistic Regression and save models/baseline.joblib."
    )
    parser.add_argument("--data-dir", type=Path, default=DEFAULT_DATA_DIR)
    parser.add_argument("--model-path", type=Path, default=DEFAULT_MODEL_PATH)
    return parser.parse_args(argv)


def main(argv: list[str] | None = None) -> int:
    args = parse_args(argv)
    x_train, y_train = load_split(args.data_dir / "train.csv")
    x_test, y_test = load_split(args.data_dir / "test.csv")

    pipeline = build_pipeline()
    pipeline.fit(x_train, y_train)

    evaluate("train", y_train, pipeline.predict(x_train).tolist())
    evaluate("test", y_test, pipeline.predict(x_test).tolist())

    args.model_path.parent.mkdir(parents=True, exist_ok=True)
    joblib.dump(pipeline, args.model_path)
    print(f"Wrote {args.model_path}")
    return 0


if __name__ == "__main__":
    sys.exit(main())
