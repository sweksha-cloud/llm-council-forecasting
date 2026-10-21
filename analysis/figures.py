"""
figures.py
----------
The paper's figures, built only from files in results/ (so `make results figures` regenerates them).

  results/figures/council_vs_average.png   left: Brier of the market, the mean pool, the best member,
                                           each council and the base rate on settled-all; right: every
                                           chair minus the mean pool of its members, with 95% intervals
                                           (results/ablation/ablation_view.csv once the ablation is merged,
                                           else the two main councils from results/settled/comparisons.csv)
  results/figures/reliability.png          reliability diagram: councils, mean pool and market (settled-all)
  results/figures/self_preference.png      each chair's extra weight on its own model, with 95% intervals
                                           (results/ablation/self_preference.csv; skipped if missing)

Usage (from the repo root):  python3 -m analysis.figures
"""

import csv
from pathlib import Path

import matplotlib

matplotlib.use("Agg")
import matplotlib.pyplot as plt  # noqa: E402

ROOT = Path(__file__).resolve().parent.parent
RES = ROOT / "results"
OUT = RES / "figures"
INK, ACC, MUTE, BAD = "#1f2937", "#2563eb", "#9ca3af", "#dc2626"
NAMES = {"llama3.1:8b": "Llama 3.1", "qwen3:8b": "Qwen 3", "gemma2:9b": "Gemma 2", "mistral:latest": "Mistral",
         "phi3:medium": "Phi-3", "llama3.3:70b": "Llama 3.3 70B"}


def _rows(path: Path):
    if not path.exists() or path.stat().st_size == 0:
        return []
    with path.open(newline="", encoding="utf-8") as f:
        return list(csv.DictReader(f))


def _clean(ax):
    for s in ("top", "right"):
        ax.spines[s].set_visible(False)


def _chair(setup: str) -> str:
    return NAMES.get(setup.split("chair=", 1)[1], setup.split("chair=", 1)[1])


def chair_vs_mean_rows():
    """(label, mean_diff, ci_low, ci_high, n) for every full-view council vs the mean pool."""
    abl = [r for r in _rows(RES / "ablation" / "ablation_view.csv")
           if r.get("source") == "all" and r["versus"] == "baseline:mean" and r["setup"].startswith("council:chair=")]
    if abl:
        return [(_chair(r["setup"]), float(r["mean_diff"]), float(r["ci_low"]), float(r["ci_high"]), int(r["n"])) for r in abl]
    return [(_chair(r["council"]), float(r["mean_diff"]), float(r["ci_low"]), float(r["ci_high"]), int(r["n"]))
            for r in _rows(RES / "settled" / "comparisons.csv") if r["versus"] == "baseline:mean" and r.get("ci_low")]


def council_vs_average(out: Path) -> bool:
    scores = {r["setup"]: r for r in _rows(RES / "settled-all" / "scores.csv")}
    if "market" not in scores or not any(s.startswith("council:") for s in scores):
        return False
    bars = [("Prediction market", "market", INK), ("Average of the members", "baseline:mean", MUTE),
            ("Best single model", "baseline:best_single", MUTE)]
    bars += [(f"Council, {_chair(s)} chair", s, ACC) for s in sorted(scores) if s.startswith("council:chair=")]
    bars += [("Always the base rate", "baseline:base_rate", MUTE)]
    bars = [b for b in bars if b[1] in scores and scores[b[1]].get("brier")]
    n = scores["market"]["answered"]
    fig, (a, b) = plt.subplots(1, 2, figsize=(12, 4.6), gridspec_kw={"width_ratios": [1.05, 1]})
    ys = list(range(len(bars)))[::-1]
    vals = [float(scores[k]["brier"]) for _, k, _ in bars]
    a.barh(ys, vals, color=[c for *_, c in bars], height=0.6)
    for y, v in zip(ys, vals):
        a.text(v + 0.004, y, f"{v:.3f}", va="center", fontsize=10, color=INK)
    a.set_yticks(ys)
    a.set_yticklabels([lbl for lbl, *_ in bars], fontsize=10)
    a.set_xlim(0, max(vals) * 1.2)
    a.set_xlabel("Brier score (lower is better)")
    a.set_title(f"{int(n):,} resolved Polymarket & Kalshi questions", fontsize=11, loc="left")
    _clean(a)
    rows = sorted(chair_vs_mean_rows(), key=lambda r: r[1])
    for i, (lbl, m, lo, hi, _) in enumerate(rows):
        col = BAD if lo > 0 else ACC
        b.plot([lo, hi], [i, i], color=col, lw=2.5)
        b.plot(m, i, "o", color=col, ms=8)
    b.axvline(0, color=INK, lw=1, ls="--")
    b.set_yticks(range(len(rows)))
    b.set_yticklabels([f"{lbl} as chair" for lbl, *_ in rows], fontsize=10)
    b.set_xlabel("Council minus simple average (Brier; right = council worse)")
    b.set_title("No chair beats the plain average of its members", fontsize=11, loc="left")
    if rows:
        b.text(0.99, 0.02, f"95% CI, {rows[0][4]} settled questions", transform=b.transAxes, ha="right",
               fontsize=8.5, color="#6b7280")
    _clean(b)
    fig.suptitle("Do LLM councils forecast better than averaging their models? No.", fontsize=13, x=0.01,
                 ha="left", fontweight="bold")
    fig.tight_layout()
    fig.savefig(out, dpi=200, facecolor="white")
    plt.close(fig)
    return True


