import pytest

from analysis.power import mde, n_needed


def test_mde_and_n_needed():
    # 2.8016 * 0.2 / sqrt(400) = 0.028016
    assert mde(0.2, 400) == pytest.approx(0.028016, abs=1e-5)
    assert mde(0.2, 400, design_effect=4) == pytest.approx(2 * 0.028016, abs=1e-5)
    # (2.8016 * 0.2 / 0.02)^2 = 784.9 -> 785
    assert n_needed(0.2, 0.02) == 785
