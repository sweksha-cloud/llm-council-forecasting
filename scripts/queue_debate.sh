#!/usr/bin/env bash
# Debate, round 2 (docs/decisions.md, 2026-10-20): each member revises once after seeing the others'
# first answers. Queue AFTER scripts/queue_spark.sh, queue_variance.sh and queue_ablation.sh.
# Writes data/debate/forecasts.csv only; the main forecasts are read, never changed. Resumes on re-run.
# Start on spark with:   tmux new -s debate "bash scripts/queue_debate.sh"
# Estimate: 359 settled questions x 5 members, ~6-10 s per call = ~3-5 h.
cd ~/llm-council-forecasting
while tmux has-session -t queue 2>/dev/null || tmux has-session -t variance 2>/dev/null \
      || tmux has-session -t ablation 2>/dev/null; do sleep 60; done
echo "$(date -u +%FT%TZ) debate: --set settled --no-think" >> logs/cmds_spark.log
python3 -u -m forecast.debate --set settled --no-think 2>&1 | tee -a logs/debate_$(date +%Y%m%d).log
echo "$(date -u +%FT%TZ) debate finished" >> logs/cmds_spark.log
