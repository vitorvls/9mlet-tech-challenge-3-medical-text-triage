"""Latency baseline benchmark for the triage API.

Sends N sequential POST /predict requests and reports mean, p50, p95, p99, min
and max latency. Run against a live API (local or Docker container).

Usage:
    python scripts/benchmark_latency.py
    python scripts/benchmark_latency.py --url http://localhost:8000 --n 200
"""

from __future__ import annotations

import argparse
import csv
import json
import statistics
import time
import urllib.error
import urllib.request
from datetime import datetime, timezone
from pathlib import Path

ROOT = Path(__file__).resolve().parents[1]

SAMPLE_TEXTS = [
    (
        "sepsis",
        "Diagnosis: SEPSIS\nSex: F\nAge: 70\n"
        "Abnormal lab results:\n"
        "- White Blood Cells: 18.2 K/uL (abnormal)\n"
        "- Lactate: 4.1 mmol/L (abnormal)\n"
        "- Creatinine: 2.1 mg/dL (abnormal)",
    ),
    (
        "elective",
        "Diagnosis: RECURRENT LEFT CAROTID STENOSIS, PRE HYDRATION\n"
        "Sex: M\nAge: 76\n"
        "Abnormal lab results:\n"
        "- Creatinine: 1.4 mg/dL (abnormal)\n"
        "- Glucose: 145 mg/dL (abnormal)",
    ),
    (
        "cardiac_arrest",
        "Diagnosis: VF ARREST\nSex: F\nAge: 79\n"
        "Abnormal lab results:\n"
        "- Creatine Kinase (CK): 4127 IU/L (abnormal)\n"
        "- Glucose: 183 mg/dL (abnormal)\n"
        "- White Blood Cells: 14.1 K/uL (abnormal)",
    ),
]


def _post_predict(url: str, text: str) -> float:
    """Return latency in seconds for one POST /predict call."""
    payload = json.dumps({"text": text}).encode()
    req = urllib.request.Request(
        url,
        data=payload,
        headers={"Content-Type": "application/json"},
        method="POST",
    )
    start = time.perf_counter()
    with urllib.request.urlopen(req, timeout=30) as resp:  # noqa: S310
        resp.read()
    return time.perf_counter() - start


def benchmark(base_url: str, n: int) -> list[float]:
    latencies: list[float] = []
    predict_url = base_url.rstrip("/") + "/predict"
    texts = [t for _, t in SAMPLE_TEXTS]
    print(f"Sending {n} requests to {predict_url} ...")
    for i in range(n):
        text = texts[i % len(texts)]
        try:
            latencies.append(_post_predict(predict_url, text))
        except (urllib.error.URLError, TimeoutError) as exc:
            print(f"  request {i + 1} failed: {exc}")
    return latencies


def report(latencies: list[float], n: int, base_url: str) -> dict:
    if not latencies:
        print("No successful requests.")
        return {}

    def p(pct: float) -> float:
        return statistics.quantiles(latencies, n=100)[int(pct) - 1]

    result = {
        "timestamp": datetime.now(timezone.utc).isoformat(),
        "target_url": base_url,
        "n_requested": n,
        "n_succeeded": len(latencies),
        "mean_ms": round(statistics.mean(latencies) * 1000, 2),
        "median_ms": round(statistics.median(latencies) * 1000, 2),
        "p95_ms": round(p(95) * 1000, 2),
        "p99_ms": round(p(99) * 1000, 2),
        "min_ms": round(min(latencies) * 1000, 2),
        "max_ms": round(max(latencies) * 1000, 2),
    }

    print("\n=== Latency Baseline ===")
    print(f"  n          : {result['n_succeeded']} / {result['n_requested']}")
    print(f"  mean       : {result['mean_ms']} ms")
    print(f"  median(p50): {result['median_ms']} ms")
    print(f"  p95        : {result['p95_ms']} ms")
    print(f"  p99        : {result['p99_ms']} ms")
    print(f"  min        : {result['min_ms']} ms")
    print(f"  max        : {result['max_ms']} ms")
    return result


def save_results(result: dict, out_dir: Path) -> None:
    out_dir.mkdir(parents=True, exist_ok=True)
    ts = datetime.now(timezone.utc).strftime("%Y%m%dT%H%M%SZ")
    json_path = out_dir / f"latency_baseline_{ts}.json"
    json_path.write_text(json.dumps(result, indent=2, ensure_ascii=False))
    print(f"\nResults saved to {json_path}")

    csv_path = out_dir / "latency_baseline_summary.csv"
    write_header = not csv_path.exists()
    with csv_path.open("a", newline="") as f:
        writer = csv.DictWriter(f, fieldnames=list(result.keys()))
        if write_header:
            writer.writeheader()
        writer.writerow(result)
    print(f"Summary appended to {csv_path}")


def parse_args(argv: list[str] | None = None) -> argparse.Namespace:
    parser = argparse.ArgumentParser(description="API latency baseline benchmark")
    parser.add_argument(
        "--url",
        default="http://localhost:8000",
        help="Base URL of the API (default: http://localhost:8000)",
    )
    parser.add_argument(
        "--n",
        type=int,
        default=100,
        help="Number of requests to send (default: 100)",
    )
    parser.add_argument(
        "--out-dir",
        type=Path,
        default=ROOT / "evidencias",
        help="Directory to save results (default: evidencias/)",
    )
    return parser.parse_args(argv)


def main(argv: list[str] | None = None) -> None:
    args = parse_args(argv)
    latencies = benchmark(args.url, args.n)
    result = report(latencies, args.n, args.url)
    if result:
        save_results(result, args.out_dir)


if __name__ == "__main__":
    main()
