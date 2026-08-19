"""Simulate continuous traffic against the medical text triage API.

Sends a mixture of normal, atenção, urgente reports and error cases in a loop
to continuously populate Prometheus metrics and feed Grafana dashboards in real time.
Runs continuously until interrupted (Ctrl+C).

Usage:
    # Execução contínua (padrão - encerra com Ctrl+C):
    python scripts/simulate_traffic.py

    # Execução com intervalo personalizado (ex: a cada 0.3s):
    python scripts/simulate_traffic.py --delay 0.3

    # Execução com número fixo de requisições:
    python scripts/simulate_traffic.py --count 100 --delay 0.1
"""

from __future__ import annotations

import argparse
import json
import random
import sys
import time
import urllib.error
import urllib.request

SAMPLES = [
    # Emergência / Urgente
    {
        "type": "valid",
        "description": "Sepsis Grave",
        "payload": {
            "text": "Diagnosis: SEPSIS, SEPTIC SHOCK\nSex: F\nAge: 70\nAbnormal lab results:\n- White Blood Cells: 18.2 K/uL (abnormal)\n- Lactate: 4.1 mmol/L (abnormal)\n- Creatinine: 2.1 mg/dL (abnormal)"
        },
    },
    {
        "type": "valid",
        "description": "Parada Cardíaca (VF Arrest)",
        "payload": {
            "text": "Diagnosis: VF ARREST, RESUSCITATED\nSex: F\nAge: 79\nAbnormal lab results:\n- Creatine Kinase (CK): 4127 IU/L (abnormal)\n- Glucose: 183 mg/dL (abnormal)\n- White Blood Cells: 14.1 K/uL (abnormal)"
        },
    },
    {
        "type": "valid",
        "description": "Insuficiência Respiratória Aguda",
        "payload": {
            "text": "Diagnosis: ACUTE RESPIRATORY FAILURE, HYPOXEMIA\nSex: M\nAge: 65\nAbnormal lab results:\n- pO2: 55 mm Hg (abnormal)\n- pCO2: 58 mm Hg (abnormal)\n- White Blood Cells: 16.5 K/uL (abnormal)"
        },
    },
    # Eletivo / Normal
    {
        "type": "valid",
        "description": "Estenose Carotídea Eletiva",
        "payload": {
            "text": "Diagnosis: RECURRENT LEFT CAROTID STENOSIS, PRE HYDRATION\nSex: M\nAge: 76\nAbnormal lab results:\n- Creatinine: 1.4 mg/dL (abnormal)\n- Glucose: 145 mg/dL (abnormal)"
        },
    },
    {
        "type": "valid",
        "description": "Cateterismo Cardíaco Agendado",
        "payload": {
            "text": "Diagnosis: CORONARY ARTERY DISEASE, ELECTIVE CATHETERIZATION\nSex: M\nAge: 58\nAbnormal lab results:\n- Cholesterol: 210 mg/dL (abnormal)"
        },
    },
    # Atenção / Urgente
    {
        "type": "valid",
        "description": "Dor Abdominal Aguda",
        "payload": {
            "text": "Diagnosis: ACUTE ABDOMINAL PAIN, SUSPECTED APPENDICITIS\nSex: F\nAge: 32\nAbnormal lab results:\n- White Blood Cells: 13.8 K/uL (abnormal)\n- CRP: 45 mg/L (abnormal)"
        },
    },
    # Casos de Teste de Erro (para painel de erros)
    {
        "type": "invalid",
        "description": "Texto Vazio (Erro 422)",
        "payload": {"text": ""},
    },
    {
        "type": "invalid",
        "description": "Campo Ausente (Erro 422)",
        "payload": {},
    },
]


def send_request(url: str, item: dict) -> tuple[int, str]:
    predict_url = f"{url.rstrip('/')}/predict"
    data = json.dumps(item["payload"]).encode("utf-8")
    req = urllib.request.Request(
        predict_url,
        data=data,
        headers={"Content-Type": "application/json"},
        method="POST",
    )
    try:
        with urllib.request.urlopen(req, timeout=5) as response:
            body = json.loads(response.read().decode("utf-8"))
            return response.status, body.get("label", "unknown")
    except urllib.error.HTTPError as exc:
        if exc.code == 422:
            return exc.code, "erro_validacao (422)"
        return exc.code, f"erro_http ({exc.code})"
    except Exception as exc:
        return 500, f"erro_conexao ({type(exc).__name__})"


