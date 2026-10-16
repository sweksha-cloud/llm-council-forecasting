# Related work

*Draft section. Every reference below was checked against its arXiv page, Crossref record or proceedings listing on 2026-10-16 (see the note at the end). Claims about each paper are taken from its abstract unless marked otherwise.*

## LLMs as forecasters

Early benchmarks showed language models well short of human forecasters. **Autocast** (Zou et al., 2022) paired tournament questions with a date-organised news corpus, so models could be tested under the conditions human forecasters had faced. Its authors found performance "far below a human expert baseline". When GPT-4 entered a three-month Metaculus tournament in 2023, its binary forecasts were significantly less accurate than the median of 843 human participants. They were also not significantly different from saying 50% on every question (Schoenegger & Park, 2023).

Two lines of work narrowed the gap. **Retrieval and aggregation:** Halawi et al. (2024) built a system that searches for news, generates several forecasts and aggregates them. On questions published after the models' knowledge cutoffs, it nears the crowd aggregate of competitive forecasters and in some settings surpasses it. **Ensembling:** Schoenegger et al. (2024) aggregated twelve LLMs on 31 binary questions. Their pre-registered analysis found the LLM crowd beat a no-information benchmark and was not statistically different from a crowd of 925 human forecasters. They also report an *acquiescence effect*: mean model predictions sat above 50% although outcomes were split almost evenly.

Pratt et al. (2024) report the opposite bias on their dataset. Models tend to guess that most events are unlikely, which happens to be right for many prediction datasets. Our re-analysis of earlier council results finds the same pattern: councils matched an "always No" baseline, not the market.

Larger and continuously updated benchmarks put these claims in context. **ForecastBench** (Karger et al., 2025) asks only about events with no known answer at submission time, so the answer can't have leaked into training data. On a 200-question subset, expert forecasters outperformed the best LLM (p < 0.001). Paleka et al. (2025) argue that many published comparisons can't be trusted as they stand. They catalogue forms of **temporal leakage** in retrospective evaluations, from training data, retrieval and question selection, and they caution against extrapolating benchmark performance to real-world forecasting. Paleka et al. (2024) propose consistency checks on logically related questions as an evaluation that doesn't require waiting for outcomes.

**How this project differs.** We study small open models (7–14B) run locally, not frontier APIs. We compare a deliberating council against the same models' independent forecasts and statistical pools on identical questions. We score everything against the prediction-market price on the date the question was asked. Our settled-set design follows the leakage concerns above: questions resolve after every model's release, and models are told the date of the market price, not today's date. A separate older subset, resolved before the models' training cutoffs, measures how much apparent skill could be recall.

## Combining forecasts and multi-agent LLMs

**Aggregating human forecasts:**
- Satopää et al. (2014) derive an aggregator from a simple model of how experts estimate probabilities. It has a closed form governed by one parameter. On over 1,300 forecasters predicting 69 geopolitical events, it outperformed widely used aggregation methods.
- Baron et al. (2014) explain why averaged probabilities should be pushed toward 0 or 1 (*extremised*), for two reasons. First, random error compresses an average toward 0.5. Second, each forecaster discounts for their own ignorance of the total body of information, which the combined crowd actually has.
- In the Good Judgment Project, training, teaming and tracking improved accuracy in a geopolitical forecasting tournament (Mellers et al., 2014).
- Our mean, median, logit-pool and extremised-pool baselines come from this literature.

**Multi-agent LLM methods:**
- Multiagent debate (Du et al., 2023): several model instances propose and critique answers over rounds. It improved reasoning and factual accuracy on their tasks.
- Mixture-of-Agents (Wang et al., 2024): layers of models refine the previous layer's outputs.
- The Language Model Council (Zhao et al., 2024): a group of LLMs writes tests, answers them and judges each other, to rank models on subjective tasks.
- Our council is closest to a one-round Mixture-of-Agents with a chairman. The open question here is whether deliberation adds anything over pooling the same members' probabilities. On forecasting, unlike the tasks above, that can be measured with a proper scoring rule against real outcomes.

## Evaluation: proper scores, not judges

- **Brier score (Brier, 1950):** the squared error between probability and outcome. It is *strictly proper*: a forecaster minimises their expected score only by reporting their true belief (Gneiting & Raftery, 2007).
- **Murphy decomposition (Murphy, 1973):** splits the Brier score into reliability (calibration), resolution and uncertainty. We report it alongside expected calibration error and sharpness.
- **Market prices** are a strong reference forecast because they aggregate the information and incentives of traders (Wolfers & Zitzewitz, 2004).

**LLM-as-a-judge (Zheng et al., 2023)** is now common for open-ended outputs, and the council design we build on was originally scored that way. But a judge rates how good an answer *looks*, not whether the event happened. Zheng et al. themselves document position, verbosity and self-enhancement biases in LLM judges. For forecasting questions with known outcomes, we use proper scoring rules and report judge scores only to show how far they diverge from the truth.

## References

