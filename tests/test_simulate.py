import numpy as np
import pytest

from clock import simulate as S

AGES = [2.0, 1.0, 0.5, 0.25, 0.1]


def _run(drift, seed=3, **kw):
    return S.branching_walk(2.0, 2.0, 0.5, AGES, drift=drift, rng=np.random.default_rng(seed), **kw)


def test_uniform_trend_is_invisible_to_nested_extremes():
    """Coupled runs: same random numbers, with and without a clock. Every extant value
    shifts by drift * T, so the nested-minimum series shifts by a constant and its slope
    is unchanged, while the true ancestral series picks up the drift."""
    a, b = _run(0.0), _run(0.8)
    np.testing.assert_allclose(b.traits - a.traits, 0.8 * 2.0, atol=1e-9)
    focal = 0
    na, nb = S.nested_series(a, focal), S.nested_series(b, focal)
    np.testing.assert_allclose(nb - na, 0.8 * 2.0, atol=1e-9)
    assert S.fit_line(AGES, nb)[0] == pytest.approx(S.fit_line(AGES, na)[0], abs=1e-9)
    anc_a, anc_b = S.ancestor_series(a, focal), S.ancestor_series(b, focal)
    slope_diff = S.fit_line(AGES, anc_b)[0] - S.fit_line(AGES, anc_a)[0]
    assert slope_diff == pytest.approx(0.8, abs=2e-3)    # checkpoints snap to the dt grid


def test_nested_minimum_is_monotone_by_construction():
    run = _run(0.0, seed=5)
    for focal in range(0, len(run.traits), max(1, len(run.traits) // 10)):
        s = S.nested_series(run, focal)
        assert np.all(np.diff(s) >= 0)    # older clades (earlier entries) can only have smaller minima


def test_floor_is_respected():
    run = _run(0.0, seed=7, floor=5.9, start=6.0)
    assert run.traits.min() >= 5.9


def test_extreme_speed_formula():
    assert S.extreme_speed(0.5, 2.0) == pytest.approx(1.0)
