#!/usr/bin/env bash
# Backtest queue on spark, one job at a time, in the order fixed in docs/decisions.md (2026-10-16).
# Every step resumes where it stopped, so the whole script can simply be re-run after an interruption.
# Start on spark with:   tmux new -s queue "bash scripts/queue_spark.sh"
#
# Estimates use the live run's pace (342 questions, 5 models + 2 chairs, in 6 h 56 min = 1.2 min/question)
# and DeepSeek's ~110 s/question with the thinking budget:
#   1. settled        360 questions   ~7 h
#   2. contamination  153 questions   ~3 h
#   3. settled-ext    ~640 questions  ~13 h   (no DeepSeek on the extension)
#   4. DeepSeek, settled        360   ~11 h
#   5. DeepSeek, contamination  153   ~5 h
cd ~/llm-council-forecasting
while tmux has-session -t topup 2>/dev/null; do sleep 60; done   # don't overlap a live top-up
M5="llama3.1:8b mistral:latest qwen3:8b gemma2:9b phi3:medium"
CHAIRS="llama3.1:8b qwen3:8b"
step() { echo "$(date -u +%FT%TZ) queue: $*" >> logs/cmds_spark.log; python3 -u -m forecast.run_forecasts "$@" 2>&1 | tee -a logs/queue_$(date +%Y%m%d).log; }
step --set settled       --no-think --models $M5 --chairmen $CHAIRS
step --set contamination --no-think --models $M5 --chairmen $CHAIRS
step --set settled-ext   --no-think --models $M5 --chairmen $CHAIRS
step --set settled       --think-budget 1024 --models deepseek-r1:8b --chairmen
step --set contamination --think-budget 1024 --models deepseek-r1:8b --chairmen
echo "$(date -u +%FT%TZ) queue finished" >> logs/cmds_spark.log
