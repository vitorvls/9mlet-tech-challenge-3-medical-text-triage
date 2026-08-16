"""Build train/test CSVs (text, label) from the MIMIC-III demo tables.

One row per hospital admission (hadm_id). The simulated report never includes
admission type, death flags, identifiers, or the /SDA elective marker.
"""

from __future__ import annotations

import argparse
import random
import re
import sys
from pathlib import Path

import pandas as pd

ROOT = Path(__file__).resolve().parents[2]
DEFAULT_RAW_DIR = ROOT / "data" / "raw"
DEFAULT_OUT_DIR = ROOT / "data" / "processed"

LABEL_MAP = {
    "ELECTIVE": "normal",
    "URGENT": "atenção",
    "EMERGENCY": "urgente",
}

MAX_ABNORMAL_LABS = 20
TEST_SIZE = 0.20
RANDOM_STATE = 42
HIPAA_AGE_YEARS = 90

# /SDA = Same Day Admission, quase só nas eletivas deste recorte (vazamento).
SDA_RE = re.compile(r"\s*/SDA\b", flags=re.IGNORECASE)
WHITESPACE_RE = re.compile(r"\s+")
LEAK_RE = re.compile(
    r"admission type|hospital_expire|expire_flag|\bemergency\b|\belective\b|\burgent\b"
    r"|\bdeceased\b|\bexpired\b|\bpatient id\b|\bsubject_id\b",
    flags=re.IGNORECASE,
)


def clean_diagnosis(raw: str) -> str:
    """Remove administrative markers that correlate with the label."""
    text = str(raw or "").strip()
    text = SDA_RE.sub("", text)
    text = text.replace("\\", "; ")
    text = WHITESPACE_RE.sub(" ", text).strip(" ;")
    return text or "not recorded"


def age_at_admission(dob: pd.Timestamp, admittime: pd.Timestamp) -> int:
    """Age in whole years. MIMIC shifts DOB of patients >89 to ~300 years.

    pandas.Timedelta overflows on that 300-year gap, so we subtract
    datetime.datetime values instead.
    """
    delta = admittime.to_pydatetime() - dob.to_pydatetime()
    age = delta.days / 365.25
    if age >= 150:
        return HIPAA_AGE_YEARS
    return max(0, int(round(age)))


def build_report(diagnosis: str, sex: str, age: int, lab_lines: list[str]) -> str:
    parts = [
        f"Diagnosis: {diagnosis}",
        f"Sex: {sex}",
        f"Age: {age}",
    ]
    if lab_lines:
        parts.append("Abnormal lab results:")
        parts.extend(lab_lines)
    else:
        parts.append("Abnormal lab results: none recorded")
    return "\n".join(parts)


def format_lab_line(row: pd.Series) -> str | None:
    name = str(row.get("lab_name") or "").strip()
    if not name:
        return None
    value = str(row.get("value") or "").strip()
    unit = str(row.get("valueuom") or "").strip()
    if value and unit:
        return f"- {name}: {value} {unit} (abnormal)"
    if value:
        return f"- {name}: {value} (abnormal)"
    return f"- {name} (abnormal)"


def load_admissions(raw_dir: Path) -> pd.DataFrame:
    path = raw_dir / "ADMISSIONS.csv"
    if not path.exists():
        raise FileNotFoundError(f"Missing {path}")
    df = pd.read_csv(path)
    needed = ["hadm_id", "subject_id", "admittime", "admission_type", "diagnosis"]
    missing = [c for c in needed if c not in df.columns]
    if missing:
        raise ValueError(f"ADMISSIONS.csv missing columns: {missing}")
    unknown = sorted(set(df["admission_type"].dropna().unique()) - set(LABEL_MAP))
    if unknown:
        raise ValueError(f"Unexpected admission_type values: {unknown}")
    return df[needed].copy()


def load_patients(raw_dir: Path) -> pd.DataFrame:
    path = raw_dir / "PATIENTS.csv"
    if not path.exists():
        raise FileNotFoundError(f"Missing {path}")
    df = pd.read_csv(path)
    needed = ["subject_id", "gender", "dob"]
    missing = [c for c in needed if c not in df.columns]
    if missing:
        raise ValueError(f"PATIENTS.csv missing columns: {missing}")
    return df[needed].copy()


def load_abnormal_labs(raw_dir: Path) -> pd.DataFrame:
    lab_path = raw_dir / "LABEVENTS.csv"
    dict_path = raw_dir / "D_LABITEMS.csv"
    if not lab_path.exists():
        raise FileNotFoundError(f"Missing {lab_path}")
    if not dict_path.exists():
        raise FileNotFoundError(f"Missing {dict_path}")

    labs = pd.read_csv(lab_path)
    items = pd.read_csv(dict_path)[["itemid", "label"]].rename(columns={"label": "lab_name"})

    labs = labs.dropna(subset=["hadm_id", "itemid"])
    labs["hadm_id"] = labs["hadm_id"].astype(int)
    labs["itemid"] = labs["itemid"].astype(int)
    flag = labs["flag"].fillna("").astype(str).str.lower()
    labs = labs.loc[flag == "abnormal", ["hadm_id", "itemid", "charttime", "value", "valueuom"]]
    labs["charttime"] = pd.to_datetime(labs["charttime"], errors="coerce")
    labs = labs.merge(items, on="itemid", how="left")
    labs = labs.sort_values(["hadm_id", "charttime", "itemid"])
    # Primeira ocorrência de cada exame na internação (mais perto da admissão).
    labs = labs.drop_duplicates(subset=["hadm_id", "lab_name"], keep="first")
    return labs


