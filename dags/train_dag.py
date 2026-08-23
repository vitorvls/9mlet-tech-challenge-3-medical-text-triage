from __future__ import annotations

from datetime import datetime
from pathlib import Path

from airflow import DAG
from airflow.operators.python import PythonOperator

from triage.prepare_data import main as prepare_data_main
from triage.train import main as train_main

ROOT = Path(__file__).resolve().parents[1]
DATA_DIR = ROOT / "data" / "processed"
MODEL_PATH = ROOT / "models" / "baseline.joblib"


def ingest_data() -> None:
    """Prepare processed train/test CSVs from the raw dataset."""
    prepare_data_main(
        ["--raw-dir", str(ROOT / "data" / "raw"), "--out-dir", str(DATA_DIR)])


def train_and_export_model() -> None:
    """Train the model and persist it to the model artifact path."""
    train_main(["--data-dir", str(DATA_DIR), "--model-path", str(MODEL_PATH)])


with DAG(
    dag_id="medical_text_triage_training",
    description="Ingest data, train the NLP triage model, and persist the optimized artifact.",
    start_date=datetime(2026, 1, 1),
    schedule_interval=None,
    catchup=False,
    tags=["ml", "triage"],
) as dag:
    ingest_task = PythonOperator(
        task_id="ingest_data",
        python_callable=ingest_data,
    )

    train_task = PythonOperator(
        task_id="train_and_export_model",
        python_callable=train_and_export_model,
    )

    ingest_task >> train_task