- Baron, J., Mellers, B. A., Tetlock, P. E., Stone, E., & Ungar, L. H. (2014). Two reasons to make aggregated probability forecasts more extreme. *Decision Analysis*, 11(2), 133–145. https://doi.org/10.1287/deca.2014.0293
- Brier, G. W. (1950). Verification of forecasts expressed in terms of probability. *Monthly Weather Review*, 78(1), 1–3. https://doi.org/10.1175/1520-0493(1950)078<0001:VOFEIT>2.0.CO;2
- Du, Y., Li, S., Torralba, A., Tenenbaum, J. B., & Mordatch, I. (2023). Improving factuality and reasoning in language models through multiagent debate. arXiv:2305.14325.
- Gneiting, T., & Raftery, A. E. (2007). Strictly proper scoring rules, prediction, and estimation. *Journal of the American Statistical Association*, 102(477), 359–378. https://doi.org/10.1198/016214506000001437
- Halawi, D., Zhang, F., Yueh-Han, C., & Steinhardt, J. (2024). Approaching human-level forecasting with language models. *Advances in Neural Information Processing Systems 37 (NeurIPS 2024)*. arXiv:2402.18563.
- Karger, E., Bastani, H., Yueh-Han, C., Jacobs, Z., Halawi, D., Zhang, F., & Tetlock, P. E. (2025). ForecastBench: A dynamic benchmark of AI forecasting capabilities. *International Conference on Learning Representations (ICLR 2025)*. arXiv:2409.19839.
- Mellers, B., Ungar, L., Baron, J., Ramos, J., Gurcay, B., Fincher, K., Scott, S. E., Moore, D., Atanasov, P., Swift, S. A., Murray, T., Stone, E., & Tetlock, P. E. (2014). Psychological strategies for winning a geopolitical forecasting tournament. *Psychological Science*, 25(5), 1106–1115. https://doi.org/10.1177/0956797614524255
- Murphy, A. H. (1973). A new vector partition of the probability score. *Journal of Applied Meteorology*, 12(4), 595–600. https://doi.org/10.1175/1520-0450(1973)012<0595:ANVPOT>2.0.CO;2
- Paleka, D., Sudhir, A. P., Alvarez, A., Bhat, V., Shen, A., Wang, E., & Tramèr, F. (2024). Consistency checks for language model forecasters. arXiv:2412.18544.
- Paleka, D., Goel, S., Geiping, J., & Tramèr, F. (2025). Pitfalls in evaluating language model forecasters. arXiv:2506.00723.
- Pratt, S., Blumberg, S., Carolino, P. K., & Morris, M. R. (2024). Can language models use forecasting strategies? arXiv:2406.04446.
- Satopää, V. A., Baron, J., Foster, D. P., Mellers, B. A., Tetlock, P. E., & Ungar, L. H. (2014). Combining multiple probability predictions using a simple logit model. *International Journal of Forecasting*, 30(2), 344–356. https://doi.org/10.1016/j.ijforecast.2013.09.009
- Schoenegger, P., & Park, P. S. (2023). Large language model prediction capabilities: Evidence from a real-world forecasting tournament. arXiv:2310.13014.
- Schoenegger, P., Tuminauskaite, I., Park, P. S., Bastos, R. V. S., & Tetlock, P. E. (2024). Wisdom of the silicon crowd: LLM ensemble prediction capabilities rival human crowd accuracy. *Science Advances*, 10(45), eadp1528. https://doi.org/10.1126/sciadv.adp1528
- Wang, J., Wang, J., Athiwaratkun, B., Zhang, C., & Zou, J. (2024). Mixture-of-agents enhances large language model capabilities. arXiv:2406.04692.
- Wolfers, J., & Zitzewitz, E. (2004). Prediction markets. *Journal of Economic Perspectives*, 18(2), 107–126. https://doi.org/10.1257/0895330041371321
- Zhao, J., Plaza-del-Arco, F. M., Genchel, B., & Curry, A. C. (2024). Language Model Council: Democratically benchmarking foundation models on highly subjective tasks. arXiv:2406.08598.
- Zheng, L., Chiang, W.-L., Sheng, Y., Zhuang, S., Wu, Z., Zhuang, Y., Lin, Z., Li, Z., Li, D., Xing, E. P., Zhang, H., Gonzalez, J. E., & Stoica, I. (2023). Judging LLM-as-a-judge with MT-Bench and Chatbot Arena. *NeurIPS 2023 Datasets and Benchmarks Track*. arXiv:2306.05685.
- Zou, A., Xiao, T., Jia, R., Kwon, J., Mazeika, M., Li, R., Song, D., Steinhardt, J., Evans, O., & Hendrycks, D. (2022). Forecasting future world events with neural networks. *NeurIPS 2022 Datasets and Benchmarks Track*. arXiv:2206.15474.

## How these were checked

| Kind | Check |
|---|---|
| arXiv papers (12) | Title, authors and first-version date read from each paper's arxiv.org abstract page (`citation_*` meta tags); every summary above is from its abstract |
| Journal papers (8) | Title, authors, year, volume, issue and pages from the Crossref record for the DOI listed; summaries from the Crossref abstract where it has one (Baron, Mellers) |
| Venues | NeurIPS 2024 (Halawi et al.): neurips.cc poster page and proceedings DOI 10.52202/079017-1598. ICLR 2025 (Karger et al.): proceedings.iclr.cc. NeurIPS 2022/2023 tracks: the arXiv comment field |

Full author lists were checked for every entry (arXiv meta tags or Crossref).
- **Satopää et al. (2014):** the summary is from its abstract as indexed on IDEAS/RePEc and Academia.edu, since Crossref has no abstract for it.
- **Schoenegger et al. (2024):** the journal version adds Bastos, who isn't on the arXiv version; the journal list is used.
- **Venues:** Pratt et al. (2024) and both Paleka et al. papers are cited as arXiv preprints. Check for published versions before submission.
