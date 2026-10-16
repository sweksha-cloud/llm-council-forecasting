# Power analysis: what can ~360 settled questions detect?

Reproduce with `python3 -m analysis.power` (under a second; the simulation is seeded).

## Method

Every main comparison is paired: council vs market, council vs its best member, on the same questions. With per-question difference `d = Brier(a) − Brier(b)`, the smallest true mean difference detected 80% of the time at two-sided α = 0.05 is

> MDE = 2.80 × sd(d) / √n

so the answer depends on sd(d). Two sources:

1. **Aye's results.** Her answers are 0 or 1, so each question's Brier is 0 or 1 and sd(d) is close to its maximum. This is a pessimistic bound and doesn't describe probability forecasts.
2. **Simulation on our settled set.** It uses the real 362 questions, their market prices (market Brier 0.144) and outcomes. A model's forecast is the market price plus Gaussian noise of sd σ in log-odds. A council is a second draw whose noise has correlation 0.7 with the member's, since it is built from the same answers. σ is matched to plausible model quality:

| σ | Simulated model's Brier | Roughly |
|---|---|---|
| 0.5 | 0.150 | close to the market |
| 1.0 | 0.166 | a strong model |
| 1.5 | 0.187 | |
| 2.0 | 0.209 | typical of 8B models on question sets like ours |

**Design effect.** Questions aren't independent: there are several "ceasefire by ⟨date⟩?" and "Hormuz traffic normal by ⟨date⟩?" markets. The settled collector allows one market per event, but related events remain. A design effect of 1.5 (effective n ≈ 240) is shown as a sensitivity check.

## Results (n = 362)

| Comparison | sd(d) | MDE | MDE, design effect 1.5 | n to detect 0.01 | 0.02 | 0.05 |
|---|---|---|---|---|---|---|
| Aye: qwen3 council vs market | 0.429 | 0.063 | 0.077 | 14,426 | 3,607 | 578 |
| Aye: llama3.1 council vs mean | 0.719 | 0.106 | 0.130 | 40,546 | 10,137 | 1,622 |
| Sim σ=1.0: council vs market | 0.141 | 0.021 | 0.025 | 1,565 | 392 | 63 |
| Sim σ=1.0: council vs a member | 0.111 | 0.016 | 0.020 | 964 | 241 | 39 |
| Sim σ=1.5: council vs market | 0.198 | 0.029 | 0.036 | 3,086 | 772 | 124 |
| Sim σ=1.5: council vs a member | 0.159 | 0.023 | 0.029 | 1,981 | 496 | 80 |
| **Sim σ=2.0: council vs market** | 0.244 | **0.036** | 0.044 | 4,690 | 1,173 | 188 |
| **Sim σ=2.0: council vs a member** | 0.201 | **0.030** | 0.036 | 3,172 | 793 | 127 |

The full table, with every Aye comparison and σ = 0.5, is in the script output.

**Contamination split** (153 older vs 362 settled questions, two independent groups): the MDE is 0.06–0.08 on raw Brier. Using Brier minus the market's Brier on the same question (`excess_gap` in `results/backtest/contamination.csv`) brings it down to 0.04–0.06 at σ = 1–2, because it removes question difficulty. Only a large recall effect will show.

## What this means

- **Council vs market: 360 is enough.** If the 8B councils land near Brier 0.20 against the market's 0.144, the gap (about 0.05) is above the MDE (0.036, or 0.044 with clustering). Aye's results already show councils far worse than the market.
- **Council vs its best member: 360 is not enough** unless the effect is large. Aggregation gains in the literature are usually around 0.005–0.02 Brier. At realistic σ, 360 questions detect only about 0.03; detecting 0.02 needs about 800 (σ = 2) to 500 (σ = 1.5). Detecting 0.01 needs thousands, which isn't feasible here. A null result on 360 would be "no difference larger than ~0.03", not "no difference".
- **Contamination: only large effects.** Report it with its interval, and lead with `excess_gap`.

## Should you collect more questions now?

**Yes, if council vs best member is a headline question; collect now and forecast later.**

- **Why now:** collection is cheap (minutes, no spark), and settled questions don't expire.
- **Target:** about 1,000 settled questions in total, roughly 640 more. That brings the council-vs-member MDE from 0.030 to about 0.018 at σ = 2, and from 0.023 to about 0.014 at σ = 1.5. That covers the upper half of plausible aggregation gains.
- **Spark cost:** grows linearly, so 640 more questions is about 1.8× the current settled run. Run the existing 360 first so those results land first, then queue the rest.
- **Where they'd come from:** questions must resolve after every model's cutoff (Qwen3, Apr 2025) to stay contamination-free. Widen the window with `python3 -m collect.collect_settled --from 2025-07-01 --to 2026-06-30 --per-source 350`. The current set covers Jul–Oct 2026. That is a choice of time range, and it's yours to make, because it mixes in an earlier period.

If the paper only needs council vs market and the descriptive comparisons, 360 is enough and no more collection is needed.

## Update 2026-10-16: the full settled sample (n = 1,040)

`python3 -m analysis.power --set settled settled-ext`. The extension is 680 Polymarket questions (Jul 2025–Jun 2026), so the combined market Brier is 0.168 and 43.6% resolved Yes. A new row, **council vs the pool of its own members** (simulated with noise correlation 0.85), is the pre-registered main comparison.

Minimum detectable Brier difference at 80% power, α = 0.05, paired, at σ = 2.0 (simulated forecaster Brier ≈ 0.23, typical of 8B models):

| Comparison | n = 360 | **n = 1,040** | n = 1,040, design effect 1.5 |
|---|---|---|---|
| Council vs market | 0.037 | **0.022** | 0.027 |
| Council vs a member | 0.030 | **0.018** | 0.022 |
| Council vs pool of its members | 0.022 | **0.013** | 0.016 |
| Contamination split, Brier minus market (153 older vs the rest) | 0.063 | 0.060 | — |

**What 1,040 can and can't detect:**
- **Council vs market:** any gap above about 0.02–0.03. Expected gaps are far larger.
- **Council vs pool / member:** differences of about 0.013–0.02. That covers the upper half of published aggregation gains (0.005–0.02), so a null result rules out a meaningful gain. It does not rule out gains around 0.005–0.01, which need 3,000+ questions.
- **Contamination:** only large recall effects (about 0.06). This is limited by the 153 older questions, not by the settled count.
- **Per source:** Kalshi is 200 questions, so per-source council comparisons on Kalshi detect only about 0.04. The pooled result uses a source-stratified bootstrap and is always shown next to the per-source ones (pre-registration in `docs/decisions.md`).
