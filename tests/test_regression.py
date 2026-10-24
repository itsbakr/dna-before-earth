import numpy as np
import pytest

from clock import curves, data, regression as R


def test_ols_recovers_exact_line():
    t = np.array([4.0, 3.0, 2.0, 1.0, 0.0])
    f = R.ols(t, 9 - 0.9 * t)
    assert f["a"] == pytest.approx(9) and f["b"] == pytest.approx(0.9)
    assert R.origin(f["a"], f["b"]) == pytest.approx(10)


def test_sharov_replication_matches_printed_intercept():
    s = data.load_sharov()
    f = R.ols(s.t, s.y)
    assert f["a"] == pytest.approx(8.64, abs=0.01)     # Sharov: log10 y = 8.64 + 0.89 x
    assert f["b"] == pytest.approx(0.89, abs=0.01)


def test_fieller_interval_brackets_estimate():
    s = data.load_sharov()
    est, lo, hi = R.fieller_origin(s.t, s.y)
    assert lo < est < hi


def test_york_pearson_benchmark():
    # Pearson data with York (1966) weights; accepted solution slope -0.4805, intercept 5.4799
    X = np.array([0.0, 0.9, 1.8, 2.6, 3.3, 4.4, 5.2, 6.1, 6.5, 7.4])
    Y = np.array([5.9, 5.4, 4.4, 4.6, 3.5, 3.7, 2.8, 2.8, 2.4, 1.5])
    wX = np.array([1000, 1000, 500, 800, 200, 80, 60, 20, 1.8, 1])
    wY = np.array([1, 1.8, 4, 8, 20, 20, 70, 70, 100, 500])
    f = R.york(-X, Y, 1 / np.sqrt(wX), 1 / np.sqrt(wY))    # york() takes ages t = -x
    assert f["b"] == pytest.approx(-0.4805, abs=2e-4)
    assert f["a"] == pytest.approx(5.4799, abs=2e-4)


def test_deming_limits():
    s = data.load_sharov()
    ols = R.ols(s.t, s.y)
    assert R.deming(s.t, s.y, 0)["b"] == pytest.approx(ols["b"])
    assert R.deming(s.t, s.y, 1e-9)["b"] == pytest.approx(ols["b"], rel=1e-6)


def test_aicc_undefined_for_saturated_models():
    assert R.aicc(1.0, 5, 4) == np.inf


def test_biexponential_recovers_synthetic_parameters():
    t = np.linspace(0, 4, 9)
    y = 6.0 + 3.5 * np.exp(-0.8 * t)
    f = curves.fit_curve("biexponential", t, y)
    np.testing.assert_allclose(f["params"], [6.0, 3.5, 0.8], atol=1e-4)
    assert f["origin_1bp"] is None      # floors at 10^6 bp: never reaches 1 bp
