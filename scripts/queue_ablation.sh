#!/usr/bin/env bash
# Chair ablations (docs/decisions.md, 2026-10-20): re-run only the chair over the members' answers
# already in data/forecasts.csv. Queue AFTER scripts/queue_spark.sh and scripts/queue_variance.sh.
# Writes data/ablation/forecasts.csv only; the main forecasts are read, never changed. Resumes on re-run.
# Start on spark with:   tmux new -s ablation "bash scripts/queue_ablation.sh"
#
# Estimate from the live run's pace (342 questions x 7 calls in 6 h 56 min, ~10 s per call):
# 7 chair calls per question (2 views x 2 chairs + 3 extra full-view chairs)
#   1. settled       359 questions   ~7 h
#   2. settled-ext   680 questions  ~14 h
cd ~/llm-council-forecasting
while tmux has-session -t queue 2>/dev/null || tmux has-session -t variance 2>/dev/null; do sleep 60; done
step() { echo "$(date -u +%FT%TZ) ablation: $*" >> logs/cmds_spark.log; python3 -u -m forecast.rechair "$@" 2>&1 | tee -a logs/ablation_$(date +%Y%m%d).log; }
for SET in settled settled-ext; do
  step --set $SET --no-think --variants numbers-only reasoning-only --chairmen llama3.1:8b qwen3:8b \
       --full-chairmen mistral:latest gemma2:9b phi3:medium
done
echo "$(date -u +%FT%TZ) ablation finished" >> logs/cmds_spark.log
