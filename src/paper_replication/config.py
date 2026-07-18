"""Strict typed configuration for one replication run."""

from __future__ import annotations

import tomllib
from dataclasses import dataclass
from pathlib import Path
from typing import Any


@dataclass(frozen=True)
class PaperConfig:
    title: str
    url: str
    code_revision: str
    dataset_revision: str


@dataclass(frozen=True)
class ExperimentConfig:
    name: str
    hypothesis: str
    seed: int
    repetitions: int


@dataclass(frozen=True)
class ReplicationConfig:
    paper: PaperConfig
    experiment: ExperimentConfig


def _table(value: object, label: str) -> dict[str, Any]:
    if not isinstance(value, dict):
        raise ValueError(f"{label} must be a TOML table")
    return value


def _strict_keys(table: dict[str, Any], expected: set[str], label: str) -> None:
    unknown = set(table) - expected
    missing = expected - set(table)
    if unknown:
        raise ValueError(f"{label} contains unknown keys: {', '.join(sorted(unknown))}")
    if missing:
        raise ValueError(f"{label} is missing keys: {', '.join(sorted(missing))}")


def _text(table: dict[str, Any], key: str, label: str) -> str:
    value = table[key]
    if not isinstance(value, str) or not value.strip():
        raise ValueError(f"{label}.{key} must be a non-empty string")
    return value.strip()


def load_config(path: Path) -> ReplicationConfig:
    """Load a strict replication configuration from TOML."""
    document = tomllib.loads(path.read_text(encoding="utf-8"))
    _strict_keys(document, {"paper", "experiment"}, "config")
    paper = _table(document["paper"], "paper")
    experiment = _table(document["experiment"], "experiment")
    _strict_keys(paper, {"title", "url", "code_revision", "dataset_revision"}, "paper")
    _strict_keys(experiment, {"name", "hypothesis", "seed", "repetitions"}, "experiment")

    seed = experiment["seed"]
    repetitions = experiment["repetitions"]
    if not isinstance(seed, int) or isinstance(seed, bool):
        raise ValueError("experiment.seed must be an integer")
    if not isinstance(repetitions, int) or isinstance(repetitions, bool) or repetitions <= 0:
        raise ValueError("experiment.repetitions must be a positive integer")

    return ReplicationConfig(
        paper=PaperConfig(
            title=_text(paper, "title", "paper"),
            url=_text(paper, "url", "paper"),
            code_revision=_text(paper, "code_revision", "paper"),
            dataset_revision=_text(paper, "dataset_revision", "paper"),
        ),
        experiment=ExperimentConfig(
            name=_text(experiment, "name", "experiment"),
            hypothesis=_text(experiment, "hypothesis", "experiment"),
            seed=seed,
            repetitions=repetitions,
        ),
    )
