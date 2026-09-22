from __future__ import annotations

import json
import re
from dataclasses import asdict, dataclass
from pathlib import Path
from typing import Any


@dataclass(frozen=True)
class EvidenceRule:
    canonical: str
    domain: str
    patterns: tuple[str, ...]
    evidence_status: str
    unit: str | None
    comparable: bool
    time_window: str | None
    description: str


@dataclass(frozen=True)
class SourceMapping:
    source: str
    raw_column: str
    canonical: str
    domain: str
    evidence_status: str
    unit: str | None
    comparable: bool
    time_window: str | None
    description: str
    evidence_reference: str


def load_rules(path: Path) -> tuple[EvidenceRule, ...]:
    payload = json.loads(path.read_text(encoding="utf-8"))
    return tuple(EvidenceRule(**item) for item in payload["variables"])


def load_source_mappings(path: Path) -> tuple[SourceMapping, ...]:
    payload = json.loads(path.read_text(encoding="utf-8"))
    return tuple(SourceMapping(**item) for item in payload.get("source_mappings", []))


def discover_columns(
    source: str,
    columns: list[str],
    rules: tuple[EvidenceRule, ...],
    mappings: tuple[SourceMapping, ...] = (),
) -> list[dict[str, Any]]:
    discovered: list[dict[str, Any]] = []
    for column in columns:
        exact_matches = [
            mapping
            for mapping in mappings
            if mapping.source.casefold() == source.casefold()
            and mapping.raw_column.casefold() == column.casefold()
        ]
        for mapping in exact_matches:
            discovered.append(
                {
                    "source": source,
                    "raw_variable": column,
                    "variable_canonical": mapping.canonical,
                    "domain": mapping.domain,
                    "evidence_status": mapping.evidence_status,
                    "unit": mapping.unit,
                    "comparable": mapping.comparable,
                    "time_window": mapping.time_window,
                    "description": mapping.description,
                    "evidence_reference": mapping.evidence_reference,
                    "mapping_type": "exact_source_mapping",
                    "match_count": 1,
                }
            )
        matches = [
            rule
            for rule in rules
            if any(re.search(pattern, column, flags=re.IGNORECASE) for pattern in rule.patterns)
        ]
        for rule in matches:
            if exact_matches:
                continue
            discovered.append(
                {
                    "source": source,
                    "raw_variable": column,
                    "variable_canonical": rule.canonical,
                    "domain": rule.domain,
                    "evidence_status": rule.evidence_status,
                    "unit": rule.unit,
                    "comparable": rule.comparable,
                    "time_window": rule.time_window,
                    "description": rule.description,
                    "evidence_reference": "evidence_catalog.variables",
                    "mapping_type": "regex_rule",
                    "match_count": sum(
                        bool(re.search(pattern, column, flags=re.IGNORECASE))
                        for pattern in rule.patterns
                    ),
                }
            )
    return discovered


def rules_as_records(rules: tuple[EvidenceRule, ...]) -> list[dict[str, Any]]:
    return [asdict(rule) for rule in rules]
