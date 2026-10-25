"""WP4a decision rules, exactly as pre-registered in prereg/WP4_preregistration.md (Section 4.4).

Reads results/genecontent_counts.json, attaches node ages (2015 Timetree MRCA of each node's ingroup and
outgroup tips; literature ages as sensitivity), runs P1, P2, P4, P5 and P6, and writes
results/genecontent.json and figures/genecontent.png.
"""

import json
import sys
from pathlib import Path

import numpy as np
from scipy import stats

ROOT = Path(__file__).resolve().parent.parent
sys.path.insert(0, str(ROOT))

from clock import phylo, realdata, regression as R  # noqa: E402
from clock.plotting import COLORS, INK, INK2, MUTED, new_figure, style_axes  # noqa: E402
from scripts.run_genecontent import LINEAGES  # noqa: E402

LITERATURE_AGES = {"LUCA": 4.2, "LECA": 1.735, "Metazoa": 0.742}   # Moody 2024; Kay 2025; dos Reis 2015 midpoints


def node_age_gyr(lvl, ing, outg):
    tree = realdata.timetree()
    ages = phylo.node_ages(tree)
    tip_taxid, lin = realdata.tip_taxonomy()
    taxa = set()
    for grp in (ing, outg):
        taxa |= {lvl} if grp == "LEVEL-minus" else set(grp)
    if lvl == 1:
        return ages[tree.root] / 1000
    tips = [lab for lab, t in tip_taxid.items() if lin.get(t, set()) & taxa]
    node = phylo.mrca(tree, tips)
    return ages[node] / 1000 if node is not None else None


def ols_ci(t, y):
    f = R.ols(t, y)
    q = stats.t.ppf(0.975, f["n"] - 2)
    se = np.sqrt(f["cov"][1, 1])
    return f, (f["b"] - q * se, f["b"] + q * se)


def prediction_interval(t_train, y_train, t_new):
    f = R.ols(t_train, y_train)
    n = f["n"]
    q = stats.t.ppf(0.975, n - 2)
    x, x0 = -np.asarray(t_train), -np.asarray(t_new)
    sxx = np.sum((x - x.mean()) ** 2)
    pred = f["a"] + f["b"] * x0
    half = q * f["resid_sd"] * np.sqrt(1 + 1 / n + (x0 - x.mean()) ** 2 / sxx)
    return pred, pred - half, pred + half


def tests(series):
    """series: {lineage: (names, t, y)}. Returns pre-registered results."""
    res = {}
    for lname, (names, t, y) in series.items():
        f, ci = ols_ci(t, y)
        bs = R.broken_stick(t, y)
        p1 = {"rate": f["b"], "rate_ci95": list(ci), "r2": f["r2"],
              "aicc_line": bs["aicc_one_line"], "aicc_two_segment_with_break": bs["aicc_two_segment_with_break_param"],
              "break_gya": bs["break_gya"], "rate_older": bs["rate_old"], "rate_younger": bs["rate_young"]}
        p1["pass"] = bool(ci[0] > 0 and f["r2"] >= 0.80 and
                          not (bs["aicc_two_segment_with_break_param"] < bs["aicc_one_line"] - 2))
        young = t < 1.0
        idx = {n: i for i, n in enumerate(names)}
        p2 = {"n_train": int(young.sum())}
        if young.sum() >= 3:
            ok = True
            for node in ("LECA", "LUCA"):
                pred, lo, hi = prediction_interval(t[young], y[young], [t[idx[node]]])
                inside = bool(lo[0] <= y[idx[node]] <= hi[0])
                p2[node] = {"observed": float(y[idx[node]]), "predicted": float(pred[0]),
                            "pi95": [float(lo[0]), float(hi[0])], "inside": inside}
                ok &= inside
            p2["pass"] = bool(ok)
        else:
            p2["pass"] = None
        p6_rate = (y[idx["LECA"]] - y[idx["LUCA"]]) / (t[idx["LUCA"]] - t[idx["LECA"]])
        res[lname] = {"P1": p1, "P2": p2,
                      "P5_age_at_one_family_gya": float(R.origin(f["a"], f["b"])) if f["b"] > 0 else None,
                      "P6": {"rate_luca_to_leca": float(p6_rate), "half_lineage_rate": f["b"] / 2,
                             "pass": bool(p6_rate >= 0.5 * f["b"])}}
        res[lname]["P5"] = {"pass": bool(res[lname]["P5_age_at_one_family_gya"] is not None
                                         and res[lname]["P5_age_at_one_family_gya"] < 13.8)}
    cis = {k: v["P1"]["rate_ci95"] for k, v in res.items()}
    keys = list(cis)
    overlaps = {f"{a}-{b}": bool(cis[a][0] <= cis[b][1] and cis[b][0] <= cis[a][1])
                for i, a in enumerate(keys) for b in keys[i + 1:]}
    res["P4"] = {"pairwise_ci_overlap": overlaps, "pass": all(overlaps.values())}
    h = res["human"]
    res["verdict_H1_supported"] = bool(h["P1"]["pass"] and h["P2"]["pass"] and res["P4"]["pass"]
                                       and h["P5"]["pass"] and h["P6"]["pass"])
    return res


