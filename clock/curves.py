"""Alternative growth curves for log10 genome size against age, with AICc and the
implied age of a 1 bp genome where that age is finite.

All curves are fitted to y = log10(bp) by least squares; t is age in Gya.
"""

import numpy as np
from scipy.optimize import brentq, curve_fit

from .regression import aicc


def _exponential(t, a, b):
    return a - b * t


def _hyperbolic(t, logA, B):
    # Markov et al.'s hyperbolic form L = A / (B + T), on the log10 scale
    return logA - np.log10(B + t)


def _biexponential(t, y_inf, A, B):
    # Markov et al.'s biexponential form ln(L / C) = A exp(-B T), on the log10 scale
    return y_inf + A * np.exp(-B * t)


def _logistic4(t, lo, hi, k, t_mid):
    # S-curve in time running forward (t is age, so forward time is -t)
    return lo + (hi - lo) / (1 + np.exp(np.clip(-k * (-t - t_mid), -700, 700)))


CURVES = {
    "exponential": dict(f=_exponential, p0=[[9, 1]], bounds=([-np.inf, -np.inf], [np.inf, np.inf])),
    "hyperbolic": dict(f=_hyperbolic, p0=[[9, 0.1], [9, 1], [10, 5]], bounds=([-np.inf, 1e-6], [np.inf, 1e3])),
    "biexponential": dict(f=_biexponential, p0=[[5, 4, 1], [0, 9, 0.5], [6, 3, 2]],
                          bounds=([-50, 0, 1e-4], [20, 100, 50])),
    "logistic4": dict(f=_logistic4, p0=[[6, 10, 2, -1], [5, 9.5, 3, -0.5]],
                      bounds=([-10, 5, 1e-3, -20], [9, 30, 50, 5])),
}


def fit_curve(name, t, y):
    spec = CURVES[name]
    best = None
    for p0 in spec["p0"]:
        try:
            p, _ = curve_fit(spec["f"], t, y, p0=p0, bounds=spec["bounds"], maxfev=50000)
        except RuntimeError:
            continue
        rss = float(np.sum((y - spec["f"](t, *p)) ** 2))
        if best is None or rss < best["rss"]:
            best = {"params": [float(v) for v in p], "rss": rss}
    if best is None:
        return {"name": name, "converged": False}
    n, k = len(t), len(spec["p0"][0]) + 1
    best.update(name=name, converged=True, n=n, k=k, aicc=float(aicc(best["rss"], n, k)),
                origin_1bp=_origin(name, spec["f"], best["params"]),
                at_bounds=_at_bounds(best["params"], spec["bounds"]))
    return best


def _at_bounds(p, bounds, rel=1e-6):
    lo, hi = bounds
    return [bool(np.isfinite(l) and abs(v - l) <= rel * max(1, abs(l))) or
            bool(np.isfinite(h) and abs(v - h) <= rel * max(1, abs(h)))
            for v, l, h in zip(p, lo, hi)]


def _origin(name, f, p, t_max=1000.0):
    """Age at which the fitted curve first reaches log10(1 bp) = 0 going back; None if never."""
    if name == "exponential":
        return float(p[0] / p[1]) if p[1] > 0 else None
    g = lambda t: f(t, *p)
    grid = np.concatenate([np.linspace(0, 50, 5001), np.linspace(50, t_max, 2000)])
    vals = g(grid)
    idx = np.where(vals <= 0)[0]
    if len(idx) == 0 or idx[0] == 0:
        return None
    i = idx[0]
    return float(brentq(g, grid[i - 1], grid[i]))
