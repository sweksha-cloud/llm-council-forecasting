# Rebuild every result in this repo from the committed data. Run from the repo root.
# `make reproduce` is the one-line check: it rebuilds everything and fails if any
# committed result changes. See docs/reproduce.md.

PY ?= $(if $(wildcard .venv/bin/python),.venv/bin/python,python3)

.PHONY: setup test aye-prices import results dashboard site reproduce clean postrun

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
	$(PY) -m scoring.report --set live --out results/live
	$(PY) -m scoring.report --set live --exclude-in-play --out results/live-no-in-play   # sensitivity check
	$(PY) -m scoring.report --set settled --out results/settled
	$(PY) -m scoring.report --set settled-ext --out results/settled-ext
	$(PY) -m scoring.report --set settled settled-ext --out results/settled-all   # the pre-registered sample
	$(PY) -m analysis.robustness --set settled settled-ext --out results/settled-all
	$(PY) -m analysis.robustness --set settled --out results/settled
	$(PY) -m analysis.recalibration --set settled settled-ext --out results/settled-all
	$(PY) -m analysis.recalibration --set settled --out results/settled
	$(PY) -m analysis.variance --out results/variance
	$(PY) -m analysis.ablation --set settled settled-ext --out results/ablation
	$(PY) -m analysis.ablation --set settled --out results/ablation/settled
	$(PY) -m analysis.chair_weights --set live --out results/live
	$(PY) -m analysis.debate --set settled --out results/debate
	$(PY) -m analysis.ablation --set settled --forecasts data/forecasts.csv data/ablation/forecasts.csv data/scale/forecasts.csv --out results/scale   # 70B chair, once run
	$(PY) -m analysis.chair_weights --set settled settled-ext --forecasts data/forecasts.csv data/ablation/forecasts.csv --out results/ablation
	$(PY) -m scoring.report --set contamination --out results/contamination
	$(PY) -m scoring.report --set settled settled-ext contamination --out results/backtest   # includes the contamination split

dashboard:        ## dashboard/index.html, built from the same data files
	$(PY) -m dashboard.build

site:             ## site/index.html, the leaderboard page: same data and metric code as the dashboard
	$(PY) site/build.py

postrun:          ## check spark's forecasts, merge them, rebuild: make postrun SPARK=data/tmp/spark_forecasts.csv
	$(PY) -m forecast.postrun $(SPARK) --log logs/cmds_spark.log

reproduce: test import results dashboard site   ## rebuild everything and confirm nothing committed changed
	git diff --exit-code -- data/imported results && echo "Reproduced: every committed result matches."

clean:
	rm -rf dashboard/index.html site/index.html .pytest_cache
