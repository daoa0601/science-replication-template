# Science replication starter

A small, runnable starting point for computational paper replications. Copy this directory into a
new Git repository, then rename the `paper_replication` package and replace the placeholder trial
before collecting real evidence.

The starter favors reproducibility over framework volume:

- `uv` with a checked-in lockfile and `src/` package layout;
- typed, strictly decoded TOML configuration;
- deterministic seeds and repeated raw trial records;
- one immutable output directory per run with source/config/environment provenance;
- Ruff, basedpyright, pytest, pre-commit, and a minimal CI workflow;
- explicit plans, result notes, data policy, and agent guidance.

## Copy and rename

```bash
cp -R templates/science-replication /path/to/my-paper-replication
cd /path/to/my-paper-replication
git init

# Rename both the distribution and import package before real work.
mv src/paper_replication src/my_replication
rg -l 'paper-replication|paper_replication|Paper Replication' \
  | xargs sed -i '' -e 's/paper-replication/my-replication/g' \
                  -e 's/paper_replication/my_replication/g' \
                  -e 's/Paper Replication/My Replication/g'
```

Review the mechanical rename before committing. On non-macOS systems, use the platform's equivalent
in-place `sed` syntax or edit the files directly.

## Exact smoke run

```bash
uv sync --all-extras
uv run paper-replication configs/baseline.toml --dry-run
make check
```

The non-dry command writes a new ignored run directory:

```bash
uv run paper-replication configs/baseline.toml
```

`src/paper_replication/experiment.py` currently emits a deterministic `placeholder_score`. Replace
`run_trial()` with the paper's real method and add correctness tests before interpreting any output.

## Before the first experiment

1. Replace every placeholder in `configs/baseline.toml`, `CITATION.cff`, and the research plan.
2. Pin paper code, model, dataset, and environment revisions—not just human-readable names.
3. Define the hypothesis, primary metric, baselines, tolerances, exclusions, and stopping rule.
4. Write a tiny correctness test that would fail for a plausible wrong implementation.
5. Commit the source and config; record any unavoidable dirty state in the result notes.
6. Keep raw inputs immutable and generated outputs ignored or in external artifact storage.

Add Hydra only when the project genuinely needs composed config groups or sweep overrides; the
typed TOML boundary is intentionally sufficient for a small first replication.

See [UPSTREAM.md](UPSTREAM.md) for the practices that informed this local starter.
