"""WP4b decision rules, as pre-registered in prereg/WP4_preregistration.md (Section 5).

Genome sizes estimated from fossils (data/fossil_genome_size.csv). Extant calibration species are excluded.
F1: per lineage group (>= 5 fossil taxa spanning >= 50 Myr), OLS of log10 genome size on age; consistent
    with H1 if the rate (growth toward the present) has a 95% CI above 0 that includes 0.89 log10/Gyr.
F2: pooled model with lineage-group intercepts and one common rate; same criterion.
F3: H1 predicts a positive rate in every qualifying group.
Writes results/fossils.json and figures/fossils.png.
"""

import json
import re
import sys
from pathlib import Path

import numpy as np
import pandas as pd
from scipy import stats

ROOT = Path(__file__).resolve().parent.parent
sys.path.insert(0, str(ROOT))

from clock.plotting import COLORS, INK, INK2, MUTED, new_figure, style_axes  # noqa: E402

SHAROV_RATE = 0.89
PALETTE = COLORS + ["#eda100", "#e87ba4", "#008300", "#6250d6", "#e34948"]


def load():
    df = pd.read_csv(ROOT / "data" / "fossil_genome_size.csv")
    df["extant_calibration"] = df["extant_calibration"].astype(str).str.upper().isin(["TRUE", "1", "YES"])
    fos = df[~df.extant_calibration].copy()
    fos["age_gyr"] = pd.to_numeric(fos.age_ma, errors="coerce") / 1000
    fos["pg"] = pd.to_numeric(fos.genome_size_pg, errors="coerce")
    rel = fos.notes.astype(str).str.extract(r"relative_proxy\s*=\s*(-?[0-9.]+)", flags=re.I)[0]
    fos["relative_proxy"] = pd.to_numeric(rel, errors="coerce")
    return df, fos


def fit(t, y):
    """Rate = growth toward the present, i.e. minus the slope of y on age."""
    n = len(t)
    X = np.column_stack([np.ones(n), -t])
    beta, *_ = np.linalg.lstsq(X, y, rcond=None)
    resid = y - X @ beta
    s2 = resid @ resid / (n - 2)
    se = np.sqrt(s2 * np.linalg.inv(X.T @ X)[1, 1])
    q = stats.t.ppf(0.975, n - 2)
    mde = (q + stats.t.ppf(0.80, n - 2)) * se          # rate detectable with 80% power
    return {"n": int(n), "rate": float(beta[1]), "ci95": [float(beta[1] - q * se), float(beta[1] + q * se)],
            "se": float(se), "min_detectable_rate_80pct_power": float(mde),
            "consistent_with_H1": bool(beta[1] - q * se > 0 and beta[1] - q * se <= SHAROV_RATE <= beta[1] + q * se)}


def main():
    raw, fos = load()
    out = {"rows_total": int(len(raw)), "rows_extant_calibration_excluded": int(raw.extant_calibration.sum()),
           "groups": {}, "relative_proxy_groups": {}}
    absolute = fos.dropna(subset=["age_gyr", "pg"])
    absolute = absolute[absolute.pg > 0]
    qualifying = []
    for g, d in absolute.groupby("lineage_group"):
        span_myr = (d.age_gyr.max() - d.age_gyr.min()) * 1000
        row = {"n_fossil_taxa": int(len(d)), "age_span_myr": float(span_myr),
               "age_range_ma": [float(d.age_gyr.min() * 1000), float(d.age_gyr.max() * 1000)]}
        if len(d) >= 5 and span_myr >= 50:
            row.update(fit(d.age_gyr.to_numpy(), np.log10(d.pg.to_numpy())))
            qualifying.append(g)
        out["groups"][g] = row
    for g, d in fos.dropna(subset=["age_gyr", "relative_proxy"]).groupby("lineage_group"):
        if len(d) >= 5:
            r = fit(d.age_gyr.to_numpy(), d.relative_proxy.to_numpy())
            out["relative_proxy_groups"][g] = {"n": r["n"], "rate_sign": int(np.sign(r["rate"])),
                                               "rate": r["rate"], "ci95": r["ci95"],
                                               "note": "relative units; sign only (pre-registered)"}
    # F2: pooled common rate with group intercepts
    q = absolute[absolute.lineage_group.isin(qualifying)]
    if len(qualifying) >= 1 and len(q) > len(qualifying) + 1:
        groups = sorted(qualifying)
        X = np.column_stack([(q.lineage_group == g).astype(float) for g in groups] + [-q.age_gyr.to_numpy()])
        y = np.log10(q.pg.to_numpy())
        beta, *_ = np.linalg.lstsq(X, y, rcond=None)
        resid = y - X @ beta
        dof = len(y) - X.shape[1]
        s2 = resid @ resid / dof
        se = np.sqrt(s2 * np.linalg.inv(X.T @ X)[-1, -1])
        tq = stats.t.ppf(0.975, dof)
        rate = float(beta[-1])
        out["F2_pooled"] = {"n": int(len(y)), "groups": groups, "rate": rate,
                            "ci95": [rate - tq * se, rate + tq * se],
                            "min_detectable_rate_80pct_power": float((tq + stats.t.ppf(0.8, dof)) * se),
                            "pass": bool(rate - tq * se > 0 and rate - tq * se <= SHAROV_RATE <= rate + tq * se)}
    else:
        out["F2_pooled"] = {"pass": None, "note": "no qualifying groups"}
    signs = [np.sign(out["groups"][g]["rate"]) for g in qualifying]
    out["F3_sign_consistency"] = {"qualifying_groups": qualifying, "signs": [int(s) for s in signs],
                                  "pass": bool(signs and all(s > 0 for s in signs))}
    out["verdict_H1_supported"] = bool(out["F2_pooled"].get("pass") and out["F3_sign_consistency"]["pass"])
    with open(ROOT / "results" / "fossils.json", "w") as fh:
        json.dump(out, fh, indent=2)
    figure(absolute, out, qualifying)
    print(json.dumps(out, indent=1))


def figure(absolute, out, qualifying):
    fig, ax = new_figure(7.5, 4.6)
    for color, (g, d) in zip(PALETTE, absolute.groupby("lineage_group")):
        ax.scatter(d.age_gyr * 1000, np.log10(d.pg), s=28, color=color, edgecolor="white", linewidth=0.8,
                   label=f"{g} (n={len(d)})", zorder=4)
        if g in qualifying:
            r = out["groups"][g]
            xs = np.linspace(d.age_gyr.min(), d.age_gyr.max(), 20)
            b0 = np.mean(np.log10(d.pg)) + r["rate"] * np.mean(d.age_gyr)
            ax.plot(xs * 1000, b0 - r["rate"] * xs, color=color, lw=1.8)
    if len(absolute):
        t0 = absolute.age_gyr.max()
        y0 = np.log10(absolute.pg).median()
        xs = np.array([t0, 0])
        ax.plot(xs * 1000, y0 + SHAROV_RATE * (t0 - xs), color=MUTED, lw=1.5, ls="--",
                label="Sharov's rate (0.89 log10/Gyr), for scale")
    ax.invert_xaxis()
    ax.set_xlabel("Age (Ma)")
    ax.set_ylabel("log10 genome size estimated from fossils (pg)")
    ax.set_title("Genome sizes of extinct species through time", loc="left", fontsize=10.5, color=INK)
    ax.legend(loc="best", frameon=False, fontsize=8)
    style_axes(ax)
    fig.tight_layout()
    fig.savefig(ROOT / "figures" / "fossils.png", dpi=160)


if __name__ == "__main__":
    main()
