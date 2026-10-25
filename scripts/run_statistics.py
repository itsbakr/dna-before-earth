"""WP0/WP1: exact replication and proper statistics on the published datasets.

Writes results/statistics.json and figures/early_rate.png, figures/curves.png.
Every number in results/RESULTS.md is generated from the JSON written here.
"""

import json
import sys
from pathlib import Path

import numpy as np
from scipy import stats
from scipy.optimize import brentq

ROOT = Path(__file__).resolve().parent.parent
sys.path.insert(0, str(ROOT))

from clock import curves, data, early_rate as E, regression as R  # noqa: E402
from clock.plotting import COLORS, INK, INK2, MUTED, style_axes, new_figure  # noqa: E402

EARTH_GYA, UNIVERSE_GYA = 4.54, 13.8
rng = np.random.default_rng(20261024)


def line_summary(series):
    f = R.ols(series.t, series.y)
    est, lo95, hi95 = R.fieller_origin(series.t, series.y, 0.95)
    _, lo99, hi99 = R.fieller_origin(series.t, series.y, 0.99)
    return {"n": f["n"], "a": f["a"], "b": f["b"], "r2": f["r2"], "p": f["p"],
            "fold_per_gyr": 10 ** f["b"], "doubling_myr": float(E.doubling_time_myr(f["b"])),
            "origin_1bp": est, "fieller95": [lo95, hi95], "fieller99": [lo99, hi99]}


def york_summary(series):
    y = R.york(series.t, series.y, series.t_sd, series.y_sd)
    dof = len(series.t) - 2
    chi2 = y["reduced_chi2"] * dof
    return {**y, "origin_1bp": y["a"] / y["b"], "chi2": chi2, "dof": dof,
            "p_line_fits": float(stats.chi2.sf(chi2, dof))}


def mom_origin(t, y, age_err_sd):
    """Method-of-moments (attenuation-corrected) slope with known age-error variance."""
    x = -t
    sxx = np.var(x)
    sxy = np.mean((x - x.mean()) * (y - y.mean()))
    b = sxy / (sxx - age_err_sd ** 2)
    a = y.mean() - b * x.mean()
    return a / b, b, sxx / (sxx - age_err_sd ** 2)


