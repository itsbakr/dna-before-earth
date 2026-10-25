"""Exploratory: better no-trend null models for genome-size evolution on the real tree.

For animals and green plants (2015 Timetree pruned to GoaT species), fit Brownian motion and
Ornstein-Uhlenbeck by REML, measure the heavy-tailedness of the standardized contrasts, then compare the
observed Markov-style nested-minimum "clock" slopes with four trendless nulls simulated on the same tree:
Brownian motion, OU at the fitted pull, empirical heavy-tailed increments, and Brownian motion reflected
within the observed range. Writes results/nullmodels.json and figures/nullmodels.png.
"""

import json
import sys
from pathlib import Path

import numpy as np
from scipy import stats

ROOT = Path(__file__).resolve().parent.parent
sys.path.insert(0, str(ROOT))

from clock import phylo, realdata  # noqa: E402
from clock.plotting import COLORS, INK, INK2, MUTED, new_figure, style_axes  # noqa: E402

N_NULL = 20
SEED = 20261025
CLADES = [("Metazoa", 33208), ("Viridiplantae", 33090)]


def main():
    rng = np.random.default_rng(SEED)
    out, panels = {}, {}
    for name, tid in CLADES:
        tree, vals = realdata.pruned_genome_tree(tid)
        x = np.array(list(vals.values()))
        c, v = phylo.pic_contrasts(tree, vals)
        u = c / np.sqrt(v)
        shape = (u - u.mean()) / u.std()
        ou = phylo.fit_ou(tree, vals)
        s2_bm = ou["sigma2_bm"]
        obs = phylo.nested_min_fits(tree, vals)
        res = {"tips": len(vals), "root_age_myr": float(phylo.node_ages(tree)[tree.root]),
               "bm_sigma_log10_per_sqrt_gyr": float(np.sqrt(s2_bm * 1000)),
               "ou": {k: ou[k] for k in ("alpha_per_myr", "half_life_myr", "sigma2_per_myr", "loglik_ou",
                                         "loglik_bm", "delta_aic_bm_minus_ou")},
               "contrast_excess_kurtosis": float(stats.kurtosis(u)),
               "contrast_share_beyond_3sd": float(np.mean(np.abs(shape) > 3)),
               "observed": phylo.summarize_fits(*obs[1:])}
        theta, lo, hi = float(np.mean(x)), float(x.min()), float(x.max())
        sims = {
            "brownian": lambda: phylo.simulate_bm(tree, s2_bm, theta, rng),
            "ou_fitted": lambda: phylo.simulate_ou(tree, ou["alpha_per_myr"], ou["sigma2_per_myr"], theta, rng=rng),
            "heavy_tailed": lambda: phylo.simulate_empirical(tree, s2_bm, shape, theta, rng),
            "bounded": lambda: phylo.simulate_bounded(tree, s2_bm, lo, hi, theta, rng),
        }
        res["nulls"] = {}
        panels[name] = {"observed": obs[1]}
        for key, sim in sims.items():
            runs, slopes = [], []
            for _ in range(N_NULL):
                f = phylo.nested_min_fits(tree, sim())
                runs.append(phylo.summarize_fits(*f[1:]))
                slopes.append(f[1])
            meds = np.array([r["slope_median"] for r in runs])
            res["nulls"][key] = {
                "slope_median_median": float(np.median(meds)), "slope_median_range": [float(meds.min()), float(meds.max())],
                "r2_median_median": float(np.median([r["r2_median"] for r in runs])),
                "pre_earth_frac_median": float(np.median([r["pre_earth_frac"] for r in runs])),
                "share_runs_with_median_slope_at_least_observed":
                    float(np.mean(meds >= res["observed"]["slope_median"])),
                "tip_sd_median": None}
            panels[name][key] = np.concatenate(slopes)
        out[name] = res
    with open(ROOT / "results" / "nullmodels.json", "w") as fh:
        json.dump(out, fh, indent=2)
    figure(panels)
    print(json.dumps(out, indent=1))


def figure(panels):
    fig, axes = new_figure(12, 4.4, ncols=2)
    labels = {"brownian": "Brownian", "ou_fitted": "Ornstein-Uhlenbeck (fitted)",
              "heavy_tailed": "heavy-tailed jumps", "bounded": "bounded"}
    colors = {"brownian": MUTED, "ou_fitted": COLORS[1], "heavy_tailed": COLORS[2], "bounded": "#6250d6"}
    bins = np.linspace(-1, 6, 71)
    for ax, (name, title) in zip(axes, [("Metazoa", "A. Animals"), ("Viridiplantae", "B. Green plants")]):
        for key in ("brownian", "ou_fitted", "heavy_tailed", "bounded"):
            ax.hist(panels[name][key], bins=bins, density=True, histtype="step", lw=1.6,
                    color=colors[key], label=f"no trend: {labels[key]}")
        ax.hist(panels[name]["observed"], bins=bins, density=True, histtype="stepfilled", alpha=0.25,
                color=COLORS[0], label="observed genome sizes")
        ax.axvline(0, color=INK2, lw=1, ls=":")
        ax.set_xlabel("Nested-minimum 'clock rate' per focal species (log10/Gyr)")
        ax.set_ylabel("Density")
        ax.set_title(f"{title}: observed vs four trendless models", loc="left", fontsize=10.5, color=INK)
        ax.legend(loc="upper right", frameon=False, fontsize=8)
        style_axes(ax)
    fig.tight_layout()
    fig.savefig(ROOT / "figures" / "nullmodels.png", dpi=160)


if __name__ == "__main__":
    main()
