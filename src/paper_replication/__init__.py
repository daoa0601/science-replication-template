"""Reproducible paper replication starter."""

from .config import ReplicationConfig, load_config
from .experiment import ExperimentResult, TrialResult, run_experiment

__all__ = [
    "ExperimentResult",
    "ReplicationConfig",
    "TrialResult",
    "load_config",
    "run_experiment",
]

__version__ = "0.1.0"
