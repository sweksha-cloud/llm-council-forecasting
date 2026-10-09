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
2. **Give spark access to this (private) repo** with a deploy key, which only works for this one repo:
   ```bash
   ssh-keygen -t ed25519 -f ~/.ssh/llm_council_deploy -N "" -C "spark deploy key"
   cat ~/.ssh/llm_council_deploy.pub
   ```
   On GitHub: repo → Settings → Deploy keys → Add deploy key → paste it → tick **Allow write access** (so results can be pushed back). Then:
   ```bash
   cat >> ~/.ssh/config <<'EOF'
   Host github-llm-council
     HostName github.com
     User git
     IdentityFile ~/.ssh/llm_council_deploy
   EOF
   git clone git@github-llm-council:sweksha-cloud/llm-council-forecasting.git
   ```
3. **Run the setup script** from the repo:
   ```bash
   cd llm-council-forecasting
   bash scripts/setup_spark.sh
   ```
   It creates the Python environment, runs the tests and a fake forecast, checks which models Ollama has, records their exact builds, and runs one real question as a smoke test.

## Long runs

Use `tmux` so a run keeps going after you disconnect:
```bash
tmux new -s forecast            # start a session
source .venv/bin/activate
python3 -m forecast.run_forecasts --set live --lock --no-think \
    --models llama3.1:8b mistral:latest qwen3:8b gemma2:9b phi3:medium deepseek-r1:8b \
    --chairmen llama3.1:8b qwen3:8b 2>&1 | tee -a logs/forecast_live.log
# detach: Ctrl+B, then D        reattach: tmux attach -t forecast
```
The run resumes where it stopped if interrupted; just run the same command again.

Save the commands you ran (Prof. Bill asks for this):
```bash
history > logs/cmds_$(date +%Y%m%d).log
```

## Getting results back

Commit results on a branch, push, and open a pull request. Never push to `main`:
```bash
git switch -c results/live-run-1
git add data/forecasts.csv logs/
git commit -m "Live-set forecasts, locked"
git push -u origin results/live-run-1
```
