from __future__ import annotations

import json
from pathlib import Path

import pytest

from paper_replication.artifacts import build_manifest, write_manifest
from paper_replication.cli import main
from paper_replication.config import load_config
from paper_replication.experiment import run_experiment


def config_file(tmp_path: Path, *, extra: str = "") -> Path:
    path = tmp_path / "experiment.toml"
    path.write_text(
        """
[paper]
title = "A paper"
url = "https://example.test/paper"
code_revision = "abc123"
dataset_revision = "sha256:example"

[experiment]
name = "baseline"
hypothesis = "The implementation matches the declared baseline"
seed = 7
repetitions = 3
"""
        + extra,
        encoding="utf-8",
    )
    return path


def test_repeated_results_are_deterministic_and_retained(tmp_path: Path) -> None:
    config = load_config(config_file(tmp_path))

    first = run_experiment(config)
    second = run_experiment(config)

    assert first == second
    assert first.metric == "placeholder_score"
    assert len(first.trials) == 3


def test_unknown_config_is_rejected(tmp_path: Path) -> None:
    with pytest.raises(ValueError, match="unknown keys"):
        load_config(config_file(tmp_path, extra="\nunexpected = true\n"))


def test_manifest_is_written_once_with_provenance(tmp_path: Path) -> None:
    config_path = config_file(tmp_path)
    config = load_config(config_path)
    result = run_experiment(config)
    manifest = build_manifest(config, result, config_path, tmp_path)

    destination = write_manifest(tmp_path / "outputs", manifest)
    stored = json.loads(destination.read_text(encoding="utf-8"))

    assert stored["config"]["sha256"]
    assert stored["environment"]["python"]
    assert stored["result"]["metric"] == "placeholder_score"


def test_dry_run_writes_nothing(tmp_path: Path, capsys: pytest.CaptureFixture[str]) -> None:
    output_root = tmp_path / "outputs"

    assert main([str(config_file(tmp_path)), "--output-root", str(output_root), "--dry-run"]) == 0
    assert not output_root.exists()
    assert "placeholder_score" in capsys.readouterr().out


def test_cli_writes_one_manifest_for_a_real_run(
    tmp_path: Path,
    capsys: pytest.CaptureFixture[str],
    monkeypatch: pytest.MonkeyPatch,
) -> None:
    config_path = config_file(tmp_path)
    output_root = tmp_path / "outputs"
    monkeypatch.chdir(tmp_path)

    assert main([str(config_path), "--output-root", str(output_root)]) == 0

    manifests = list(output_root.glob("*/manifest.json"))
    assert len(manifests) == 1
    assert str(manifests[0]) in capsys.readouterr().out


@pytest.mark.parametrize(
    ("old", "new", "message"),
    [
        ('dataset_revision = "sha256:example"', "", "paper is missing keys"),
        ('title = "A paper"', 'title = "   "', "paper.title must be a non-empty string"),
        ("seed = 7", 'seed = "seven"', "experiment.seed must be an integer"),
        ("repetitions = 3", "repetitions = 0", "must be a positive integer"),
    ],
)
def test_invalid_config_values_fail_closed(
    tmp_path: Path,
    old: str,
    new: str,
    message: str,
) -> None:
    path = config_file(tmp_path)
    path.write_text(path.read_text(encoding="utf-8").replace(old, new), encoding="utf-8")

    with pytest.raises(ValueError, match=message):
        load_config(path)