def main():
    out = {}
    sharov, markov, markov_now, ext = (data.load_sharov(), data.load_markov("published"),
                                       data.load_markov("current"), data.load_extended())

    # --- 1. Replication -------------------------------------------------------------
    reprint = data.load_sharov("markov_reprint")
    legacy = reprint.subset(np.ones(5, bool))
    legacy.t = legacy.t.copy()
    legacy.t[-1] = 0.0
    out["replication"] = {
        "sharov_printed": {"a": 8.64, "b": 0.89, "r2": 0.97, "fold_per_gyr": 7.8},
        "sharov_figure_ages": line_summary(sharov),
        "sharov_markov_reprint_ages": line_summary(reprint),
        "sharov_mammals_0_legacy_repo": line_summary(legacy),
        "markov_published_ages": line_summary(markov),
        "markov_current_ages": line_summary(markov_now),
        "extended_corrected": line_summary(ext),
        "markov_published_r": {"exponential": 0.914, "biexponential": 0.979,
                               "note": "Markov et al. 2010 report Pearson r (labelled R2); r^2 = R^2"},
    }

    # --- 2. Errors in variables ----------------------------------------------------------
    deming_grid = [0, 0.1, 0.5, 1, 2, 5, 1e6]
    dem = [R.deming(sharov.t, sharov.y, r) for r in deming_grid]
    req_sd = brentq(lambda u: mom_origin(sharov.t, sharov.y, u)[0] - 4.5, 0.01, 1.2)
    lam = mom_origin(sharov.t, sharov.y, req_sd)[2]
    var_n, var_n1 = np.var(sharov.t), np.var(sharov.t, ddof=1)
    out["errors_in_variables"] = {
        "york_sharov": york_summary(sharov),
        "york_markov": york_summary(markov),
        "deming_sharov": [{"ratio": r, "b": d["b"], "origin_1bp": d["a"] / d["b"]}
                          for r, d in zip(deming_grid, dem)],
        "attenuation_route_sharov": {
            "age_error_sd_for_origin_4p5": req_sd,
            "reliability_factor_at_that_sd": lam,
            "age_error_sd_consistent_n": float(np.sqrt(var_n * (1 - 1 / lam))),
            "age_error_sd_consistent_n1": float(np.sqrt(var_n1 * (1 - 1 / lam))),
            "age_error_sd_marzban_eq6": float(np.sqrt((lam - 1) * 1.86)),
            "sd_of_observed_dates": float(np.sqrt(var_n1)),
            "marzban_lambda_at_sigma_w_0p5": float(1 + 0.5 ** 2 / 1.86),
            "grid": [{"age_error_sd": u, "origin_1bp": mom_origin(sharov.t, sharov.y, u)[0]}
                     for u in (0, 0.3, 0.5, 0.7, 0.9, 1.0)],
        },
    }

    # --- 3. Curve forms on Markov --------------------------------------------------------
    out["curves"] = {lab: {name: curves.fit_curve(name, s.t, s.y) for name in curves.CURVES}
                     for lab, s in (("published", markov), ("current", markov_now))}
    out["broken_stick"] = {"published": R.broken_stick(markov.t, markov.y),
                           "current": R.broken_stick(markov_now.t, markov_now.y)}

    # --- 4. Rate constancy: leave-one-out, backcasting, segments -------------------------
    loo = R.leave_one_out(markov.t, markov.y)
    for row in loo:
        row["group"] = markov.groups[row["dropped"]]
    phan = markov.t <= 0.6
    bc = R.backcast(markov.t, markov.y, phan)
    pre = R.ols(markov.t[~phan], markov.y[~phan])
    out["rate_constancy"] = {
        "leave_one_out": loo,
        "phanerozoic_fit": {"b": bc["b"], "origin_1bp": bc["origin"],
                            "predictions": [{"group": g, "t": float(t), "observed": float(o),
                                             "predicted": float(p), "error_log10": float(e)}
                                            for g, t, o, p, e in zip(np.array(markov.groups)[~phan],
                                                                     bc["test_t"], bc["test_y"],
                                                                     bc["pred"], bc["error_log10"])]},
        "precambrian_fit": {"b": pre["b"], "origin_1bp": R.origin(pre["a"], pre["b"])},
    }

    # --- 5. The unobserved early interval ------------------------------------------------
    sh, mk = out["replication"]["sharov_figure_ages"], out["replication"]["markov_published_ages"]
    anchors = {
        "sharov_first_point": (sharov.t[0], sharov.y[0], sh["b"]),
        "markov_first_point": (markov.t[0], markov.y[0], mk["b"]),
        "luca_moody2024": (4.2, np.log10(2.5e6), sh["b"]),
    }
    out["early_rate"] = {
        name: {"t_first": float(t0), "y_first": float(y0), "b": float(b),
               "required_multiplier_origin_4p4": float(E.required_multiplier(t0, y0, b, 4.4)),
               "required_multiplier_origin_4p5": float(E.required_multiplier(t0, y0, b, 4.5)),
               "doubling_myr_at_4p4": float(E.doubling_time_myr(E.required_multiplier(t0, y0, b, 4.4) * b))}
        for name, (t0, y0, b) in anchors.items()}
    seg_ratio = [out["rate_constancy"]["precambrian_fit"]["b"] / mk["b"],
                 out["rate_constancy"]["phanerozoic_fit"]["b"] / mk["b"]]
    out["early_rate"]["observed_segment_rate_ratios_markov"] = seg_ratio

    # --- 6. Age uncertainty with current dates -------------------------------------------
    lo, hi = data.current_age_ranges(markov.groups)
    origins = []
    for _ in range(20000):
        t = rng.uniform(lo, hi)
        f = R.ols(t, markov.y)
        origins.append(R.origin(f["a"], f["b"]))
    origins = np.array(origins)
    out["current_age_sampling"] = {"n": len(origins), "median": float(np.median(origins)),
                                   "p2_5": float(np.percentile(origins, 2.5)),
                                   "p97_5": float(np.percentile(origins, 97.5))}

    # --- 7. Same method on other complexity metrics (literature inputs) -----------------
    metrics = {
        "protein_coding_genes": {"luca": 2600, "human": 20000, "luca_age": 4.2,
                                 "sources": "LUCA ~2,600 proteins (Moody et al. 2024); human ~20,000 genes"},
        "constrained_dna_bp": {"luca": 2.3e6, "human": 3.32e8, "luca_age": 4.2,
                               "sources": "LUCA >=2.5 Mb mostly coding, ~2.3 Mb assumed functional; "
                                          "human 10.7% constrained, ~332 Mb (Zoonomia 2023)"},
    }
    for v in metrics.values():
        rate = np.log10(v["human"] / v["luca"]) / v["luca_age"]
        v["rate_log10_per_gyr"] = float(rate)
        v["origin_of_one_unit_gya"] = float(v["luca_age"] + np.log10(v["luca"]) / rate)
    out["metric_reductio"] = metrics

    (ROOT / "results").mkdir(exist_ok=True)
    (ROOT / "figures").mkdir(exist_ok=True)
    with open(ROOT / "results" / "statistics.json", "w") as fh:
        json.dump(out, fh, indent=2, default=_jsonable)
    figure_early_rate(sharov, markov, out)
    figure_curves(markov, out)
    print("wrote results/statistics.json, figures/early_rate.png, figures/curves.png")


