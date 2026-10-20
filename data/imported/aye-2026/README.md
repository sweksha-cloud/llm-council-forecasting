# Aye Nyein Kyaw's council results (Spring/Summer 2026)

Everything in this folder comes from **Aye Nyein Kyaw**'s LLM-as-Council work, advised by
Prof. Bill Andreopoulos at San Jose State University: https://github.com/JennicaANK/llm-council-judge.
Please credit her when using it.

- `source/new_council_detailed.xlsx`: her per-question council results for the new set. It isn't in
  her repo; it was copied from her run on the SJSU GPU server (dated 2026-07-29) and is pinned by
  sha256 in `importers/import_aye.py`. Published here with credit to her.
- `questions.csv`, `forecasts.csv`, `summary.csv`: her questions and answers converted into this
  project's record format by `importers/import_aye.py`, and re-scored with this project's metrics
  (her reported accuracy had scoring bugs; see `docs/plan.md`).
- `market_prices.csv`: Polymarket prices on her collection dates, added by this project
  (`importers/aye_market_prices.py`).
