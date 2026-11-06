#!/usr/bin/env bash
# Round-2 checks, pre-registered in docs/decisions.md (2026-11-06). Run on spark inside tmux:
#   tmux new -s round2 "bash scripts/queue_round2.sh"
# In order, each resuming if interrupted (rows already written are skipped):
#   1. prompt check: the "anchored" chair (different wording, shuffled members, average shown),
#      both main chairs, on settled + settled-ext (data/ablation/forecasts.csv)
#   2. debate round 2 on settled-ext (data/debate/forecasts.csv)
#   3. the 70B scale check on settled-ext, alone and as chair (data/scale/forecasts.csv); the model
#      is removed afterwards only if this script pulled it
# CPU only while spark's GPU driver is down: FORECAST_NUM_THREAD caps the cores used (10 of 20).
set -uo pipefail
cd ~/llm-council-forecasting
log() { echo "$(date -u +%FT%TZ) round2: $*" >> logs/cmds_spark.log; }
export FORECAST_NUM_THREAD=${FORECAST_NUM_THREAD:-10}
T=3600
L=logs/round2_$(date +%Y%m%d).log
log "start FORECAST_NUM_THREAD=$FORECAST_NUM_THREAD timeout=${T}s"

log "1/3 anchored chair (llama3.1:8b, qwen3:8b) on settled settled-ext"
python3 -u -m forecast.rechair --set settled settled-ext --variants anchored --chairmen llama3.1:8b qwen3:8b \
    --no-think --timeout $T 2>&1 | tee -a $L

log "2/3 debate round 2 on settled-ext"
python3 -u -m forecast.debate --set settled-ext --no-think --timeout $T 2>&1 | tee -a $L

M=llama3.3:70b
if ollama list | grep -q "^$M"; then PULLED=0; log "$M already on spark (not ours): will not remove it"
else PULLED=1; log "ollama pull $M"; ollama pull $M || { log "pull failed"; exit 1; }; fi
log "3/3 $M alone on settled-ext"
python3 -u -m forecast.run_forecasts --set settled-ext --models $M --chairmen --out data/scale/forecasts.csv --timeout $T \
    2>&1 | tee -a $L
log "3/3 $M as chair on settled-ext"
python3 -u -m forecast.rechair --set settled-ext --variants --full-chairmen $M --out data/scale/forecasts.csv --timeout $T \
    2>&1 | tee -a $L
if [ "$PULLED" = 1 ]; then log "ollama rm $M (only the model this script pulled)"; ollama stop $M; ollama rm $M; fi
log "finished"
