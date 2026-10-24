"""Straight-line clock fits: OLS, inverse prediction, errors-in-variables, diagnostics.

The model is ``y = a - b * t`` (see ``clock/__init__.py``). Internally the
regressions use ``x = -t`` so that ordinary slope formulas apply.
"""

import numpy as np
from scipy import stats


def ols(t, y):
    t, y = np.asarray(t, float), np.asarray(y, float)
    n = len(t)
    X = np.column_stack([np.ones(n), -t])
    beta, *_ = np.linalg.lstsq(X, y, rcond=None)
    resid = y - X @ beta
    rss = float(resid @ resid)
    s2 = rss / (n - 2)
    cov = s2 * np.linalg.inv(X.T @ X)
    r2 = 1 - rss / float(np.sum((y - y.mean()) ** 2))
    tstat = beta[1] / np.sqrt(cov[1, 1])
    p = 2 * stats.t.sf(abs(tstat), n - 2)
    return {"a": float(beta[0]), "b": float(beta[1]), "cov": cov, "rss": rss,
            "resid_sd": float(np.sqrt(s2)), "r2": float(r2), "p": float(p), "n": n}


def origin(a, b, y0=0.0):
    """Age (Gya) at which the line y = a - b t reaches y0."""
    return (a - y0) / b


def fieller_origin(t, y, level=0.95, y0=0.0):
    """Point estimate and Fieller interval for the age at which the fitted line reaches y0.

    Returns (estimate, low, high). low/high are nan when the interval is unbounded
    (the slope is not significantly different from zero at this level).
    """
    fit = ols(t, y)
    a, b, cov = fit["a"] - y0, fit["b"], fit["cov"]
    q = stats.t.ppf(0.5 + level / 2, fit["n"] - 2)
    # Ages s satisfying (a - b s)^2 <= q^2 Var(a - b s)
    A = b * b - q * q * cov[1, 1]
    B = -2 * (a * b - q * q * cov[0, 1])
    C = a * a - q * q * cov[0, 0]
    est = a / b
    disc = B * B - 4 * A * C
    if A <= 0 or disc < 0:
        return est, np.nan, np.nan
    r = np.sqrt(disc)
    return est, (-B - r) / (2 * A), (-B + r) / (2 * A)


def york(t, y, t_sd, y_sd, tol=1e-12, max_iter=1000):
    """York et al. (2004) straight-line fit with errors in both variables (uncorrelated).

    Returns dict with a, b (clock convention) and their standard errors.
    """
    x, y = -np.asarray(t, float), np.asarray(y, float)
    wx, wy = 1 / np.asarray(t_sd, float) ** 2, 1 / np.asarray(y_sd, float) ** 2
    slope = np.polyfit(x, y, 1)[0]
    for _ in range(max_iter):
        W = wx * wy / (wx + slope * slope * wy)
        xbar, ybar = np.sum(W * x) / W.sum(), np.sum(W * y) / W.sum()
        U, V = x - xbar, y - ybar
        beta = W * (U / wy + slope * V / wx)
        new = np.sum(W * beta * V) / np.sum(W * beta * U)
        if abs(new - slope) < tol:
            slope = new
            break
        slope = new
    W = wx * wy / (wx + slope * slope * wy)
    xbar, ybar = np.sum(W * x) / W.sum(), np.sum(W * y) / W.sum()
    U, V = x - xbar, y - ybar
    beta = W * (U / wy + slope * V / wx)
    intercept = ybar - slope * xbar
    xadj = xbar + beta
    u = xadj - np.sum(W * xadj) / W.sum()
    sb = np.sqrt(1 / np.sum(W * u * u))
    sa = np.sqrt(1 / W.sum() + (np.sum(W * xadj) / W.sum()) ** 2 * sb * sb)
    chi2 = float(np.sum(W * (y - slope * x - intercept) ** 2))
    return {"a": float(intercept), "b": float(slope), "a_se": float(sa), "b_se": float(sb),
            "reduced_chi2": chi2 / (len(x) - 2)}


def deming(t, y, ratio):
    """Deming regression. ``ratio`` = (age-error variance) / (log-size-error variance),
    in units of Gyr^2 per (log10)^2. ratio -> 0 recovers OLS of y on t.
    """
    x, y = -np.asarray(t, float), np.asarray(y, float)
    sxx = np.mean((x - x.mean()) ** 2)
    syy = np.mean((y - y.mean()) ** 2)
    sxy = np.mean((x - x.mean()) * (y - y.mean()))
    if ratio == 0:
        b = sxy / sxx
    else:
        d = 1.0 / ratio          # error-variance ratio y over x
        b = (syy - d * sxx + np.sqrt((syy - d * sxx) ** 2 + 4 * d * sxy ** 2)) / (2 * sxy)
    a = y.mean() - b * x.mean()
    return {"a": float(a), "b": float(b)}


def aicc(rss, n, k):
    """Small-sample AIC for a Gaussian least-squares fit; k counts sigma too. inf when undefined."""
    if n - k - 1 <= 0:
        return np.inf
    return n * np.log(rss / n) + 2 * k + 2 * k * (k + 1) / (n - k - 1)


def leave_one_out(t, y, y0=0.0):
    """Origin estimate with each point dropped in turn."""
    out = []
    for i in range(len(t)):
        m = np.arange(len(t)) != i
        f = ols(t[m], y[m])
        out.append({"dropped": i, "b": f["b"], "origin": origin(f["a"], f["b"], y0)})
    return out


def backcast(t, y, train_mask, y0=0.0):
    """Fit on train_mask points, predict the rest. Returns fit and per-point prediction errors."""
    train_mask = np.asarray(train_mask, bool)
    f = ols(t[train_mask], y[train_mask])
    pred = f["a"] - f["b"] * t[~train_mask]
    return {"b": f["b"], "origin": origin(f["a"], f["b"], y0),
            "test_t": t[~train_mask], "test_y": y[~train_mask], "pred": pred,
            "error_log10": y[~train_mask] - pred}


def broken_stick(t, y, breaks=None):
    """Two-segment continuous line in t with the breakpoint chosen by least squares.

    Returns the best breakpoint, both slopes and the AICc comparison with one line.
    """
    t, y = np.asarray(t, float), np.asarray(y, float)
    n = len(t)
    if breaks is None:
        ts = np.sort(t)
        breaks = np.linspace(ts[1], ts[-2], 200)
    best = None
    for c in breaks:
        X = np.column_stack([np.ones(n), -t, -np.maximum(t - c, 0)])
        beta, *_ = np.linalg.lstsq(X, y, rcond=None)
        rss = float(np.sum((y - X @ beta) ** 2))
        if best is None or rss < best["rss"]:
            best = {"break_gya": float(c), "rss": rss,
                    "rate_young": float(beta[1]), "rate_old": float(beta[1] + beta[2])}
    one = ols(t, y)
    best["aicc_two_segment"] = float(aicc(best["rss"], n, 4))   # a, b1, b2, sigma (+break)
    best["aicc_two_segment_with_break_param"] = float(aicc(best["rss"], n, 5))
    best["aicc_one_line"] = float(aicc(one["rss"], n, 3))
    return best
