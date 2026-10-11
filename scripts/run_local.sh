#!/usr/bin/env bash
# Run the live set on a laptop with little disk space (e.g. a 16 GB Mac).
# Models are run one at a time: download, answer every question, delete.
# The council step runs last and reuses the saved member answers.
# Safe to re-run: finished (question, setup) rows are skipped.
#
# Usage (from the repo root, with Ollama running):
#   caffeinate -i bash scripts/run_local.sh            # full live run, locked
#   caffeinate -i bash scripts/run_local.sh --limit 3  # quick test
set -uo pipefail
cd "$(dirname "$0")/.."

MODELS=(llama3.1:8b mistral:latest qwen3:8b gemma2:9b deepseek-r1:8b phi3:medium)
CHAIRMEN=(llama3.1:8b qwen3:8b)
PY=python3; [[ -x .venv/bin/python ]] && PY=.venv/bin/python
mkdir -p logs
LOG="logs/run_local_$(date +%Y%m%d_%H%M).log"
EXTRA=("$@")

run() { "$PY" -m forecast.run_forecasts --set live --lock --no-think "$@" ${EXTRA[@]+"${EXTRA[@]}"} 2>&1 | tee -a "$LOG"; }
DONE=()  # models that ran; only these count as council members

echo "Started $(date -u +%FT%TZ)  args: ${EXTRA[*]:-}" | tee -a "$LOG"
ollama --version | tee -a "$LOG"

# 1. Single models, one at a time
for m in "${MODELS[@]}"; do
  echo "== $m" | tee -a "$LOG"
  ollama pull "$m" >/dev/null || { echo "pull failed: $m" | tee -a "$LOG"; continue; }
  ollama list | grep "^$m " | tee -a "$LOG"   # record the exact build (digest)
  run --models "$m" --chairmen
  DONE+=("$m")
  ollama rm "$m" >/dev/null   # free the disk for the next model
done

# 2. Councils, from the saved answers
for c in "${CHAIRMEN[@]}"; do
  echo "== council, chair $c" | tee -a "$LOG"
  ollama pull "$c" >/dev/null || { echo "pull failed: $c" | tee -a "$LOG"; continue; }
  run --models ${DONE[@]+"${DONE[@]}"} --chairmen "$c"
  ollama rm "$c" >/dev/null
done

echo "Finished $(date -u +%FT%TZ)" | tee -a "$LOG"
