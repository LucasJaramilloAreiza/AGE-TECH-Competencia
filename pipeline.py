from __future__ import annotations

import hashlib
import json
import re
from datetime import datetime, timezone
from pathlib import Path
from typing import Any

import pandas as pd

from .catalog import discover_columns, load_rules, rules_as_records
from .config import PipelineConfig, SourceConfig

DIRECT_ID_PATTERNS = (
    r"(^|_)(name|nombre|address|direccion|phone|telefono|email|ssn|cedula|"
    r"identificador|id_number|curp|clave)(_|$)",
)
LEAKAGE_PATTERNS = (r"outcome", r"target", r"label", r"future", r"post", r"after")
MISSING_CODES = {-99, -98, -97, -96, 97, 98, 99}


def run(config: PipelineConfig) -> dict[str, Any]:
    _validate_inputs(config)
    rules = load_rules(config.evidence_catalog)
    config.output_dir.mkdir(parents=True, exist_ok=True)
    source_records: list[dict[str, Any]] = []
    source_frames: list[pd.DataFrame] = []
    quality: list[dict[str, Any]] = []

    for source in config.sources:
        frame, records = _build_source(source, rules, config.output_dir)
        source_frames.append(frame)
        source_records.extend(records)
        quality.extend(_quality_records(frame, source.name))

    all_frame = pd.concat(source_frames, ignore_index=True, sort=False)
    harmonized = _build_harmonized(all_frame, rules)
    _write_table(all_frame, config.output_dir / "all_sources.parquet")
    _write_table(harmonized, config.output_dir / "harmonized" / "regional.parquet")
    _write_csv(source_records, config.output_dir / "catalog" / "variable_catalog.csv")
    _write_csv(rules_as_records(rules), config.output_dir / "catalog" / "evidence_rules.csv")
    _write_csv(quality, config.output_dir / "quality" / "coverage.csv")
    exclusions = _exclusions(all_frame.columns)
    _write_csv(exclusions, config.output_dir / "quality" / "exclusions.csv")
    leakage = _staging_leakage_check(config)
    leakage["harmonized_check"] = _leakage_check(harmonized)
    leakage["passed"] = leakage["passed"] and leakage["harmonized_check"]["passed"]
    _write_json(leakage, config.output_dir / "quality" / "leakage_check.json")
    partitions = _make_partitions(harmonized, config.seed, config.test_size)
    _write_table(partitions, config.output_dir / "partitions.parquet")
    report = {
        "created_at_utc": datetime.now(timezone.utc).isoformat(),
        "rows_source_preserving": int(len(all_frame)),
        "rows_harmonized": int(len(harmonized)),
        "variables_discovered": int(len(source_records)),
        "sources": [
            {"name": source.name, "country": source.country, "wave": source.wave}
            for source in config.sources
        ],
        "leakage_check": leakage,
        "quality_records": len(quality),
        "policy": {
            "original_staging_modified": False,
            "direct_identifiers_modeled": False,
            "cross_source_linkage": False,
            "falls_windows_collapsed": False,
        },
    }
    _write_json(report, config.output_dir / "quality" / "report.json")
    _write_json(
        {
            "config_sha256": _sha256(Path(config.evidence_catalog)),
            "inputs": [_manifest_summary(source) for source in config.sources],
            "created_at_utc": report["created_at_utc"],
        },
        config.output_dir / "run_manifest.json",
    )
    return report


def _build_source(
    source: SourceConfig,
    rules: tuple,
    output_dir: Path,
) -> tuple[pd.DataFrame, list[dict[str, Any]]]:
    files = sorted(source.staging_dir.glob("*.parquet"))
    if not files:
        raise FileNotFoundError(f"No parquet files found in {source.staging_dir}")
    frames: list[pd.DataFrame] = []
    records: list[dict[str, Any]] = []
    for path in files:
        frame = pd.read_parquet(path)
        matches = discover_columns(source.name, [str(c) for c in frame.columns], rules)
        records.extend(
            {
                **match,
                "raw_file": path.name,
                "traceability_id": _trace_id(source.name, path.name, match["raw_variable"]),
            }
            for match in matches
        )
        selected = [
            item["raw_variable"]
            for item in matches
            if not _is_direct_identifier(item["raw_variable"])
        ]
        selected = list(dict.fromkeys(selected))
        if not selected:
            continue
        out = frame[selected].copy()
        out.insert(0, "row_source_file", path.name)
        out.insert(0, "source", source.name)
        out.insert(0, "country", source.country)
        out.insert(0, "wave", source.wave)
        out["source_row_number"] = range(len(out))
        out = _clean_values(out, selected)
        frames.append(out)
    if not frames:
        raise ValueError(f"No evidence-backed columns discovered for {source.name}")
    result = pd.concat(frames, ignore_index=True, sort=False)
    target = output_dir / "source" / f"{source.name}_{source.wave}" / "dataset.parquet"
    _write_table(result, target)
    return result, records


def _clean_values(frame: pd.DataFrame, raw_columns: list[str]) -> pd.DataFrame:
    for column in raw_columns:
        if column not in frame:
            continue
        numeric = pd.to_numeric(frame[column], errors="coerce")
        frame[column] = frame[column].mask(numeric.isin(MISSING_CODES))
    return frame