def _jsonable(o):
    if isinstance(o, np.ndarray):
        return o.tolist()
    if isinstance(o, (np.floating, np.integer)):
        return o.item()
    if isinstance(o, np.bool_):
        return bool(o)
    raise TypeError(type(o))


def figure_early_rate(sharov, markov, out):
    fig, ax = new_figure(6.8, 4.4)
    m = np.logspace(-1, 2, 400)
    for s, key, color, label in [(sharov, "sharov_figure_ages", COLORS[0], "Sharov 2006 (5 pts)"),
                                 (markov, "markov_published_ages", COLORS[1], "Markov et al. 2010 (9 pts)")]:
        b = out["replication"][key]["b"]
        ax.plot(m, E.origin_given_multiplier(s.t[0], s.y[0], b, m), color=color, lw=2, label=label)
    lo, hi = out["early_rate"]["observed_segment_rate_ratios_markov"]
    ax.axvspan(lo, hi, color="#eceae4", zorder=0)
    ax.text(np.sqrt(lo * hi), 27, "rate ratios seen\nbetween segments\nof the record", ha="center",
            color=INK2, fontsize=8.5)
    ax.axvline(1, color=MUTED, lw=1, ls=":")
    ax.text(1.06, 1.2, "m = 1: early rate equals\nthe fitted average", color=INK2, fontsize=8.5)
    for yv, txt in [(EARTH_GYA, "Earth forms (4.54)"), (UNIVERSE_GYA, "Big Bang (13.8)")]:
        ax.axhline(yv, color=MUTED, lw=1, ls="--")
        ax.text(0.11, yv + 0.4, txt, color=INK2, fontsize=8.5, ha="left")
    ax.set_xscale("log")
    ax.set_ylim(0, 32)
    ax.legend(loc="upper right", frameon=False, fontsize=9)
    ax.set_xlabel("Assumed early rate ÷ fitted rate (m)")
    ax.set_ylabel("Implied origin of a 1 bp genome (Gya)")
    ax.set_title("The data fix the fitted rate; the origin is set by the assumed early rate",
                 loc="left", fontsize=10.5, color=INK)
    style_axes(ax)
    fig.tight_layout()
    fig.savefig(ROOT / "figures" / "early_rate.png", dpi=160)


def figure_curves(markov, out):
    fig, ax = new_figure(6.8, 4.4)
    tt = np.linspace(0, 12, 600)
    fits = out["curves"]["published"]
    for name, color, label in [("exponential", COLORS[0], "Straight line (the clock)"),
                               ("biexponential", COLORS[1], "Markov et al.'s biexponential"),
                               ]:
        f = fits[name]
        ax.plot(tt, curves.CURVES[name]["f"](tt, *f["params"]), color=color, lw=2)
        o = f["origin_1bp"]
        lab = f"{label}\nAICc {f['aicc']:.1f}, origin " + (f"{o:.1f} Gya" if o else "none")
        yl = curves.CURVES[name]["f"](9.0, *f["params"])
        ax.annotate(lab, xy=(9.0, yl), xytext=(0, 10 if name == "biexponential" else -28),
                    textcoords="offset points", color=INK, fontsize=8.5, ha="center")
    ax.scatter(markov.t, markov.y, s=40, color=INK, zorder=5, edgecolor="white", linewidth=1.2)
    ax.axvline(EARTH_GYA, color=MUTED, lw=1, ls="--")
    ax.text(EARTH_GYA + 0.1, 0.4, "Earth forms", color=INK2, fontsize=8.5)
    ax.set_xlim(12, -0.2)
    ax.set_ylim(0, 10)
    ax.set_xlabel("Age (Gya)")
    ax.set_ylabel("log10 minimal genome size (bp)")
    ax.set_title("Markov's data: the best-fitting curve levels off and never reaches 1 bp",
                 loc="left", fontsize=10.5, color=INK)
    style_axes(ax)
    fig.tight_layout()
    fig.savefig(ROOT / "figures" / "curves.png", dpi=160)


if __name__ == "__main__":
    main()
