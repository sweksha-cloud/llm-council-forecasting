"""analysis/figures.py builds every figure from the committed results."""

import pytest

pytest.importorskip("matplotlib")

from analysis import figures  # noqa: E402


def test_figures_build(tmp_path):
    assert figures.council_vs_average(tmp_path / "a.png")
    assert figures.reliability(tmp_path / "b.png")
    for name in ("a.png", "b.png"):
        assert (tmp_path / name).stat().st_size > 10_000


def test_chair_rows_have_intervals():
    rows = figures.chair_vs_mean_rows()
    assert rows and all(lo <= m <= hi for _, m, lo, hi, _ in rows)