def _build_harmonized(frame: pd.DataFrame, rules: tuple) -> pd.DataFrame:
    records = []
    rule_by_name = {rule.canonical: rule for rule in rules}
    for _, row in frame.iterrows():
        metadata = {
            key: row.get(key)
            for key in ("source", "country", "wave", "row_source_file", "source_row_number")
        }
        for column, value in row.items():
            if column in metadata or column.startswith("source_") or pd.isna(value):
                continue
            matches = [rule for rule in rules if any(
                re.search(pattern, column, flags=re.IGNORECASE) for pattern in rule.patterns
            )]
            for rule in matches:
                records.append(
                    {
                        **metadata,
                        "variable_canonical": rule.canonical,
                        "value": value,
                        "unit": rule.unit,
                        "time_window": rule.time_window,
                        "comparable": rule.comparable,
                        "evidence_status": rule.evidence_status,
                        "raw_variable": column,
                        "quality_flag": "observed",
                        "traceability_id": _trace_id(
                            str(row.get("source")), str(row.get("row_source_file")), column
                        ),
                    }
                )
    result = pd.DataFrame.from_records(records)
    if not result.empty and "value" in result.columns:
        result["value"] = result["value"].map(lambda v: None if pd.isna(v) else str(v))
    return result


def _quality_records(frame: pd.DataFrame, source: str) -> list[dict[str, Any]]:
    result = []
    for column in frame.columns:
        if column in {"source", "country", "wave", "row_source_file", "source_row_number"}:
            continue
        values = frame[column]
        result.append(
            {
                "source": source,
                "raw_variable": column,
                "rows": int(len(values)),
                "non_missing": int(values.notna().sum()),
                "coverage_pct": round(float(values.notna().mean() * 100), 4),
                "distinct_non_missing": int(values.nunique(dropna=True)),
                "invalid_missing_codes": int(
                    pd.to_numeric(values, errors="coerce").isin(MISSING_CODES).sum()
                ),
            }
        )
    return result


def _exclusions(columns: Any) -> list[dict[str, str]]:
    return [
        {"column": str(column), "reason": "direct_identifier_or_leakage", "pattern": pattern}
        for column in columns
        for pattern in (*DIRECT_ID_PATTERNS, *LEAKAGE_PATTERNS)
        if re.search(pattern, str(column), flags=re.IGNORECASE)
    ]


def _is_direct_identifier(column: str) -> bool:
    return any(re.search(pattern, str(column), flags=re.IGNORECASE) for pattern in DIRECT_ID_PATTERNS)


def _leakage_check(frame: pd.DataFrame) -> dict[str, Any]:
    columns = [str(column) for column in frame.columns]
    offenders = [
        column
        for column in columns
        if any(re.search(pattern, column, flags=re.IGNORECASE) for pattern in LEAKAGE_PATTERNS)
    ]
    if "raw_variable" in frame:
        raw_offenders = [
            str(value)
            for value in frame["raw_variable"].dropna().unique()
            if any(re.search(pattern, str(value), flags=re.IGNORECASE) for pattern in LEAKAGE_PATTERNS)
        ]
        offenders.extend(raw_offenders)
    return {
        "passed": not offenders,
        "offending_columns": sorted(set(offenders)),
        "checked_columns": columns,
    }


def _staging_leakage_check(config: PipelineConfig) -> dict[str, Any]:
    checked: list[str] = []
    offenders: list[str] = []
    for source in config.sources:
        for path in sorted(source.staging_dir.glob("*.parquet")):
            columns = [str(column) for column in pd.read_parquet(path, engine="pyarrow").columns]
            checked.extend(f"{source.name}:{column}" for column in columns)
            offenders.extend(
                f"{source.name}:{column}"
                for column in columns
                if any(re.search(pattern, column, flags=re.IGNORECASE) for pattern in LEAKAGE_PATTERNS)
            )
    return {"passed": not offenders, "offending_columns": sorted(set(offenders)), "checked_columns": checked}


def _make_partitions(frame: pd.DataFrame, seed: int, test_size: float) -> pd.DataFrame:
    if frame.empty:
        return frame.assign(split=pd.Series(dtype="string"))
    keys = frame[["source", "country", "wave", "row_source_file", "source_row_number"]].astype(str)
    hashed = pd.util.hash_pandas_object(keys, index=False).astype("uint64")
    # A stable arithmetic offset makes the configured seed effective without
    # relying on Python's process-randomized hash implementation.
    threshold = int(test_size * 10_000)
    split = ((hashed + seed) % 10_000 < threshold).map({True: "test", False: "train"})
    result = frame.copy()
    result["split"] = split.to_numpy()
    return result


def _validate_inputs(config: PipelineConfig) -> None:
    if not config.evidence_catalog.exists():
        raise FileNotFoundError(f"Evidence catalog not found: {config.evidence_catalog}")
    for source in config.sources:
        if not source.staging_dir.is_dir():
            raise FileNotFoundError(f"Staging directory not found: {source.staging_dir}")
        if not source.manifest.exists():
            raise FileNotFoundError(f"Manifest not found: {source.manifest}")


def _manifest_summary(source: SourceConfig) -> dict[str, Any]:
    payload = json.loads(source.manifest.read_text(encoding="utf-8"))
    return {"name": source.name, "manifest": str(source.manifest), "entries": len(payload)}


def _trace_id(*parts: str) -> str:
    return hashlib.sha256("|".join(parts).encode("utf-8")).hexdigest()[:20]


def _sha256(path: Path) -> str:
    return hashlib.sha256(path.read_bytes()).hexdigest()


def _write_table(frame: pd.DataFrame, path: Path) -> None:
    path.parent.mkdir(parents=True, exist_ok=True)
    frame.to_parquet(path, index=False)


def _write_csv(records: list[dict[str, Any]], path: Path) -> None:
    path.parent.mkdir(parents=True, exist_ok=True)
    pd.DataFrame.from_records(records).to_csv(path, index=False)


def _write_json(payload: Any, path: Path) -> None:
    path.parent.mkdir(parents=True, exist_ok=True)
    path.write_text(json.dumps(payload, ensure_ascii=False, indent=2, default=str), encoding="utf-8")
