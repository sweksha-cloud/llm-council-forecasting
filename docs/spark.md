# Working on spark

The SJSU GPU server runs the models through Ollama. All analysis can run anywhere.

- Host: `spark-833c-1`, Tailscale address **100.110.180.56** (the old `spark-833c` / 100.107.21.115 is retired)
- Tailscale must be on, signed in with an SJSU account
- Login: `ssh <username>@100.110.180.56`

## First-time setup

1. **Log in** and lock down your home folder so other users can't read it:
   ```bash
   ssh <username>@100.110.180.56
   chmod 700 ~
   ```
2. **Copy the repo over from your laptop.** Spark gets no GitHub credentials; code goes up with rsync and results come back with scp, then get committed on the laptop:
   ```bash
   rsync -az --exclude .venv --exclude logs --exclude data/forecasts.csv --exclude data/ablation --exclude data/debate --exclude .git ./ <username>@100.110.180.56:llm-council-forecasting/
   ```
   The forecasting and collection code uses only the Python standard library, so no environment is needed on spark.

**Models are shared with other spark users.** Never run `ollama rm` there, and never use `scripts/run_local.sh` on spark (it deletes each model after use).

## Long runs

Use `tmux` so a run keeps going after you disconnect:
```bash
tmux new -s forecast            # start a session
python3 -u -m forecast.run_forecasts --set live --lock --no-think \
    --models llama3.1:8b mistral:latest qwen3:8b gemma2:9b phi3:medium \
    --chairmen llama3.1:8b qwen3:8b 2>&1 | tee -a logs/forecast_live.log
# detach: Ctrl+B, then D        reattach: tmux attach -t forecast
```
The run resumes where it stopped if interrupted; just run the same command again.

Each run's command and the exact model builds are appended to `logs/cmds_spark.log` (Prof. Bill asks for this).

deepseek-r1:8b (the Qwen3-based build on spark) ignores `think=false` and reasons past any reasonable limit at temperature 0, so it isn't in the main runs. See `docs/decisions.md`.

## Backtest queue (settled, contamination, settled-ext, DeepSeek)

1. From the laptop, on an up-to-date `main`, send the code and questions up (same rsync as above; it leaves spark's `data/forecasts.csv` alone):
   ```bash
   rsync -az --exclude .venv --exclude logs --exclude data/forecasts.csv --exclude data/ablation --exclude data/debate --exclude .git --exclude .notes --exclude .claude ./ <username>@100.110.180.56:llm-council-forecasting/
   ```
2. On spark, refill live outcomes (rsync replaced spark's `questions.csv`, which the cron job keeps current) and check the code:
   ```bash
   cd ~/llm-council-forecasting && python3 -m collect.update_outcomes
   python3 -m forecast.run_forecasts --backend fake --set settled-ext --limit 2 --models a b --chairmen a --out /tmp/check.csv  # no models used; should print 2 questions
   ```
3. Remove forecasts made with a price that has since changed (after any repricing; harmless otherwise, keeps a backup):
   ```bash
   python3 -m forecast.drop_stale
   ```
4. Start the queue (order and estimates in the script): `tmux new -s queue "bash scripts/queue_spark.sh"`
   Check on it any time (read-only): `bash scripts/status_spark.sh` — progress per set and setup, failed calls, ETA.
5. Then everything else in one session, most informative first: `tmux new -s followups "bash scripts/queue_followups.sh"` (waits for the queue session; runs the chair ablation on settled, debate, the ablation on settled-ext, then the variance seeds). The separate `queue_variance.sh`, `queue_ablation.sh` and `queue_debate.sh` still work on their own.

## Outcome updates

A cron job on spark runs `python3 -m collect.update_outcomes` every Monday and Thursday at 9am (log: `logs/outcomes_cron.log`). That makes spark's `data/questions.csv` the up-to-date copy for live outcomes. Bring them back with `SPARK_USER=<username> bash scripts/sync_live.sh` (add `--dry-run` first to see what changes): it copies only new live outcomes into the laptop's file, rescores the live set, rebuilds the dashboard and commits on a `data/live-outcomes-<date>` branch. Remove the cron job with `crontab -e`.

## Getting results back

Copy results to the laptop and commit them there (routine results go straight to `main`):
```bash
mkdir -p data/tmp
scp <username>@100.110.180.56:llm-council-forecasting/data/forecasts.csv data/tmp/spark_forecasts.csv
scp <username>@100.110.180.56:llm-council-forecasting/data/questions.csv data/
scp <username>@100.110.180.56:llm-council-forecasting/logs/cmds_spark.log logs/
make postrun SPARK=data/tmp/spark_forecasts.csv     # check, merge, make results + dashboard
git checkout -b data/settled-results && git add data/forecasts.csv data/questions.csv logs/cmds_spark.log results && git commit -m "..."
```
`make postrun` checks the spark file first (every queued setup answered every eligible question, failed calls, abstention and malformed-reply rates, one prompt version, council members, market prices match `questions.csv`, no seed/temperature overrides in the log) and stops with a report, merging nothing, if anything is off. `python3 -m forecast.postrun data/tmp/spark_forecasts.csv --dry-run` only checks. Variance runs live in their own files: copy `data/variance/seed*.csv` back as they are. So do the chair ablations: `scp …:llm-council-forecasting/data/ablation/forecasts.csv data/ablation/`, then `python3 -m analysis.ablation` (the rsync up excludes `data/ablation`, so spark's copy is never overwritten).
Merge instead of overwriting: the laptop's `data/forecasts.csv` may hold rows spark's copy doesn't (e.g. from a run written to a separate file). The merge only appends rows it doesn't already have, so locked forecasts never change.
