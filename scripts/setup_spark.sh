#!/usr/bin/env bash
# First-time setup on the GPU server. Safe to re-run.
# Usage (from the repo root):  bash scripts/setup_spark.sh [--pull]
#   --pull   also download any missing models with `ollama pull`
set -uo pipefail
cd "$(dirname "$0")/.."

MODELS=(llama3.1:8b mistral:latest qwen3:8b gemma2:9b phi3:medium deepseek-r1:8b)
PULL=0; [[ "${1:-}" == "--pull" ]] && PULL=1

step() { printf '\n== %s\n' "$1"; }

step "Home folder permissions"
if [[ "$(stat -c %a "$HOME" 2>/dev/null)" != "700" ]]; then
  chmod 700 "$HOME" && echo "set $HOME to 700 (only you can read it)"
else
  echo "ok: $HOME is private"
fi

step "Python environment"
PY=$(command -v python3.12 || command -v python3.11 || command -v python3)
echo "using $PY ($($PY --version))"
[[ -d .venv ]] || "$PY" -m venv .venv || { echo "could not create .venv (try: $PY -m pip install --user virtualenv)"; exit 1; }
.venv/bin/pip install -q --upgrade pip
.venv/bin/pip install -q -r requirements.txt && echo "dependencies installed"

step "Tests"
.venv/bin/python -m pytest -q || echo "!! tests failed, check before running forecasts"

step "Fake forecast run (no models)"
.venv/bin/python -m forecast.run_forecasts --backend fake --limit 2 --out /tmp/setup_fake_forecasts.csv \
  --models a b --chairmen a >/dev/null && echo "ok: pipeline works" && rm -f /tmp/setup_fake_forecasts.csv

step "Ollama"
if ! command -v ollama >/dev/null; then
  echo "!! ollama not found on PATH; ask Prof. Bill where it's installed"; exit 1
fi
if ! curl -s -m 5 http://localhost:11434/api/tags >/dev/null; then
  echo "!! Ollama server not answering on localhost:11434"; exit 1
fi
mkdir -p logs docs
missing=()
for m in "${MODELS[@]}"; do
  if ollama list | awk 'NR>1{print $1}' | grep -qx "$m"; then echo "ok: $m"; else echo "missing: $m"; missing+=("$m"); fi
done
if (( ${#missing[@]} )) && (( PULL )); then
  for m in "${missing[@]}"; do ollama pull "$m"; done
elif (( ${#missing[@]} )); then
  echo "re-run with --pull to download: ${missing[*]}"
fi

step "Recording exact model builds → docs/spark_models.txt"
{
  echo "# Recorded $(date -u +%Y-%m-%dT%H:%M:%SZ) on $(hostname)"
  ollama --version
  ollama list
  for m in "${MODELS[@]}"; do echo; echo "## $m"; ollama show "$m" 2>/dev/null | head -20; done
} > docs/spark_models.txt
echo "saved"

step "Smoke test: 1 real question, 2 models, 1 chairman"
.venv/bin/python -m forecast.run_forecasts --set live --limit 1 --no-think --no-prices \
  --out /tmp/setup_smoke_forecasts.csv --models llama3.1:8b qwen3:8b --chairmen llama3.1:8b \
  && echo "ok: real models answered (see probabilities above)" && rm -f /tmp/setup_smoke_forecasts.csv

step "Done"
echo "Next: start the live run in tmux (see docs/spark.md)."
