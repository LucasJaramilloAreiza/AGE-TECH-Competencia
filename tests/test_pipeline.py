from pathlib import Path

import pandas as pd
import pytest

from AgeTechRegional.catalog import EvidenceRule, SourceMapping, discover_columns
from AgeTechRegional.config import PipelineConfig, SourceConfig
from AgeTechRegional.pipeline import (
    _build_harmonized,
    _leakage_check,
    _make_partitions,
    _read_source_file,
    _write_table,
    _validate_inputs,
)


def test_discovery_requires_evidence_pattern():
    rules = (
        EvidenceRule("falls_12m", "falls", (r"fall_12m",), "direct", None, False, "last_12_months", "x"),
    )
    records = discover_columns("sabe", ["fall_12m", "unrelated"], rules)
    assert [record["raw_variable"] for record in records] == ["fall_12m"]


def test_exact_source_mapping_has_provenance_and_wins_over_regex():
    rules = (
        EvidenceRule("comorbidity", "comorbidities", (r"c4_24",), "direct", None, False, "history", "broad"),
    )
    mappings = (
        SourceMapping(
            "mhas", "c4_24", "hypertension", "comorbidities", "official_label",
            None, False, "interview_or_history", "hypertension", "MHAS label c4_24",
        ),
    )

    records = discover_columns("mhas", ["c4_24"], rules, mappings)

    assert len(records) == 1
    assert records[0]["variable_canonical"] == "hypertension"
    assert records[0]["mapping_type"] == "exact_source_mapping"
    assert records[0]["evidence_reference"] == "MHAS label c4_24"


def test_source_mapping_preserves_falls_windows():
    mappings = (
        SourceMapping(
            "mhas", "c37_24", "falls_24m", "falls", "official_label",
            "binary_or_count", False, "last_24_months", "two-year falls", "MHAS c37_24",
        ),
        SourceMapping(
            "sabe", "CAIDAS_ULTIMO_ANO", "falls_12m", "falls", "documented_code",
            "binary_or_count", False, "last_12_months", "one-year falls", "SABE documented code",
        ),
    )

    mhas = discover_columns("mhas", ["c37_24"], (), mappings)
    sabe = discover_columns("sabe", ["CAIDAS_ULTIMO_ANO"], (), mappings)

    assert mhas[0]["variable_canonical"] == "falls_24m"
    assert mhas[0]["time_window"] == "last_24_months"
    assert sabe[0]["variable_canonical"] == "falls_12m"
    assert sabe[0]["time_window"] == "last_12_months"


def test_harmonized_output_keeps_mapping_metadata():
    frame = pd.DataFrame(
        {"source": ["mhas"], "country": ["MX"], "wave": [2024],
         "row_source_file": ["synthetic.dta"], "source_row_number": [0],
         "c37_24": [1]}
    )
    mapping = SourceMapping(
        "mhas", "c37_24", "falls_24m", "falls", "official_label",
        "binary_or_count", False, "last_24_months", "two-year falls", "MHAS c37_24",
    )

    result = _build_harmonized(frame, (), (mapping,))

    assert result.loc[0, "variable_canonical"] == "falls_24m"
    assert result.loc[0, "evidence_reference"] == "MHAS c37_24"
    assert result.loc[0, "mapping_type"] == "exact_source_mapping"


def test_write_table_normalizes_mixed_stata_category(tmp_path: Path):
    frame = pd.DataFrame(
        {
            "c38_24": pd.Series([1, "88.RF", None], dtype="category"),
            "age_24": [70, 71, 72],
        }
    )

    _write_table(frame, tmp_path / "mixed.parquet")
    result = pd.read_parquet(tmp_path / "mixed.parquet")

    assert result["c38_24"].iloc[:2].tolist() == ["1", "88.RF"]
    assert pd.isna(result["c38_24"].iloc[2])
    assert result["age_24"].tolist() == [70, 71, 72]


def test_fall_windows_are_not_collapsed():
    assert "falls_12m" != "falls_24m"


def test_leakage_check_flags_future_columns():
    frame = pd.DataFrame({"variable_canonical": ["falls_12m"], "raw_variable": ["future_target"]})
    result = _leakage_check(frame)
    assert not result["passed"]


def test_partitions_are_deterministic():
    frame = pd.DataFrame(
        {
            "source": ["sabe"] * 4,
            "country": ["CO"] * 4,
            "wave": [2015] * 4,
            "row_source_file": ["a.parquet"] * 4,
            "source_row_number": range(4),
            "variable_canonical": ["age_years"] * 4,
            "value": [70, 71, 72, 73],
        }
    )
    first = _make_partitions(frame, 7, 0.5)["split"].tolist()
    second = _make_partitions(frame, 7, 0.5)["split"].tolist()
    assert first == second


def test_validation_generates_missing_manifests(tmp_path: Path):
    staging = tmp_path / "staging" / "sabe"
    staging.mkdir(parents=True)
    input_path = staging / "input.parquet"
    pd.DataFrame({"age": [70]}).to_parquet(input_path, index=False)
    manifest = tmp_path / "results" / "manifest_sabe.json"
    config = PipelineConfig(
        sources=(SourceConfig("sabe", "CO", 2015, staging, manifest, {}),),
        output_dir=tmp_path / "outputs",
        evidence_catalog=tmp_path / "evidence_catalog.json",
    )
    config.evidence_catalog.write_text('{"variables": []}', encoding="utf-8")

    _validate_inputs(config)

    assert manifest.exists()
    assert '"input.parquet"' in manifest.read_text(encoding="utf-8")


def test_validation_reports_empty_staging(tmp_path: Path):
    staging = tmp_path / "staging" / "mhas"
    staging.mkdir(parents=True)
    config = PipelineConfig(
        sources=(
            SourceConfig("mhas", "MX", 2024, staging, tmp_path / "manifest.json", {}),
        ),
        output_dir=tmp_path / "outputs",
        evidence_catalog=tmp_path / "evidence_catalog.json",
    )
    config.evidence_catalog.write_text('{"variables": []}', encoding="utf-8")

    with pytest.raises(ValueError, match="staging/mhas/"):
        _validate_inputs(config)


def test_pipe_delimited_text_is_supported(tmp_path: Path):
    source_file = tmp_path / "Cap1Ident.txt"
    source_file.write_text("age|fall_12m\n70|1\n", encoding="utf-8")

    frame = _read_source_file(source_file)

    assert frame.to_dict(orient="records") == [{"age": 70, "fall_12m": 1}]


def test_cp1252_pipe_delimited_text_is_supported(tmp_path: Path):
    source_file = tmp_path / "Cap1Ident.txt"
    source_file.write_bytes("nombre|region\nMuñoz|Bogotá\n".encode("cp1252"))

    frame = _read_source_file(source_file)

    assert frame.to_dict(orient="records") == [
        {"nombre": "Muñoz", "region": "Bogotá"}
    ]