def lab_lines_by_hadm(labs: pd.DataFrame) -> dict[int, list[str]]:
    grouped: dict[int, list[str]] = {}
    for hadm_id, group in labs.groupby("hadm_id", sort=False):
        lines: list[str] = []
        for _, row in group.head(MAX_ABNORMAL_LABS).iterrows():
            line = format_lab_line(row)
            if line:
                lines.append(line)
        grouped[int(hadm_id)] = lines
    return grouped


def build_dataset(raw_dir: Path) -> pd.DataFrame:
    admissions = load_admissions(raw_dir)
    patients = load_patients(raw_dir)
    labs = load_abnormal_labs(raw_dir)
    lab_map = lab_lines_by_hadm(labs)

    df = admissions.merge(patients, on="subject_id", how="left")
    if df["gender"].isna().any() or df["dob"].isna().any():
        missing_n = int(df["gender"].isna().sum())
        raise ValueError(f"{missing_n} admissions without a matching PATIENTS row")

    df["admittime"] = pd.to_datetime(df["admittime"], errors="coerce")
    df["dob"] = pd.to_datetime(df["dob"], errors="coerce")
    df["label"] = df["admission_type"].map(LABEL_MAP)
    df["diagnosis_clean"] = df["diagnosis"].map(clean_diagnosis)
    df["age"] = [
        age_at_admission(dob, admit) for dob, admit in zip(df["dob"], df["admittime"])
    ]
    df["text"] = [
        build_report(
            diagnosis=row.diagnosis_clean,
            sex=str(row.gender).strip() or "U",
            age=int(row.age),
            lab_lines=lab_map.get(int(row.hadm_id), []),
        )
        for row in df.itertuples(index=False)
    ]
    return df[["hadm_id", "text", "label"]].copy()


def assert_no_label_leakage(texts: pd.Series) -> None:
    offenders = []
    for i, text in enumerate(texts.astype(str)):
        if LEAK_RE.search(text) or "Admission Type" in text:
            offenders.append(i)
    if offenders:
        raise ValueError(
            f"Label leakage in {len(offenders)} reports (e.g. index {offenders[0]})"
        )


def split_by_hadm(
    df: pd.DataFrame,
    test_size: float = TEST_SIZE,
    random_state: int = RANDOM_STATE,
) -> tuple[pd.DataFrame, pd.DataFrame]:
    """Keep the same admission on only one side; put at least one of each label in test."""
    rng = random.Random(random_state)
    train_ids: list[int] = []
    test_ids: list[int] = []

    for _label, group in df.groupby("label", sort=True):
        ids = group["hadm_id"].astype(int).tolist()
        rng.shuffle(ids)
        n = len(ids)
        if n < 2:
            train_ids.extend(ids)
            continue
        n_test = max(1, int(round(n * test_size)))
        if n_test >= n:
            n_test = n - 1
        test_ids.extend(ids[:n_test])
        train_ids.extend(ids[n_test:])

    train = df[df["hadm_id"].isin(train_ids)].copy()
    test = df[df["hadm_id"].isin(test_ids)].copy()
    train = train.sample(frac=1, random_state=random_state).reset_index(drop=True)
    test = test.sample(frac=1, random_state=random_state).reset_index(drop=True)
    return train, test


def write_split(df: pd.DataFrame, path: Path) -> None:
    path.parent.mkdir(parents=True, exist_ok=True)
    out = df[["text", "label"]]
    out.to_csv(path, index=False, encoding="utf-8")


def _print_counts(name: str, df: pd.DataFrame) -> None:
    counts = df["label"].value_counts()
    parts = [f"{label}={int(counts.get(label, 0))}" for label in ("normal", "atenção", "urgente")]
    print(f"{name}: n={len(df)} ({', '.join(parts)})")


def parse_args(argv: list[str] | None = None) -> argparse.Namespace:
    parser = argparse.ArgumentParser(
        description="Build data/processed/train.csv and test.csv from MIMIC demo tables."
    )
    parser.add_argument("--raw-dir", type=Path, default=DEFAULT_RAW_DIR)
    parser.add_argument("--out-dir", type=Path, default=DEFAULT_OUT_DIR)
    parser.add_argument("--test-size", type=float, default=TEST_SIZE)
    parser.add_argument("--random-state", type=int, default=RANDOM_STATE)
    return parser.parse_args(argv)


def main(argv: list[str] | None = None) -> int:
    args = parse_args(argv)
    smr_path = args.raw_dir / "structured_medical_records.csv"
    if smr_path.exists():
        print(
            "Note: structured_medical_records.csv is ignored as training source "
            "(9 stays, all EMERGENCY, leaks Admission Type)."
        )

    dataset = build_dataset(args.raw_dir)
    assert_no_label_leakage(dataset["text"])
    train, test = split_by_hadm(
        dataset, test_size=args.test_size, random_state=args.random_state
    )
    overlap = set(train["hadm_id"]) & set(test["hadm_id"])
    if overlap:
        raise RuntimeError(f"hadm_id leaked across split: {sorted(overlap)[:5]}")

    train_path = args.out_dir / "train.csv"
    test_path = args.out_dir / "test.csv"
    write_split(train, train_path)
    write_split(test, test_path)

    _print_counts("full", dataset)
    _print_counts("train", train)
    _print_counts("test", test)
    print(f"Wrote {train_path}")
    print(f"Wrote {test_path}")
    print("Leakage check: passed")
    return 0


if __name__ == "__main__":
    sys.exit(main())
