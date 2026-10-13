# Decisions log

One line per decision: what was decided, why, and what it affects. Newest first. Add to it whenever a choice could change the results.

| Date | Decision | Why | Affects |
|---|---|---|---|
| 2026-10-12 | Run deepseek-r1:8b separately with a 1,024-token thinking budget, then force it to answer | It answered 6 of 6 test questions this way (about 110 s each) vs 0 of 4 with a plain 2,048-token cap. It's a single model only, not a council member | DeepSeek results on settled and contamination sets |
| 2026-10-12 | Pause the settled run until the live top-up finishes | Live questions close daily; settled questions don't, and two runs at once slowed both | Run order |
| 2026-10-12 | Re-score Aye's councils against an "always No" baseline, not only against single models | 67% of her questions resolved No; councils looked better mainly by answering No more often | Week 9 notes |
| 2026-10-12 | Top up the live set with 145 new questions closing by Nov 15 | 58 of the original 400 closed before the live run could start | Live set size, Week 11 |
| 2026-10-12 | Settled questions are asked "as of" their price date (7 days before close), and scored against the price at that date | Telling the model today's date, after the question closed, would leak information; today's price is already ~0 or 1 | Settled and contamination runs |
| 2026-10-12 | Leave deepseek-r1:8b out of the main runs | It ignores `think=false` and reasons past 2,000 tokens without answering at temperature 0; it would take 2+ days per run, too slow for live questions | Model list; council has 5 members |
| 2026-10-12 | Councils use 2 chairmen: llama3.1:8b and qwen3:8b | Two chairmen show whether results depend on which model chairs | All council results |
| 2026-10-12 | First 84 live Llama answers kept from the laptop run | Same model build as spark (46e0c10c039e), same prompt | Live set |
| 2026-10-10 | Prompt v2: ask for reasoning before the probability | With the number first, llama3.1:8b answered 0.55 on 12 of 15 test questions | All forecasts (no v1 forecasts exist) |
| 2026-10-09 | Grade earlier free-text answers strictly: Yes/No only if stated explicitly, otherwise abstain | Substring matching counted "not" as "No"; failed judge reads were scored as 1 | Aye re-scoring |
| 2026-10-09 | Exclude crypto and price-threshold markets from collection | They're mostly coin-flip price bets, not forecastable events | Question sets |
| 2026-10-09 | Live questions: at most 1 per event and 40% per topic | Kalshi was dominated by sports and near-duplicate questions | Question sets |
