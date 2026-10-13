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
   rsync -az --exclude .venv --exclude logs --exclude data/forecasts.csv --exclude .git ./ <username>@100.110.180.56:llm-council-forecasting/
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

## Outcome updates

A cron job on spark runs `python3 -m collect.update_outcomes` every Monday and Thursday at 9am (log: `logs/outcomes_cron.log`). That makes spark's `data/questions.csv` the up-to-date copy: copy it back before committing outcomes. Remove the job with `crontab -e`.

## Getting results back

Copy results to the laptop and commit them there (routine results go straight to `main`):
```bash
mkdir -p data/tmp
scp <username>@100.110.180.56:llm-council-forecasting/data/forecasts.csv data/tmp/spark_forecasts.csv
scp <username>@100.110.180.56:llm-council-forecasting/data/questions.csv data/
scp <username>@100.110.180.56:llm-council-forecasting/logs/cmds_spark.log logs/
python3 -m forecast.merge_forecasts data/tmp/spark_forecasts.csv
git add data/forecasts.csv data/questions.csv logs/cmds_spark.log && git commit -m "..." && git push
```
Merge instead of overwriting: the laptop's `data/forecasts.csv` may hold rows spark's copy doesn't (e.g. from a run written to a separate file). The merge only appends rows it doesn't already have, so locked forecasts never change.
