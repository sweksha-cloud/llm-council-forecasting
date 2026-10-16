# Re-analysis of the earlier council study

*Draft paper section. Every number comes from `results/aye-2026-new/` and `results/aye-2026-old/` (`make results`). The import and grading are in `importers/import_aye.py`; market prices are in `importers/aye_market_prices.py`.*

## Setup

Aye Nyein Kyaw's 2026 study asked six 8–14B open models, and councils built from them, Polymarket Yes/No questions in free text. Each council had one of three chairs: Llama 3.1 8B, Mistral 7B or Qwen3 8B. Answers were scored by an LLM judge (1–5). We re-scored the same answers against **how the questions actually resolved**, with three changes.

1. **Strict grading.** An answer counts as Yes or No only if it says so explicitly: it starts with Yes/No or labels it ("Answer: No"). Everything else is an abstention. The original scripts matched substrings, so "not" counted as No, and they scored unreadable judge replies as 1.
2. **Market baseline.** The original files had no prices. We took each question's Polymarket Yes price at 00:00 UTC on the day it was collected, before any model was asked (2,404 of 2,501 questions priced).
3. **Reference baselines.**
   - "Always No" says 0% on every question.
   - The base rate says the share that resolved Yes on every question. It uses the outcomes, so it's mildly optimistic.

Answers are 0 or 1, so each answered question's Brier score is 0 (right) or 1 (wrong): Brier here equals the error rate. We report Brier for comparability with probability forecasts, plus accuracy and call-based ground-truth metrics.

The new set has 1,611 resolved Yes/No questions, collected 15 July 2026; **33.0% resolved Yes**. The old set (890 questions, April 2026) has no council file. Its single models answered at most 9 questions each under strict grading, so we report only its market baseline.

## Finding 1: the councils are far worse than the market

**Table 1.** New set, on each setup's answered questions.

| Setup | Answered (coverage) | Brier | Accuracy | Balanced acc. | MCC |
|---|---|---|---|---|---|
| Council, Llama 3.1 chair | 936 (58%) | 0.343 | 65.7% | 0.602 | 0.215 |
| Council, Mistral chair | 512 (32%) | 0.357 | 64.3% | 0.645 | 0.280 |
| Council, Qwen3 chair | 191 (12%) | 0.283 | 71.7% | 0.590 | 0.193 |
| Best single (Phi-3 Medium) | 887 (55%) | 0.646 | 35.4% | 0.521 | 0.075 |
| Always No | 1,611 (100%) | 0.330 | 67.0% | 0.500 | 0 |
| Base rate (0.33) | 1,611 (100%) | 0.221 | 67.0% | 0.500 | 0 |
| **Market** | 1,572 (98%) | **0.194** | **72.2%** | **0.638** | **0.370** |

Paired on the questions both answered, every council's Brier score is higher than the market's by 0.16–0.19. All three 95% bootstrap intervals exclude zero (Table 2). As Brier skill vs the market, the councils score −0.85 to −1.36: their squared error is roughly double the market's.

## Finding 2: the councils are no better than always saying No

The councils' accuracy (64–72%) brackets the 67% that "always No" gets for free, and the paired Brier differences are indistinguishable from zero:

**Table 2.** Paired Brier difference, council minus reference (negative = council better), with 95% bootstrap interval.

| Council | vs market | vs always No | vs best single | vs mean of singles |
|---|---|---|---|---|
| Llama 3.1 chair | +0.158 [0.129, 0.188], n=901 | −0.006 [−0.037, 0.029], n=936 | −0.196 [−0.257, −0.136], n=479 | −0.135 [−0.249, −0.015], n=151 |
| Mistral chair | +0.193 [0.152, 0.231], n=484 | −0.006 [−0.066, 0.055], n=512 | −0.112 [−0.190, −0.045], n=268 | −0.123 [−0.243, 0.005], n=96 |
| Qwen3 chair | +0.168 [0.107, 0.236], n=172 | +0.037 [−0.026, 0.105], n=191 | −0.314 [−0.441, −0.196], n=102 | −0.311 [−0.462, −0.145], n=49 |

