"""WP5 (exploratory): the unobserved interval before LUCA, and a reproduction of Marzban et al. (2014).

Part 1. Monte Carlo of the average growth rate a terrestrial origin requires, from the onset of habitability
to LUCA, with uncertainty in every input; compared with Sharov's fitted rate.
Part 2. Non-identifiability: the post-LUCA data do not depend on the pre-LUCA rate, so the inferred origin
date is the push-forward of whatever prior is placed on that rate. Shown for several priors.
Part 3. Marzban et al. 2014, eqs 5-9, applied to Sharov's points: where their prediction bands reach
log10(1 bp) = 0, as printed and with plausible alternative readings.

Writes results/wp5.json and figures/wp5.png.
"""

import json
import sys
from pathlib import Path

import numpy as np
from scipy import stats
from scipy.optimize import brentq

ROOT = Path(__file__).resolve().parent.parent
sys.path.insert(0, str(ROOT))

from clock import data, regression as R  # noqa: E402
from clock.plotting import COLORS, INK, INK2, MUTED, new_figure, style_axes  # noqa: E402

rng = np.random.default_rng(20261025)
N = 200_000
EARTH = 4.54


def part1():
    """Required average rate (log10 per Gyr) from a 1 bp (or 100 nt) start to LUCA."""
    luca_age = np.clip(rng.normal(4.21, 0.06, N), 4.09, 4.33)          # Moody et al. 2024: 4.09-4.33 Ga
    luca_bp = rng.uniform(2.49e6, 2.99e6, N)                            # Moody et al. 2024: 2.49-2.99 Mb
    start = rng.uniform(4.35, 4.50, N)                                  # liquid water by ~4.4 Ga; Moon >= 4.51 Ga
    ok = start > luca_age + 0.01
    out = {"inputs": {"luca_age_gya": "N(4.21, 0.06) truncated to 4.09-4.33 (Moody et al. 2024)",
                      "luca_genome_bp": "U(2.49e6, 2.99e6) (Moody et al. 2024)",
                      "habitability_onset_gya": "U(4.35, 4.50) (liquid water by about 4.4 Ga; Moon at least 4.51 Ga)"},
           "draws_used": int(ok.sum())}
    sharov_b = R.ols(*(lambda s: (s.t, s.y))(data.load_sharov()))["b"]
    for label, start_bp in [("from_1bp", 1.0), ("from_100nt", 100.0)]:
        rate = (np.log10(luca_bp[ok]) - np.log10(start_bp)) / (start[ok] - luca_age[ok])
        dbl = np.log10(2) / rate * 1000
        out[label] = {"rate_median": float(np.median(rate)),
                      "rate_95": [float(np.percentile(rate, 2.5)), float(np.percentile(rate, 97.5))],
                      "multiple_of_sharov_median": float(np.median(rate) / sharov_b),
                      "multiple_of_sharov_95": [float(np.percentile(rate, 2.5) / sharov_b),
                                                float(np.percentile(rate, 97.5) / sharov_b)],
                      "doubling_myr_median": float(np.median(dbl)),
                      "doubling_myr_95": [float(np.percentile(dbl, 2.5)), float(np.percentile(dbl, 97.5))]}
    out["sharov_rate"] = sharov_b
    out["comparison_rates_log10_per_gyr"] = {
        "sharov_average": sharov_b,
        "markov_minima_phanerozoic_segment": 2.57,
        "whole_genome_duplication": "+0.30 in one generation (doubling)"}
    return out, rate


def part2():
    """Origin date implied by different priors on the early-rate multiplier m (LUCA anchor)."""
    sharov_b = R.ols(*(lambda s: (s.t, s.y))(data.load_sharov()))["b"]
    y_luca, t_luca = np.log10(2.5e6), 4.2
    priors = {
        "m = 1 (Sharov's assumption)": np.ones(N),
        "log-uniform m in [0.1, 10]": 10 ** rng.uniform(-1, 1, N),
        "log-uniform m in [0.1, 100]": 10 ** rng.uniform(-1, 2, N),
        "log-uniform m in [1, 1000]": 10 ** rng.uniform(0, 3, N),
    }
    out = {}
    for name, m in priors.items():
        origin = t_luca + y_luca / (m * sharov_b)
        out[name] = {"origin_median_gya": float(np.median(origin)),
                     "p_origin_on_earth": float(np.mean(origin <= EARTH)),
                     "p_origin_older_than_universe": float(np.mean(origin > 13.8))}
    out["note"] = ("The likelihood of every post-LUCA observation is independent of m, so each row is "
                   "prior times a constant: the data cannot shift these probabilities.")
    return out


