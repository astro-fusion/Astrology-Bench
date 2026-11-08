PY ?= python
SEED ?= 20261108

.PHONY: install lint test generate baselines leaderboard all

install:
	$(PY) -m pip install -e ".[dev]"

lint:
	$(PY) -m ruff check .
	$(PY) -m mypy

test:
	$(PY) -m pytest -q

generate:
	$(PY) -m astro_bench.cli generate --split dev --seed $(SEED)
	$(PY) -m astro_bench.cli validate items/

baselines:
	for s in oracle random constant mock; do $(PY) -m astro_bench.cli run --solver $$s --items items/ --out results/; done

leaderboard:
	$(PY) -m astro_bench.cli leaderboard --results results/ --out LEADERBOARD.md

all: lint test generate baselines leaderboard
