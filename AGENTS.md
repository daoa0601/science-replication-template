# Paper replication context

This repository must preserve the distinction between raw observations, derived results, and
claims. Never overwrite a prior run directory or upgrade historical evidence after the fact.

## Quick start

```bash
uv sync --all-extras
uv run paper-replication configs/baseline.toml --dry-run
make check
```

## Rules

- Pin upstream code, datasets, models, and environments to immutable revisions.
- Keep config typed and strict. Add Hydra only when real composition or sweep needs justify it.
- Change one hypothesis family at a time and retain raw repeated measurements.
- Generated data belongs under ignored `data/` or `outputs/`, or in documented external storage.
- Do not call the placeholder trial a result. Replace it and add correctness tests first.
- Do not claim replication from a single run; define tolerances and independent checks in advance.
- Keep `AGENTS.md` limited to non-obvious repository facts; user-facing procedure belongs in docs.
- Run `make check` before handoff.
