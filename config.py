from __future__ import annotations

import json
from dataclasses import dataclass
from pathlib import Path
from typing import Any


@dataclass(frozen=True)
class SourceConfig:
    name: str
    country: str
    wave: int
    staging_dir: Path
    manifest: Path
    time_windows: dict[str, str]


@dataclass(frozen=True)
class PipelineConfig:
    sources: tuple[SourceConfig, ...]
    output_dir: Path
    evidence_catalog: Path
    seed: int = 20260921
    test_size: float = 0.2

    @classmethod
    def from_json(cls, path: str | Path) -> "PipelineConfig":
        raw = json.loads(Path(path).read_text(encoding="utf-8"))
        base = Path(path).resolve().parent
        sources = tuple(
            SourceConfig(
                name=item["name"],
                country=item["country"],
                wave=int(item["wave"]),
                staging_dir=_resolve(base, item["staging_dir"]),
                manifest=_resolve(base, item["manifest"]),
                time_windows=item.get("time_windows", {}),
            )
            for item in raw["sources"]
        )
        return cls(
            sources=sources,
            output_dir=_resolve(base, raw["output_dir"]),
            evidence_catalog=_resolve(base, raw["evidence_catalog"]),
            seed=int(raw.get("seed", 20260921)),
            test_size=float(raw.get("test_size", 0.2)),
        )


def _resolve(base: Path, value: str) -> Path:
    candidate = Path(value)
    return candidate if candidate.is_absolute() else (base / candidate).resolve()
