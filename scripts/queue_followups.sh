#!/usr/bin/env bash
# Everything after the main queue, in one session, most informative first (docs/decisions.md, 2026-10-20):
#   1. chair ablation, settled (359)       ~4 h   the "why", and self-preference with 5 chairs
#   2. debate round 2, settled (359)       ~3 h
#   3. chair ablation, settled-ext (680)   ~8 h   completes settled-all for the ablation
#   4. variance, 3 seeds at T=0.7 (200)    ~7 h
# Estimates at ~6 s per call. Replaces queue_variance.sh, queue_ablation.sh and queue_debate.sh run one
# after another (same commands, new order). Every step resumes where it stopped.
# Start on spark with:   tmux new -s followups "bash scripts/queue_followups.sh"
cd ~/llm-council-forecasting
while tmux has-session -t queue 2>/dev/null; do sleep 60; done   # wait for the main queue
log() { echo "$(date -u +%FT%TZ) followups: $*" >> logs/cmds_spark.log; }
M5="llama3.1:8b mistral:latest qwen3:8b gemma2:9b phi3:medium"
ablation() { log "rechair --set $1"; python3 -u -m forecast.rechair --set "$1" --no-think --variants numbers-only reasoning-only \
             --chairmen llama3.1:8b qwen3:8b --full-chairmen mistral:latest gemma2:9b phi3:medium 2>&1 | tee -a logs/ablation_$(date +%Y%m%d).log; }
ablation settled
log "debate --set settled"; python3 -u -m forecast.debate --set settled --no-think 2>&1 | tee -a logs/debate_$(date +%Y%m%d).log
ablation settled-ext
for SEED in 1 2 3; do
  log "variance seed $SEED"
  python3 -u -m forecast.run_forecasts --set settled --questions data/variance/questions_200.csv \
      --out data/variance/seed$SEED.csv --temperature 0.7 --seed $SEED --no-think \
      --models $M5 --chairmen llama3.1:8b qwen3:8b 2>&1 | tee -a logs/variance_$(date +%Y%m%d).log
done
log "finished"
