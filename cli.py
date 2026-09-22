from __future__ import annotations

import argparse
import json

try:
    from .config import PipelineConfig
    from .pipeline import run
except ImportError:  # pragma: no cover - compatibility for direct module execution
    from config import PipelineConfig
    from pipeline import run


def main() -> None:
    parser = argparse.ArgumentParser(description="Build the regional AgeTech analytical dataset.")
    parser.add_argument("--config", required=True, help="Path to a JSON configuration file.")
    args = parser.parse_args()
    print(json.dumps(run(PipelineConfig.from_json(args.config)), indent=2, ensure_ascii=False))


if __name__ == "__main__":
    main()
