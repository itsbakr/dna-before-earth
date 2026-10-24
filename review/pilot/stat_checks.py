"""Independent checks of the genome-clock regressions (critique pilot)."""
import numpy as np
from scipy import stats
from scipy.optimize import curve_fit

def ols(x, y):
    n = len(x); X = np.column_stack([np.ones(n), x])
    beta, *_ = np.linalg.lstsq(X, y, rcond=None)
    resid = y - X @ beta; s2 = resid @ resid / (n - 2)
    cov = s2 * np.linalg.inv(X.T @ X)
    return beta, cov, s2, resid

def fieller_xint(x, y, level=0.95, y0=0.0):
    """CI for age t where the line reaches y0 (inverse prediction of the mean line)."""
    beta, cov, s2, _ = ols(x, y); n = len(x)
    tq = stats.t.ppf(0.5 + level / 2, n - 2)
    a, b = beta[0] - y0, beta[1]
    # solve (a + b t)^2 <= tq^2 * (vaa + 2 t vab + t^2 vbb)
    vaa, vab, vbb = cov[0, 0], cov[0, 1], cov[1, 1]
    A = b * b - tq**2 * vbb; B = 2 * (a * b - tq**2 * vab); C = a * a - tq**2 * vaa
    disc = B * B - 4 * A * C
    est = -a / b
    if A <= 0:
        return est, (np.nan, np.nan), "unbounded (slope not significant at this level)"
    r = sorted([(-B - np.sqrt(disc)) / (2 * A), (-B + np.sqrt(disc)) / (2 * A)])
    return est, tuple(r), "bounded"

def aicc(rss, n, k):
    aic = n * np.log(rss / n) + 2 * k
    return aic + 2 * k * (k + 1) / (n - k - 1) if n - k - 1 > 0 else np.inf

# t is time before present in Gyr (positive = past); model: log10 G = a - b t
sharov = dict(t=np.array([3.5, 2.0, 1.0, 0.5, 0.0]), y=np.log10([5e5, 2.9e6, 7.3e7, 1.3e8, 4.8e8]))
sharov125 = dict(t=np.array([3.5, 2.0, 1.0, 0.5, 0.125]), y=sharov["y"])
markov = dict(t=np.array([4.0, 2.0, 1.25, 0.575, 0.54, 0.375, 0.315, 0.22, 0.065]),
              y=np.log10(np.array([1.3, 9.2, 19.6, 68.6, 342, 931, 951, 1695, 2215]) * 1e6))

print("=" * 72); print("1. Point estimate and 95% inverse-prediction (Fieller) CI for 1 bp origin")
for name, d in [("Sharov, mammals@0", sharov), ("Sharov, mammals@0.125", sharov125), ("Markov 9-pt", markov)]:
    x = -d["t"]; y = d["y"]
    beta, cov, s2, _ = ols(x, y)
    r2 = 1 - np.sum((y - (beta[0] + beta[1] * x))**2) / np.sum((y - y.mean())**2)
    for lvl in (0.95, 0.99):
        est, ci, kind = fieller_xint(x, y, lvl)
        print(f"  {name:<24} R2={r2:.3f} origin={-est:5.2f} Gya  {int(lvl*100)}% CI = [{-ci[1]:.2f}, {-ci[0]:.2f}] Gya ({kind})")

print("=" * 72); print("2. AICc (small-sample) for Sharov 5-pt: linear vs quadratic vs 3-par logistic")
x = -sharov["t"]; y = sharov["y"]; n = len(x)
rss_lin = np.sum((y - np.polyval(np.polyfit(x, y, 1), x))**2)
rss_quad = np.sum((y - np.polyval(np.polyfit(x, y, 2), x))**2)
print(f"  linear k=3 (incl. sigma): AICc = {aicc(rss_lin, n, 3):.2f}")
print(f"  quadratic k=4:            AICc = {aicc(rss_quad, n, 4):.2f}  (n-k-1=0 -> undefined/inf)")
print(f"  logistic k=4:             AICc = inf (same reason). With n=5, no 3-parameter curve can be compared.")

