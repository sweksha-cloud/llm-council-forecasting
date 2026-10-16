#!/usr/bin/env bash
# Bring live outcomes back from spark, rescore the live set, rebuild the dashboard, commit on a branch.
#
#   SPARK_USER=<username> bash scripts/sync_live.sh --dry-run     # show what would change; writes nothing
#   SPARK_USER=<username> bash scripts/sync_live.sh               # merge, rescore, commit on data/live-outcomes-<date>
#   bash scripts/sync_live.sh --from path/to/questions.csv        # use a file instead of copying from spark
#
# Only `outcome` and `resolved_at` of live questions are taken from spark, and only where the laptop's are
# empty (collect/merge_outcomes.py). Run from the repo root on a clean working tree. Doesn't push.
set -euo pipefail
DRY=0; FROM=""
while [ $# -gt 0 ]; do
  case "$1" in
    --dry-run) DRY=1 ;;
    --from) FROM="$2"; shift ;;
    *) echo "unknown option: $1" >&2; exit 2 ;;
  esac
  shift
done
PY="${PY:-$([ -x .venv/bin/python ] && echo .venv/bin/python || echo python3)}"
HOST="${SPARK_HOST:-100.110.180.56}"
mkdir -p data/tmp
TMP=data/tmp/spark_questions.csv

if [ -n "$(git status --porcelain -- data results dashboard/template.html)" ]; then
  echo "Uncommitted changes under data/ or results/; commit or stash them first." >&2; exit 1
fi

if [ -n "$FROM" ]; then
  cp "$FROM" "$TMP"
else
  : "${SPARK_USER:?set SPARK_USER to your spark username (or use --from FILE)}"
  scp -q "$SPARK_USER@$HOST:llm-council-forecasting/data/questions.csv" "$TMP"
fi

PREVIEW="$("$PY" -m collect.merge_outcomes "$TMP" --dry-run)"
echo "$PREVIEW"
N="$(echo "$PREVIEW" | head -1 | awk '{print $1}')"
if [ "$DRY" = 1 ]; then echo "Dry run: nothing written."; exit 0; fi
if [ "$N" = 0 ]; then echo "No new live outcomes; nothing to do."; exit 0; fi

BRANCH="data/live-outcomes-$(date +%Y%m%d-%H%M)"
git checkout -q -b "$BRANCH"
"$PY" -m collect.merge_outcomes "$TMP" > /dev/null
"$PY" -m scoring.report --set live --out results/live > /dev/null
"$PY" -m dashboard.build > /dev/null
git add data/questions.csv results/live
git commit -q -m "Live outcomes from spark: $N questions resolved; live set rescored"
echo "Committed on $BRANCH: $N new outcomes, results/live rescored, dashboard rebuilt (not committed: it's built)."
echo "Next: git push -u origin $BRANCH, then open a PR."