def part3():
    """Marzban et al. 2014 eqs 5-9 on Sharov's points (eukaryotes 2.05, mammals 0.125, as in their Fig. 2)."""
    t = np.array([3.5, 2.05, 1.0, 0.5, 0.125])
    y = data.load_sharov().y
    x = -t
    n = len(x)
    b, a = np.polyfit(x, y, 1)
    resid = y - (a + b * x)
    sxx = np.sum((x - x.mean()) ** 2)
    sigma_b2 = np.var(t, ddof=1)
    res = {"ols_slope": float(b), "ols_origin_gya": float(a / b), "sigma_b2": float(sigma_b2)}

    def crossing(lam, s2_eps, last_term_var, q=1.96):
        """Youngest age at which the lower edge of the 95% prediction band reaches y = 0."""
        Vb = s2_eps / sxx
        bl = b * lam
        al = y.mean() - bl * x.mean()
        Vbl = lam ** 2 * Vb + (b ** 2 + Vb) * (lam ** 2 - 1) ** 2 / n                      # eq. 8
        def lower(age):
            X = -age
            spe2 = s2_eps + s2_eps / n + (X - x.mean()) ** 2 * Vbl + (bl ** 2 + Vbl) * last_term_var   # eq. 9
            return al + bl * X - q * np.sqrt(spe2)
        return float(brentq(lower, 0.0, 60.0)) if lower(60.0) < 0 < lower(0.0) else None

    s2_n2 = np.sum(resid ** 2) / (n - 2)
    s2_n = np.sum(resid ** 2) / n
    tq = stats.t.ppf(0.975, n - 2)
    res["ols_band_crossing"] = {"z, SSR/(n-2)": crossing(1.0, s2_n2, 0.0),
                                "t(3 df), SSR/(n-2)": crossing(1.0, s2_n2, 0.0, q=tq),
                                "z, SSR/n": crossing(1.0, s2_n, 0.0),
                                "paper_fig2_reports": 7.0}
    sw2_for = lambda lam: (lam - 1) * sigma_b2
    res["lambda_1p14_crossing"] = {
        "eq9 as printed (last term x sigma_b^2)": crossing(1.14, s2_n2, sigma_b2),
        "last term x sigma_w^2": crossing(1.14, s2_n2, sw2_for(1.14)),
        "no last term": crossing(1.14, s2_n2, 0.0),
        "paper_text": "band includes 4.5; figure shows the red band reaching about 4.3 to 4.4"}
    lam_grid = np.round(np.arange(1.0, 3.01, 0.01), 2)
    for key, ltv in [("eq9 as printed", lambda lam: sigma_b2), ("last term x sigma_w^2", sw2_for)]:
        hit = [lam for lam in lam_grid if (c := crossing(lam, s2_n2, ltv(lam))) is not None and c <= 4.5]
        res.setdefault("smallest_lambda_band_reaches_4p5", {})[key] = float(hit[0]) if hit else None
    res["lambda_point_estimate_4p5"] = float(brentq(lambda lam: x.mean() - y.mean() / (b * lam) + 4.5, 1.0, 10.0))
    return res


def main():
    p1, rate_draws = part1()
    out = {"required_rate": p1, "prior_pushforward": part2(), "marzban_reproduction": part3()}
    with open(ROOT / "results" / "wp5.json", "w") as fh:
        json.dump(out, fh, indent=2)
    fig, ax = new_figure(6.6, 4.2)
    dbl = np.log10(2) / rate_draws * 1000
    ax.hist(dbl, bins=np.linspace(0, 60, 61), color=COLORS[0], alpha=0.8)
    sh = np.log10(2) / p1["sharov_rate"] * 1000
    ax.axvline(min(sh, 59), color=COLORS[1], lw=2)
    ax.text(min(sh, 59) - 1, ax.get_ylim()[1] * 0.9, f"Sharov's average:\nevery {sh:.0f} Myr (off scale)",
            ha="right", color=INK, fontsize=8.5)
    ax.set_xlabel("Genome doubling time needed from 100 nt to LUCA (Myr)")
    ax.set_ylabel("Monte Carlo draws")
    ax.set_title("What a terrestrial origin requires before LUCA", loc="left", fontsize=10.5, color=INK)
    style_axes(ax)
    fig.tight_layout()
    fig.savefig(ROOT / "figures" / "wp5.png", dpi=160)
    print(json.dumps(out, indent=1))


if __name__ == "__main__":
    main()
