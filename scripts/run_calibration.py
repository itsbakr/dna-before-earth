"""WP2: calibrate the Sharov/Markov construction on simulated histories where the truth is known.

Writes results/calibration.json, figures/invariance.png and figures/null_grid.png.
Parameter values are illustrative; WP3 will estimate sigma and diversification from real data.
"""

import json
import sys
from pathlib import Path

import numpy as np

ROOT = Path(__file__).resolve().parent.parent
sys.path.insert(0, str(ROOT))

from clock import data, regression as R, simulate as S  # noqa: E402
from clock.plotting import COLORS, INK, INK2, MUTED, new_figure, style_axes  # noqa: E402

MARKOV = data.load_markov()
AGES = MARKOV.t                    # Markov's clade ages, oldest first
T_ROOT, START, EARTH = 4.0, 6.0, 4.54
REPS = 25
SEED = 20261024


def run_many(n, rng, **kw):
    """Collect n surviving runs with at least 50 extant lineages."""
    runs = []
    while len(runs) < n:
        r = S.branching_walk(T_ROOT, rng=rng, checkpoints=AGES, start=START, **kw)
        if r is not None and len(r.traits) >= 50:
            runs.append(r)
    return runs


def summarize(runs, focal_mode, rng):
    slopes, r2s, origins, anc_slopes = [], [], [], []
    for r in runs:
        focal = int(np.argmax(r.traits)) if focal_mode == "max" else int(rng.integers(len(r.traits)))
        b, o, r2 = S.fit_line(AGES, S.nested_series(r, focal))
        slopes.append(b); origins.append(o); r2s.append(r2)
        anc_slopes.append(S.fit_line(AGES, S.ancestor_series(r, focal))[0])
    slopes, origins, r2s = np.array(slopes), np.array(origins), np.array(r2s)
    return {"runs": len(runs), "median_tips": int(np.median([len(r.traits) for r in runs])),
            "nested_slope_median": float(np.median(slopes)),
            "nested_slope_iqr": [float(np.percentile(slopes, 25)), float(np.percentile(slopes, 75))],
            "positive_slope_frac": float(np.mean(slopes > 0)),
            "r2_median": float(np.nanmedian(r2s)),
            "inferred_origin_median": float(np.median(origins)),
            "pre_earth_frac": float(np.mean(origins > EARTH)),
            "ancestor_slope_median": float(np.median(anc_slopes))}


def main():
    rng = np.random.default_rng(SEED)
    obs = R.ols(MARKOV.t, MARKOV.y)
    out = {"settings": {"root_age_gya": T_ROOT, "start_log10_bp": START, "reps": REPS,
                        "checkpoint_ages": AGES.tolist(), "seed": SEED,
                        "true_origin_gya": T_ROOT},
           "observed_markov": {"slope": obs["b"], "r2": obs["r2"]}}

    # E1: coupled runs with and without a uniform clock (identical random numbers)
    pair = {}
    for drift in (0.0, 0.8):
        r = S.branching_walk(T_ROOT, 2.5, 0.5, AGES, drift=drift, start=START,
                             rng=np.random.default_rng(7))
        pair[drift] = r
    focal = int(np.random.default_rng(1).integers(len(pair[0.0].traits)))
    e1 = {}
    for drift, r in pair.items():
        nested, anc = S.nested_series(r, focal), S.ancestor_series(r, focal)
        e1[str(drift)] = {"nested": nested.tolist(), "ancestor": anc.tolist(),
                          "nested_fit": S.fit_line(AGES, nested), "ancestor_fit": S.fit_line(AGES, anc)}
    out["invariance"] = e1

    # E2: null grid (no trend)
    grid = []
    for sigma in (0.25, 0.5, 0.75, 1.0):
        for lam in (1.5, 2.0, 2.5):
            runs = run_many(REPS, rng, lam=lam, sigma=sigma)
            for mode in ("random", "max"):
                grid.append({"sigma": sigma, "lam": lam, "mu": 0.0, "focal": mode,
                             "theory_speed": float(S.extreme_speed(sigma, lam)),
                             **summarize(runs, mode, rng)})
    runs = run_many(REPS, rng, lam=4.0, mu=1.5, sigma=0.5)
    for mode in ("random", "max"):
        grid.append({"sigma": 0.5, "lam": 4.0, "mu": 1.5, "focal": mode,
                     "theory_speed": float(S.extreme_speed(0.5, 2.5)), **summarize(runs, mode, rng)})
    out["null_grid"] = grid

    # E3: reflecting floor (minimum viable genome ~300 kb)
    runs = run_many(REPS, rng, lam=2.5, sigma=0.5, floor=5.5)
    out["null_floor"] = {mode: summarize(runs, mode, rng) for mode in ("random", "max")}

    # E4: true clock of different strengths; does each method recover it?
    trend = []
    for drift in (0.0, 0.4, 0.8, 1.2):
        runs = run_many(REPS, rng, lam=2.5, sigma=0.5, drift=drift)
        trend.append({"true_drift": drift, **summarize(runs, "random", rng)})
    out["trend_recovery"] = trend

    (ROOT / "results").mkdir(exist_ok=True)
    (ROOT / "figures").mkdir(exist_ok=True)
    with open(ROOT / "results" / "calibration.json", "w") as fh:
        json.dump(out, fh, indent=2)
    figure_invariance(out)
    figure_grid(out)
    print("wrote results/calibration.json, figures/invariance.png, figures/null_grid.png")