def main() -> None:
    parser = argparse.ArgumentParser(
        description="Simulate continuous traffic for Medical Text Triage API (calibrated for 99% availability & 1% error budget).",
        formatter_class=argparse.RawDescriptionHelpFormatter,
    )
    parser.add_argument(
        "--url",
        default="http://localhost:8000",
        help="API base URL (default: http://localhost:8000)",
    )
    parser.add_argument(
        "--count",
        type=int,
        default=0,
        help="Number of requests to send (0 = continuous loop until Ctrl+C, default: 0)",
    )
    parser.add_argument(
        "--delay",
        type=float,
        default=0.3,
        help="Delay between requests in seconds (default: 0.3s)",
    )
    parser.add_argument(
        "--error-rate",
        type=float,
        default=0.01,
        help="Probability of injecting an error request to test SLA (default: 0.01 = 1%% error / 99%% success)",
    )
    args = parser.parse_args()

    # Separa pools de válidos e inválidos
    valid_pool = [s for s in SAMPLES if s["type"] == "valid"]
    invalid_pool = [s for s in SAMPLES if s["type"] == "invalid"]

    is_continuous = args.count <= 0
    total_target = "∞ (contínuo até Ctrl+C)" if is_continuous else str(args.count)

    print("=" * 68)
    print(f"  Medical Text Triage — Gerador Contínuo de Tráfego")
    print(f"  Target URL       : {args.url}")
    print(f"  Modo             : {'Contínuo (pressione Ctrl+C para parar)' if is_continuous else f'Fixo ({args.count} requisições)'}")
    print(f"  Intervalo        : {args.delay}s por requisição")
    print(f"  Taxa de Erro     : {args.error_rate * 100:.1f}% (Alvo SLA Disponibilidade: 99.0%)")
    print(f"  Grafana          : http://localhost:3000")
    print("=" * 68 + "\n")

    counts: dict[str, int] = {}
    success_count = 0
    error_count = 0
    i = 0
    start_time = time.perf_counter()

    try:
        while True:
            i += 1
            if not is_continuous and i > args.count:
                break

            # Sorteia se esta requisição será um erro (1%) ou sucesso (99%)
            if args.error_rate > 0 and random.random() < args.error_rate:
                sample = random.choice(invalid_pool)
            else:
                sample = random.choice(valid_pool)

            status, label_or_err = send_request(args.url, sample)
            counts[label_or_err] = counts.get(label_or_err, 0) + 1

            if status == 200:
                success_count += 1
            else:
                error_count += 1

            count_str = f"{i:05d}" if is_continuous else f"{i:03d}/{args.count}"
            print(f"[{count_str}] Status HTTP: {status} | Predição/Resultado: {label_or_err:<22} ({sample['description']})")
            time.sleep(args.delay)

    except KeyboardInterrupt:
        print("\n\n[!] Interrupção manual solicitada (Ctrl+C). Finalizando...")

    total_time = time.perf_counter() - start_time
    total_requests = sum(counts.values())

    availability_pct = (success_count / total_requests * 100) if total_requests > 0 else 100.0
    error_budget_pct = (error_count / total_requests * 100) if total_requests > 0 else 0.0
    sla_status = "🟢 DENTRO DO SLA (>= 99.0%)" if availability_pct >= 99.0 else "🔴 SLA VIOLADO (< 99.0%)"

    print("\n" + "=" * 68)
    print(f"  Resumo da Simulação & Métricas de SLA")
    print(f"  Total de requisições enviadas : {total_requests}")
    print(f"  Requisições com Sucesso (200) : {success_count}")
    print(f"  Requisições com Falha (4xx)   : {error_count}")
    print(f"  Disponibilidade Alcançada     : {availability_pct:.2f}% ({sla_status})")
    print(f"  Error Budget Consumido        : {error_budget_pct:.2f}% (Meta SLA: <= 1.00%)")
    print(f"  Tempo total decorrido         : {total_time:.2f}s")
    if total_time > 0 and total_requests > 0:
        print(f"  Throughput médio              : {total_requests / total_time:.2f} req/s")
    print("\n  Distribuição dos resultados:")
    for k, v in sorted(counts.items()):
        pct = (v / total_requests * 100) if total_requests > 0 else 0
        print(f"    - {k:<24}: {v:5d} ({pct:5.1f}%)")
    print("=" * 68)
    print("Consulte os gráficos consolidados no Grafana: http://localhost:3000\n")


if __name__ == "__main__":
    main()
