#!/usr/bin/env bash
# Runs after the live top-up finishes, one job at a time. Each step resumes where it stopped.
cd ~/llm-council-forecasting   # on spark; started with: tmux new -s queue "bash scripts/queue_spark.sh"
while tmux has-session -t topup 2>/dev/null; do sleep 60; done
M5="llama3.1:8b mistral:latest qwen3:8b gemma2:9b phi3:medium"
step() { echo "$(date -u +%FT%TZ) queue: $*" >> logs/cmds_spark.log; python3 -u -m forecast.run_forecasts "$@" 2>&1 | tee -a logs/queue_$(date +%Y%m%d).log; }
step --set settled --no-think --models $M5 --chairmen llama3.1:8b qwen3:8b
step --set contamination --no-think --models $M5 --chairmen llama3.1:8b qwen3:8b
step --set settled --think-budget 1024 --models deepseek-r1:8b --chairmen
step --set contamination --think-budget 1024 --models deepseek-r1:8b --chairmen
echo "$(date -u +%FT%TZ) queue finished" >> logs/cmds_spark.log
