#!/usr/bin/env bash
# Read-only status of the spark queue: progress per set and setup, failed calls, ETA, variance runs.
# Run on spark from anywhere:   bash ~/llm-council-forecasting/scripts/status_spark.sh
# Uses only the Python standard library; writes nothing.
cd "$(dirname "$0")/.." || exit 1
for s in queue variance; do
  if command -v tmux >/dev/null && tmux has-session -t "$s" 2>/dev/null; then echo "tmux session '$s': running"
  else echo "tmux session '$s': not running"; fi
done
python3 -m forecast.status
LOG=$(ls -t logs/queue_*.log logs/variance_*.log 2>/dev/null | head -1)
if [ -n "$LOG" ]; then echo; echo "Last line of $LOG:"; tail -n 1 "$LOG"; fi
