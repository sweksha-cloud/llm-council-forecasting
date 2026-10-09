# Models and knowledge cutoffs

Used for the Week 8 contamination check: a model can only "remember" an outcome
if the question resolved before the model's training data was collected.

**Release date is a safe upper bound on the cutoff.** A model can't have seen
anything that happened after it was released. Published cutoffs are used where
the developer states one; otherwise the cutoff is unknown and only the release
date is used.

| Ollama tag | Model | Released | Stated training cutoff | Source |
|---|---|---|---|---|
| `llama3.1:8b` | Llama 3.1 8B Instruct (Meta) | Jul 2024 | Dec 2023 | Meta model card |
| `mistral:latest` | Mistral 7B Instruct v0.3 | May 2024 | not published | — |
| `qwen3:8b` | Qwen3 8B (Alibaba) | Apr 2025 | not published | — |
| `gemma2:9b` | Gemma 2 9B (Google) | Jun 2024 | not published | — |
| `phi3:medium` | Phi-3 Medium 14B (Microsoft) | May 2024 | Oct 2023 | Microsoft model card |
| `deepseek-r1:8b` | DeepSeek-R1 distill, 8B | 2025 | not published | — |

⚠️ To verify before Week 8:
- Check each cutoff against the official model card.
- Ollama tags can point to different builds over time. `deepseek-r1:8b` in particular has meant both a Llama-based and a Qwen3-based distill. Record the exact build actually used on spark (`ollama show <tag>` and the digest from `ollama list`); `scripts/setup_spark.sh` saves this to `docs/spark_models.txt`.

## What this means for the question sets

- Every question in the current live and settled sets resolves in **2026**, after all of these models were released. **None of them can be contaminated.** That's good for the main results.
- So the Week 8 check needs an extra **older settled subset**: questions that resolved *before* a model's cutoff (e.g. 2023 to early 2024), compared against questions resolved after it. If models score much better on the older questions, that suggests recall rather than forecasting. The settled collector can do this with `--from` / `--to`, if the markets' price history goes back that far.
