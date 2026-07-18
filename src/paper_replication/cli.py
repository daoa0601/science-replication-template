"""Command-line entry point for the replication starter."""

from __future__ import annotations

import argparse
import json
from collections.abc import Sequence
from dataclasses import asdict
from pathlib import Path

from .artifacts import build_manifest, write_manifest
from .config import load_config
from .experiment import run_experiment


def parser() -> argparse.ArgumentParser:
    command = argparse.ArgumentParser(description=__doc__)
    command.add_argument("config", type=Path, help="Strict TOML experiment configuration")
    command.add_argument("--output-root", type=Path, default=Path("outputs"))
    command.add_argument(
        "--dry-run", action="store_true", help="Validate and print without writing"
    )
    return command


def main(argv: Sequence[str] | None = None) -> int:
    arguments = parser().parse_args(argv)
    config = load_config(arguments.config)
    result = run_experiment(config)
    if arguments.dry_run:
        print(json.dumps({"config": asdict(config), "result": asdict(result)}, indent=2))
        return 0

    repository_root = Path.cwd()
    manifest = build_manifest(config, result, arguments.config, repository_root)
    destination = write_manifest(arguments.output_root, manifest)
    print(destination)
    return 0


if __name__ == "__main__":
    raise SystemExit(main())