**The councils beat the single models by saying No more often, not by aggregating better.**
- **Single models:** they call Yes on most questions they answer. Phi-3 does so on 822 of 887, and its recall on Yes events is 0.96.
- **Councils:** they call No on 52–80% of questions.
- **Why that matters:** two-thirds of questions resolve No, so moving toward No alone cuts the error rate, with or without deliberation.

Balanced accuracy and MCC separate the two effects:
- **Councils:** some genuine discrimination (balanced accuracy 0.59–0.65, MCC 0.19–0.28).
- **Single models:** close to none (balanced accuracy 0.35–0.57).
- **Market:** better than both (MCC 0.37).

## Finding 3: the LLM judge doesn't track correctness

The original study ranked setups by judge score. We split each setup's answered questions into right and wrong answers and compared their judge scores:

**Table 3.** LLM-judge score (1–5) for answers that turned out right vs wrong. AUROC = chance a right answer got a higher score than a wrong one (0.5 = can't tell them apart).

| Setup | Right / wrong | Judge, right | Judge, wrong | AUROC |
|---|---|---|---|---|
| Council, Llama 3.1 chair | 615 / 321 | 4.78 | 4.81 | 0.48 |
| Council, Mistral chair | 329 / 183 | 4.26 | 4.37 | 0.44 |
| Council, Qwen3 chair | 137 / 54 | 4.75 | 4.67 | 0.54 |
| Phi-3 Medium | 205 / 392 | 4.23 | 4.32 | 0.46 |
| DeepSeek-R1 8B | 38 / 68 | 4.61 | 4.41 | 0.60 |

The judge's AUROC is 0.44–0.54 for the three councils and the largest single-model sample. On the smaller single-model samples (36–54 judged answers) it ranges up to 0.66. Wrong answers score as high as right ones; for two of the three councils, slightly higher. A high judge score says an answer reads well, not that it is correct. This is the expected failure of LLM-as-a-judge on questions with an outcome, and it is why we evaluate with proper scoring rules.

## Caveats

- **Abstention is not random.** Strict grading leaves most single-model answers ungraded (coverage 2.5–8.6% except Phi-3 at 55%), and councils answered 12–58%. Each setup is scored on the questions it chose to answer explicitly, so rows in Table 1 cover different questions. Table 2 compares setups only on shared questions. Counting every abstention as 50% (`brier_abstain_0.5` in `scores.csv`) gives the councils 0.25–0.30 and the market 0.195; the ordering doesn't change.
- **Grading choices.** A looser grader would answer more questions and change the coverage, though not the market or always-No rows. The strict rule was fixed before re-scoring (see `docs/decisions.md`) and is unit-tested.
- **0/1 answers.** With 0/1 answers, Brier is the error rate, and log score, ECE and AUROC carry little information; we don't interpret them. The comparison with the market is inherently unfavourable to the councils: a forecaster that never hedges pays the full penalty on every miss. That is a property of the original design (no probability was asked for) and is part of the finding.
- **Market timing.** The price is from the collection date. Questions closed days to months later, so the market faced a longer horizon than a price taken at a fixed lead time would; this works against the market, not for it. 39 new-set questions had no trade in the two days before collection and have no market price.
- **Judge self-preference.** The judge was Llama 3.1 8B, which is also a council member, one of the chairs, and a single model under evaluation. LLM judges are known to favour their own outputs (Zheng et al., 2023).
- **Related questions.** Several markets come from the same event family, e.g. dated deadlines for the same ceasefire. The bootstrap treats questions as independent, so the intervals are somewhat too narrow. The council-vs-market gaps are large enough that this doesn't change the conclusion; the always-No comparisons were already null.
- **Single source.** All questions are Polymarket questions from two collection dates, and topics follow what was trading then.
- **Old set.** Under strict grading, its single models answered 2, 7 and 9 of 839 questions. No conclusion about them is possible. Its market baseline (Brier 0.194, accuracy 66.9%, n=832) matches the new set's.