def figure_invariance(out):
    fig, axes = new_figure(11.5, 4.2, ncols=2)
    for ax, key, title in [(axes[0], "nested", "A. Markov's method: minimum genome in each ancestral clade"),
                           (axes[1], "ancestor", "B. What actually happened: the ancestor's genome")]:
        for drift, color, lab in [("0.0", COLORS[0], "no clock"), ("0.8", COLORS[1], "clock: +0.8 log10 per Gyr")]:
            v = out["invariance"][drift]
            b = v[f"{key}_fit"][0]
            ax.plot(AGES, v[key], color=color, lw=2, marker="o", ms=5,
                    label=f"{lab}  (fitted slope {b:.2f})")
        ax.set_xlim(4.2, -0.1)
        ax.set_xlabel("Clade age (Gya)")
        ax.set_ylabel("log10 genome size (bp)")
        ax.set_title(title, loc="left", fontsize=10.5, color=INK)
        ax.legend(loc="lower right" if key == "nested" else "upper left", frameon=False, fontsize=9)
        style_axes(ax)
    axes[0].text(4.1, axes[0].get_ylim()[1] - 0.2,
                 "Same simulated history, same random numbers.\nThe clock only shifts every living genome\n"
                 "by the same amount, so the slope is identical.",
                 fontsize=8.5, color=INK2, va="top")
    fig.tight_layout()
    fig.savefig(ROOT / "figures" / "invariance.png", dpi=160)


def figure_grid(out):
    fig, ax = new_figure(6.4, 4.4)
    rows = [g for g in out["null_grid"] if g["focal"] == "random"]
    x = np.array([g["theory_speed"] for g in rows])
    y = np.array([g["nested_slope_median"] for g in rows])
    lo = np.array([g["nested_slope_iqr"][0] for g in rows])
    hi = np.array([g["nested_slope_iqr"][1] for g in rows])
    ax.errorbar(x, y, yerr=[y - lo, hi - y], fmt="o", color=COLORS[0], ms=6, lw=1.2, capsize=0,
                label="no-clock simulations (median, IQR)")
    lim = max(x.max(), hi.max()) * 1.05
    ax.plot([0, lim], [0, lim], color=MUTED, lw=1, ls=":")
    ax.text(2.0, 2.2, "theory (infinite clade)", color=INK2, fontsize=8.5, ha="right")
    obs = out["observed_markov"]["slope"]
    ax.axhline(obs, color=COLORS[1], lw=2)
    ax.text(0.05, obs + 0.04, f"observed Markov slope {obs:.2f}", color=INK, fontsize=9)
    ax.set_xlim(0, lim)
    ax.set_ylim(0, lim)
    ax.set_xlabel("Extreme-value speed σ·√(2r) (log10 per Gyr)")
    ax.set_ylabel("Fitted 'clock rate' with no clock (log10 per Gyr)")
    ax.set_title("With no trend at all, the method still reports a clock rate", loc="left",
                 fontsize=10.5, color=INK)
    ax.legend(loc="upper left", frameon=False, fontsize=9, bbox_to_anchor=(0, 0.93))
    style_axes(ax)
    fig.tight_layout()
    fig.savefig(ROOT / "figures" / "null_grid.png", dpi=160)


if __name__ == "__main__":
    main()