def main():
    counts = json.load(open(ROOT / "results" / "genecontent_counts.json"))
    table, series = {}, {"S_a": {}, "S_b": {}, "S_a_literature_ages": {}, "S_a_outgroup_ge3_exploratory": {}}
    for lname, lin in LINEAGES.items():
        rows = counts["lineages"][lname]
        for row, (node, lvl, ing, outg) in zip(rows, lin["nodes"]):
            row["age_gyr_timetree"] = node_age_gyr(lvl, ing, outg)
            row["age_gyr_literature"] = LITERATURE_AGES.get(node, row["age_gyr_timetree"])
        table[lname] = rows
        # Deviation: a node with no ingroup or outgroup species in eggNOG has no defined split.
        usable = [r for r in rows if r["n_ingroup_species"] > 0 and r["n_outgroup_species"] > 0]
        robust = [r for r in usable if r["n_outgroup_species"] >= 3 or r["node"] in ("LUCA", "LECA")]
        for key, stat, rws, agecol in [("S_a", "S_a", usable, "age_gyr_timetree"),
                                       ("S_b", "S_b", usable, "age_gyr_timetree"),
                                       ("S_a_literature_ages", "S_a", usable, "age_gyr_literature"),
                                       ("S_a_outgroup_ge3_exploratory", "S_a", robust, "age_gyr_timetree")]:
            series[key][lname] = ([r["node"] for r in rws], np.array([r[agecol] for r in rws]),
                                  np.log10([r[stat] for r in rws]))
    dropped = [f"{l}: {r['node']}" for l, rows in table.items() for r in rows
               if r["n_ingroup_species"] == 0 or r["n_outgroup_species"] == 0]
    out = {"counts_and_ages": table,
           "deviations": counts["deviations"] + [f"Dropped (no outgroup or ingroup species in eggNOG): {', '.join(dropped)}"],
           "tests": {k: tests(v) for k, v in series.items()}}
    with open(ROOT / "results" / "genecontent.json", "w") as fh:
        json.dump(out, fh, indent=2, default=float)
    figure(series["S_a"], out["tests"]["S_a"])
    print(json.dumps(out["tests"]["S_a"], indent=1, default=float))


def figure(series, res):
    fig, axes = new_figure(12.5, 4.6, ncols=2)
    ax = axes[0]
    for (lname, (names, t, y)), color in zip(series.items(), COLORS):
        order = np.argsort(t)
        ax.plot(t[order], y[order], marker="o", ms=5, lw=1.6, color=color,
                label=f"{lname} lineage (straight-line R² {res[lname]['P1']['r2']:.2f})")
    names, t, y = series["human"]
    for n_, ti, yi in zip(names, t, y):
        if n_ in ("LUCA", "LECA", "Metazoa", "Bilateria"):
            ax.annotate(n_, (ti, yi), xytext=(6, -12), textcoords="offset points", fontsize=8, color=INK2)
    ax.set_xlim(max(t) * 1.05, -0.05)
    ax.set_ylim(3.3, 4.55)
    ax.set_xlabel("Node age (Gya, 2015 Timetree)")
    ax.set_ylabel("log10 ancestral gene families")
    ax.set_title("A. Gene families present in each ancestor (eggNOG 6)", loc="left", fontsize=10.5, color=INK)
    ax.legend(loc="upper left", frameon=False, fontsize=8.5)
    style_axes(ax)

    ax = axes[1]
    names, t, y = series["human"]
    f = R.ols(t, y)
    o = R.origin(f["a"], f["b"])
    xs = np.linspace(0, o, 200)
    ax.plot(xs, f["a"] - f["b"] * xs, color=COLORS[1], lw=2,
            label=f"constant rate {f['b']:.2f} log10/Gyr (pre-registered fit)")
    ax.scatter(t, y, s=30, color=COLORS[0], zorder=5, edgecolor="white", linewidth=1, label="human-lineage ancestors")
    for xv, txt in [(4.54, "Earth forms"), (13.8, "Big Bang")]:
        ax.axvline(xv, color=MUTED, lw=1, ls="--")
        ax.text(xv + 0.3, 0.25, txt, color=INK2, fontsize=8.5, rotation=90, va="bottom")
    ax.annotate(f"one gene family at {o:.1f} Gya", (o, 0), xytext=(12, 4), textcoords="offset points",
                ha="left", fontsize=9, color=INK)
    ax.set_xlim(o * 1.08, -0.3)
    ax.set_ylim(-0.2, 4.6)
    ax.set_xlabel("Age (Gya)")
    ax.set_ylabel("log10 ancestral gene families")
    ax.set_title("B. The gene-content clock extrapolated (test P5)", loc="left", fontsize=10.5, color=INK)
    ax.legend(loc="upper left", frameon=False, fontsize=8.5)
    style_axes(ax)
    fig.tight_layout()
    fig.savefig(ROOT / "figures" / "genecontent.png", dpi=160)


if __name__ == "__main__":
    main()
