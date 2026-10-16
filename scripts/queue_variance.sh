#!/usr/bin/env bash
# Variance runs: the same 5 models + 2 chairs on a fixed 200-question settled subset
# (data/variance/questions_200.csv), 3 seeds at temperature 0.7. Queue AFTER scripts/queue_spark.sh.
# Each seed writes its own file, so the main forecasts are untouched and each run resumes on its own.
# Start on spark with:   tmux new -s variance "bash scripts/queue_variance.sh"
# Estimate: 200 questions x 1.2 min = ~4 h per seed, ~12 h in total.
cd ~/llm-council-forecasting
while tmux has-session -t queue 2>/dev/null; do sleep 60; done   # wait for the main queue
M5="llama3.1:8b mistral:latest qwen3:8b gemma2:9b phi3:medium"
for SEED in 1 2 3; do
  echo "$(date -u +%FT%TZ) variance: seed $SEED" >> logs/cmds_spark.log
  python3 -u -m forecast.run_forecasts --set settled --questions data/variance/questions_200.csv \
      --out data/variance/seed$SEED.csv --temperature 0.7 --seed $SEED --no-think \
      --models $M5 --chairmen llama3.1:8b qwen3:8b 2>&1 | tee -a logs/variance_$(date +%Y%m%d).log
done
echo "$(date -u +%FT%TZ) variance finished" >> logs/cmds_spark.log