print("=" * 72); print("3. Repo logistic fit: parameter sits on the bound L=15 (degenerate)")
def logistic(t, L, k, t0): return L / (1 + np.exp(-k * (t - t0)))
for upper in (15, 30, 60, 120):
    p, _ = curve_fit(logistic, x, y, p0=[9, 1.5, -2], bounds=([5, 0.01, -50], [upper, 10, 0]), maxfev=20000)
    t1 = p[2] - np.log(99) / p[1]
    print(f"  upper bound on L = {upper:>3}: L={p[0]:6.2f} k={p[1]:.3f}  '1% of L' origin = {-t1:6.2f} Gya")
print("  -> the 20.5 Gya figure is set by the arbitrary bound on L, not by the data.")
# Logistic with free floor (rapid early rise then saturation, i.e. Koonin-style)
def logistic4(t, lo, hi, k, t0): return lo + (hi - lo) / (1 + np.exp(-k * (t - t0)))
print("  4-par logistic with free floor has 4 params for 5 points: any origin date fits (non-identifiable).")

print("=" * 72); print("4. Leave-one-out on Markov 9-pt: how much does the origin move?")
x = -markov["t"]; y = markov["y"]
labels = ["Bacteria", "Eukaryotes", "Metazoa", "Chordates", "Vertebrates", "Tetrapods", "Amniotes", "Mammals", "Primates"]
for i in range(len(x)):
    m = np.ones(len(x), bool); m[i] = False
    b = np.polyfit(x[m], y[m], 1)
    print(f"  drop {labels[i]:<12} origin = {b[1]/b[0]:6.2f} Gya   slope = {b[0]:.3f} log10/Gyr")

print("=" * 72); print("5. Backcasting test: fit one segment, predict the other")
ph = markov["t"] <= 0.6
b_ph = np.polyfit(-markov["t"][ph], markov["y"][ph], 1)
print(f"  Phanerozoic-only (6 pts) slope = {b_ph[0]:.2f} log10/Gyr, origin = {b_ph[1]/b_ph[0]:.2f} Gya")
for t, yy, lab in zip(markov["t"][~ph], markov["y"][~ph], np.array(labels)[~ph]):
    pred = np.polyval(b_ph, -t)
    print(f"    predicts {lab:<11} at {t:.2f} Gya: 10^{pred:.2f} bp  (observed 10^{yy:.2f}; error {yy-pred:+.2f} orders of magnitude)")
pre = ~ph
b_pre = np.polyfit(-markov["t"][pre], markov["y"][pre], 1)
print(f"  Precambrian-only (3 pts) slope = {b_pre[0]:.2f} log10/Gyr, origin = {b_pre[1]/b_pre[0]:.2f} Gya")
print("  -> rate differs ~5x between segments; the origin is whatever rate you assume for the unobserved interval.")

print("=" * 72); print("6. Rate needed in the unobserved pre-LUCA interval")
for size_bp, age, lab in [(5e5, 3.5, "Sharov prokaryote"), (2.5e6, 4.2, "Moody 2024 LUCA (~2.5 Mb, ~4.2 Ga)")]:
    for start in (4.4, 4.5):
        dt = start - age
        rate = np.log10(size_bp) / dt
        print(f"  {lab}: origin at {start} Gya needs {rate:5.1f} log10/Gyr = {rate/0.877:5.1f}x Sharov's rate "
              f"(doubling every {np.log10(2)/rate*1000:.0f} Myr)")
print("  Repo's '3x faster' scenario (5.7 Gya) uses 3x; the multiplier is a free choice.")

print("=" * 72); print("7. Same constant-rate method on other complexity metrics (reductio)")
# gene count: LUCA ~2600 proteins at ~4.2 Ga (Moody 2024); human ~20,000 protein-coding genes
for lab, g0, t0, g1 in [("protein-coding genes (LUCA 2600 -> human 20000)", 2600, 4.2, 20000),
                        ("constrained DNA (LUCA ~2.3 Mb -> human ~330 Mb)", 2.3e6, 4.2, 3.3e8)]:
    rate = np.log10(g1 / g0) / t0
    origin = t0 + np.log10(g0) / rate
    print(f"  {lab}: rate {rate:.2f} log10/Gyr -> 'origin' at {origin:.1f} Gya (universe = 13.8)")
