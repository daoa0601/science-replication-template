"""Deterministic placeholder experiment to replace with the replicated method."""

from __future__ import annotations

import hashlib
import statistics
from dataclasses import dataclass

from .config import ReplicationConfig


@dataclass(frozen=True)
class TrialResult:
    repetition: int
    seed: int
    placeholder_score: float


@dataclass(frozen=True)
class ExperimentResult:
    metric: str
    mean: float
    trials: tuple[TrialResult, ...]


def run_trial(seed: int, repetition: int) -> TrialResult:
    """Return deterministic placeholder data; replace before doing research."""
    digest = hashlib.sha256(f"{seed}:{repetition}".encode()).digest()
    score = int.from_bytes(digest[:8], "big") / 2**64
    return TrialResult(repetition=repetition, seed=seed, placeholder_score=score)


def run_experiment(config: ReplicationConfig) -> ExperimentResult:
    """Run every declared repetition without dropping raw trial values."""
    trials = tuple(
        run_trial(config.experiment.seed, repetition)
        for repetition in range(config.experiment.repetitions)
    )
    return ExperimentResult(
        metric="placeholder_score",
        mean=statistics.fmean(trial.placeholder_score for trial in trials),
        trials=trials,
    )
