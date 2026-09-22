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


def load_rules(path: Path) -> tuple[EvidenceRule, ...]:
    payload = json.loads(path.read_text(encoding="utf-8"))
    return tuple(EvidenceRule(**item) for item in payload["variables"])


def discover_columns(
    source: str,
    columns: list[str],
    rules: tuple[EvidenceRule, ...],
) -> list[dict[str, Any]]:
    discovered: list[dict[str, Any]] = []
    for column in columns:
        matches = [
            rule
            for rule in rules
            if any(re.search(pattern, column, flags=re.IGNORECASE) for pattern in rule.patterns)
        ]
        if not matches:
            continue
        for rule in matches:
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
                    "match_count": sum(
                        bool(re.search(pattern, column, flags=re.IGNORECASE))
                        for pattern in rule.patterns
                    ),
                }
            )
    return discovered


def rules_as_records(rules: tuple[EvidenceRule, ...]) -> list[dict[str, Any]]:
    return [asdict(rule) for rule in rules]
