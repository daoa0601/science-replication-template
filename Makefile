.PHONY: sync format lint typecheck test build check smoke

sync:
	uv sync --all-extras

format:
	uv run ruff check --fix .
	uv run ruff format .

lint:
	uv run ruff format --check .
	uv run ruff check .

typecheck:
	uv run basedpyright

test:
	uv run pytest --cov=paper_replication --cov-report=term-missing

build:
	uv build

smoke:
	uv run paper-replication configs/baseline.toml --dry-run

check: lint typecheck test build smoke