def reliability(out: Path) -> bool:
    rows = _rows(RES / "settled-all" / "reliability.csv")
    keep = [s for s in ("market", "baseline:mean", "council:chair=llama3.1:8b", "council:chair=qwen3:8b")
            if any(r["setup"] == s for r in rows)]
    if not keep:
        return False
    style = {"market": (INK, "Market"), "baseline:mean": (MUTE, "Average of members"),
             "council:chair=llama3.1:8b": (ACC, "Council, Llama chair"), "council:chair=qwen3:8b": ("#7c3aed", "Council, Qwen chair")}
    fig, ax = plt.subplots(figsize=(5.2, 5))
    ax.plot([0, 1], [0, 1], ls="--", color="#d1d5db", lw=1)
    for s in keep:
        pts = [(float(r["mean_forecast"]), float(r["observed_rate"])) for r in rows if r["setup"] == s and int(r["count"]) >= 10]
        col, lbl = style[s]
        ax.plot([p for p, _ in pts], [o for _, o in pts], "o-", color=col, label=lbl, ms=4)
    ax.set_xlabel("Forecast probability (binned)")
    ax.set_ylabel("Share that resolved Yes")
    ax.set_title("Calibration, settled questions", fontsize=11, loc="left")
    ax.legend(frameon=False, fontsize=9)
    _clean(ax)
    fig.tight_layout()
    fig.savefig(out, dpi=200, facecolor="white")
    plt.close(fig)
    return True


def self_preference(out: Path) -> bool:
    rows = _rows(RES / "ablation" / "self_preference.csv")
    if not rows:
        return False
    rows.sort(key=lambda r: float(r["own_weight_minus_others"]))
    fig, ax = plt.subplots(figsize=(6, 0.6 * len(rows) + 1.4))
    for i, r in enumerate(rows):
        m, lo, hi = float(r["own_weight_minus_others"]), float(r["ci_low"]), float(r["ci_high"])
        col = ACC if lo > 0 else MUTE
        ax.plot([lo, hi], [i, i], color=col, lw=2.5)
        ax.plot(m, i, "o", color=col, ms=8)
    ax.axvline(0, color=INK, lw=1, ls="--")
    ax.set_yticks(range(len(rows)))
    ax.set_yticklabels([f"{NAMES.get(r['chair'], r['chair'])} as chair" for r in rows], fontsize=10)
    ax.set_xlabel("Extra weight on its own model vs other chairs (95% CI)")
    ax.set_title("Chairs over-weight their own model", fontsize=11, loc="left")
    _clean(ax)
    fig.tight_layout()
    fig.savefig(out, dpi=200, facecolor="white")
    plt.close(fig)
    return True


def main() -> None:
    OUT.mkdir(parents=True, exist_ok=True)
    for name, fn in (("council_vs_average", council_vs_average), ("reliability", reliability),
                     ("self_preference", self_preference)):
        path = OUT / f"{name}.png"
        print(f"{'saved' if fn(path) else 'skipped (no data yet)'}: {path.relative_to(ROOT)}")


if __name__ == "__main__":
    main()
