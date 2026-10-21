#!/usr/bin/env bash
# Scale check (docs/decisions.md, 2026-10-20): does the council result hold with a 10x larger model?
# Llama 3.3 70B (Ollama llama3.3:70b, ~43 GB) on the 359 settled questions:
#   1. as a single forecaster (same prompt as the 8B models)      ~3-4 h at ~35 s per answer
#   2. as the chair over the same 5 members' stored answers        ~4-6 h
# then the model is deleted, as agreed with the professor (only this model; never the shared ones).
# Writes data/scale/forecasts.csv only. Every step resumes where it stopped.
# Start on spark only with the professor's OK:   tmux new -s scale "bash scripts/queue_70b.sh"
cd ~/llm-council-forecasting
while tmux has-session -t queue 2>/dev/null || tmux has-session -t followups 2>/dev/null; do sleep 60; done
log() { echo "$(date -u +%FT%TZ) scale: $*" >> logs/cmds_spark.log; }
M=llama3.3:70b
log "ollama pull $M"; ollama pull $M && ollama list | grep "^$M" >> logs/cmds_spark.log
log "single $M on settled"
python3 -u -m forecast.run_forecasts --set settled --models $M --chairmen --out data/scale/forecasts.csv \
    2>&1 | tee -a logs/scale_$(date +%Y%m%d).log
log "chair $M on settled"
python3 -u -m forecast.rechair --set settled --variants --full-chairmen $M --out data/scale/forecasts.csv \
    2>&1 | tee -a logs/scale_$(date +%Y%m%d).log
log "ollama rm $M (only the model this script pulled)"; ollama rm $M
log "finished"
