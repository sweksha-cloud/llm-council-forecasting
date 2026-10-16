# Rebuild every result in this repo from the committed data. Run from the repo root.
# `make reproduce` is the one-line check: it rebuilds everything and fails if any
# committed result changes. See docs/reproduce.md.

PY ?= $(if $(wildcard .venv/bin/python),.venv/bin/python,python3)

.PHONY: setup test aye-prices import results dashboard reproduce clean

setup:            ## create .venv and install pinned dependencies
	python3 -m venv .venv
	.venv/bin/pip install -q -r requirements.txt

test:             ## scoring checked against hand-computed values; dashboard checked against the report
	$(PY) -m pytest -q

aye-prices:       ## look up Polymarket prices for Aye's questions (internet, ~10 min; result is committed)
	$(PY) -m importers.aye_market_prices

import:           ## re-import Aye's results from her pinned commit (needs internet the first time)
	$(PY) -m importers.import_aye

results:          ## all results tables (results/*/)
	$(PY) -m scoring.report --questions data/imported/aye-2026/questions.csv \
	    --forecasts data/imported/aye-2026/forecasts.csv --id-prefix aye-new: --out results/aye-2026-new
	$(PY) -m scoring.report --questions data/imported/aye-2026/questions.csv \
	    --forecasts data/imported/aye-2026/forecasts.csv --id-prefix aye-old: --out results/aye-2026-old

dashboard:        ## dashboard/index.html, built from the same data files
	$(PY) -m dashboard.build

reproduce: test import results dashboard   ## rebuild everything and confirm nothing committed changed
	git diff --exit-code -- data/imported results && echo "Reproduced: every committed result matches."

clean:
	rm -rf dashboard/index.html .pytest_cache
