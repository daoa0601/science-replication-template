"""Immutable local artifact manifest helpers."""

from __future__ import annotations

import hashlib
import json
import platform
import subprocess
import sys
from dataclasses import asdict
from datetime import UTC, datetime
from pathlib import Path
from typing import Any

from .config import ReplicationConfig
from .experiment import ExperimentResult


def _git(arguments: list[str], root: Path) -> str | None:
    try:
        completed = subprocess.run(
            ["git", *arguments],
            cwd=root,
            check=False,
            capture_output=True,
            text=True,
            timeout=5,
        )
    except (OSError, subprocess.TimeoutExpired):
        return None
    return completed.stdout.strip() if completed.returncode == 0 else None


def build_manifest(
    config: ReplicationConfig,
    result: ExperimentResult,
    config_path: Path,
    repository_root: Path,
) -> dict[str, Any]:
    """Build a self-describing manifest without changing repository state."""
    config_bytes = config_path.read_bytes()
    status = _git(["status", "--porcelain=v1"], repository_root)
    return {
        "schema_version": "1",
        "generated_at": datetime.now(UTC).isoformat(),
        "config": {
            "path": str(config_path.resolve()),
            "sha256": hashlib.sha256(config_bytes).hexdigest(),
            "value": asdict(config),
        },
        "source": {
            "commit": _git(["rev-parse", "HEAD"], repository_root),
            "dirty": None if status is None else bool(status),
        },
        "environment": {
            "python": sys.version.split()[0],
            "platform": platform.platform(),
        },
        "result": asdict(result),
        "warning": "placeholder_score is not research evidence; replace run_trial first",
    }


def write_manifest(output_root: Path, manifest: dict[str, Any]) -> Path:
    """Create one new run directory and atomically place its manifest."""
    timestamp = datetime.now(UTC).strftime("%Y%m%dT%H%M%S.%fZ")
    config_digest = str(manifest["config"]["sha256"])[:10]
    run_directory = output_root / f"{timestamp}-{config_digest}"
    run_directory.mkdir(parents=True, exist_ok=False)
    temporary = run_directory / "manifest.json.tmp"
    destination = run_directory / "manifest.json"
    temporary.write_text(f"{json.dumps(manifest, indent=2, sort_keys=True)}\n", encoding="utf-8")
    temporary.replace(destination)
    return destination
