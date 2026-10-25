"""WP3: the clock on real data.

(a) Markov et al.'s minimal-genome table recomputed from GoaT (directly measured genome sizes) with
    NCBI clade membership and TimeTree crown ages.
(b) Real-tree calibration: the Brownian-motion rate of log10 genome size is estimated by independent
    contrasts on the TimeTree of Life pruned to species with data; the Markov-style nested-minimum
    slope is computed for every species as focal lineage, and compared with the same statistic under
    a no-trend Brownian-motion null simulated on the same tree.

Needs the raw downloads from scripts/fetch_data.py. Writes results/realdata.json and figures/realdata.png.
"""

import json
import sys
from pathlib import Path

import numpy as np
import pandas as pd

ROOT = Path(__file__).resolve().parent.parent
sys.path.insert(0, str(ROOT))

from clock import data, phylo, regression as R, taxonomy  # noqa: E402
from clock.plotting import COLORS, INK, INK2, MUTED, new_figure, style_axes  # noqa: E402

EXT = ROOT / "data" / "external"
EARTH_GYA = 4.54
N_NULL = 20
SEED = 20261025
MARKOV_CLADES = [("Eukaryotes", "Eukaryota", 2759), ("Metazoa", "Metazoa", 33208),
                 ("Chordates", "Chordata", 7711), ("Vertebrates", "Vertebrata", 7742),
                 ("Tetrapods", "Tetrapoda", 32523), ("Amniotes", "Amniota", 32524),
                 ("Mammals", "Mammalia", 40674), ("Primates", "Primates", 9443)]
MAJOR_CLADES = [("Eukaryota", 2759), ("Viridiplantae", 33090), ("Fungi", 4751), ("Metazoa", 33208),
                ("Arthropoda", 6656), ("Vertebrata", 7742), ("Mammalia", 40674)]


def load_goat():
    g = pd.read_csv(EXT / "goat" / "eukaryote_genome_size_direct.tsv", sep="\t", dtype={"taxon_id": str})
    g = g[g.genome_size > 0].copy()
    g["log10_bp"] = np.log10(g.genome_size)
    g["ncbi"] = g.taxon_id.str.fullmatch(r"\d+")
    return g


def main():
    rng = np.random.default_rng(SEED)
    out = {}
    goat = load_goat()
    tree = phylo.read_tree(EXT / "timetree" / "TimetreeOfLife2015.nwk")
    ages = phylo.node_ages(tree)
    tips = [leaf.label for leaf in tree.traverse_leaves()]
    tip_taxid = taxonomy.scientific_names_to_taxids(tips)
    g_ncbi = goat[goat.ncbi]
    lin = taxonomy.lineages(list(tip_taxid.values()) + g_ncbi.taxon_id.astype(int).tolist())
    out["inputs"] = {"goat_species": int(len(goat)), "goat_species_with_ncbi_taxid": int(len(g_ncbi)),
                     "tree_tips": len(tips), "tree_tips_with_taxid": len(tip_taxid),
                     "tree_root_age_myr": float(ages[tree.root])}

    # ---------------- (a) Markov's table recomputed -------------------------------------------
    markov = data.load_markov()
    rows = []
    for group, name, tid in MARKOV_CLADES:
        members = g_ncbi[[tid in lin.get(int(t), ()) for t in g_ncbi.taxon_id]]
        imin = members.genome_size.idxmin()
        clade_tips = [lab for lab, t in tip_taxid.items() if tid in lin.get(t, ())]
        node = phylo.mrca(tree, clade_tips)
        rows.append({"group": group, "ncbi_name": name, "taxid": tid, "n_species_with_size": int(len(members)),
                     "min_mb": float(members.genome_size.min() / 1e6),
                     "min_species": members.loc[imin, "scientific_name"],
                     "p01_mb": float(members.genome_size.quantile(0.01) / 1e6),
                     "median_mb": float(members.genome_size.median() / 1e6),
                     "crown_age_gya_timetree": float(ages[node] / 1000) if node else None,
                     "n_tree_tips": len(clade_tips),
                     "markov_mgs_mb": float(10 ** markov.y[markov.groups.index(group)] / 1e6),
                     "markov_age_gya": float(markov.t[markov.groups.index(group)])})
    tab = pd.DataFrame(rows)
    t = tab.crown_age_gya_timetree.to_numpy()
    fits = {}
    for col in ("min_mb", "p01_mb", "median_mb"):
        f = R.ols(t, np.log10(tab[col].to_numpy() * 1e6))
        fits[col] = {"b": f["b"], "r2": f["r2"], "origin_1bp": R.origin(f["a"], f["b"])}
    f = R.ols(markov.t[1:], markov.y[1:])
    fits["markov_eukaryote_rows_published"] = {"b": f["b"], "r2": f["r2"], "origin_1bp": R.origin(f["a"], f["b"])}
    out["markov_recomputed"] = {"table": rows, "fits": fits}

    # ---------------- (b) Real-tree calibration -----------------------------------------------
    values = dict(zip(goat.scientific_name, goat.log10_bp))
    pruned = phylo.prune_to(tree, values.keys())
    p_ages = phylo.node_ages(pruned)
    leaves = list(pruned.traverse_leaves())
    vals = {leaf.label: values[leaf.label] for leaf in leaves}
    sigma2_myr, ncon = phylo.pic_sigma2(pruned, vals)
    out["pruned_tree"] = {"tips": len(leaves), "root_age_myr": float(p_ages[pruned.root]),
                          "sigma2_per_myr": sigma2_myr, "sigma_log10_per_sqrt_gyr": float(np.sqrt(sigma2_myr * 1000)),
                          "contrasts": ncon}

    # BM rate by major clade (subtree of the pruned tree)
    by_clade = []
    label_taxid = {leaf.label: tip_taxid.get(leaf.label) for leaf in leaves}
    for name, tid in MAJOR_CLADES:
        labs = [lab for lab, t in label_taxid.items() if t and tid in lin.get(t, ())]
        if len(labs) < 20:
            continue
        sub = phylo.prune_to(pruned, labs)
        s2, nc = phylo.pic_sigma2(sub, {lab: vals[lab] for lab in labs})
        by_clade.append({"clade": name, "tips": len(labs), "sigma_log10_per_sqrt_gyr": float(np.sqrt(s2 * 1000)),
                         "crown_age_myr": float(phylo.node_ages(sub)[sub.root])})
    out["sigma_by_clade"] = by_clade

    def per_focal(tr, tr_ages, tr_leaves, stat_values):
        lo, _, _ = phylo.clade_extremes(tr, stat_values)
        labels, b, o, r2 = [], [], [], []
        for leaf in tr_leaves:
            ts, ys = phylo.focal_series(leaf, tr_ages, lo, min_age=1.0)
            if len(ts) < 3:
                continue
            fit = phylo.quick_fit(ts, ys)
            labels.append(leaf.label); b.append(fit[0]); o.append(fit[1]); r2.append(fit[2])
        return labels, np.array(b), np.array(o), np.array(r2)

    def summarize(slopes, origins, r2s):
        fin = origins[np.isfinite(origins)]
        return {"focal_lineages": int(len(slopes)), "slope_median": float(np.median(slopes)),
                "slope_iqr": [float(np.percentile(slopes, 25)), float(np.percentile(slopes, 75))],
                "positive_slope_frac": float(np.mean(slopes > 0)),
                "r2_median": float(np.nanmedian(r2s)),
                "origin_median": float(np.median(origins)),
                "origin_iqr": [float(np.percentile(fin, 25)), float(np.percentile(fin, 75))],
                "pre_earth_frac": float(np.mean(origins > EARTH_GYA))}

    def calibrate(tr, tr_vals):
        tr_ages = phylo.node_ages(tr)
        tr_leaves = list(tr.traverse_leaves())
        s2, _ = phylo.pic_sigma2(tr, tr_vals)
        labels, b, o, r2 = per_focal(tr, tr_ages, tr_leaves, tr_vals)
        root_value = float(np.mean(list(tr_vals.values())))
        null_summ, null_b = [], []
        for _ in range(N_NULL):
            sim = phylo.simulate_bm(tr, s2, root_value=root_value, rng=rng)
            _, nb, no, nr2 = per_focal(tr, tr_ages, tr_leaves, sim)
            null_summ.append(summarize(nb, no, nr2))
            null_b.append(nb)
        res = {"tips": len(tr_leaves), "root_age_myr": float(tr_ages[tr.root]),
               "sigma_log10_per_sqrt_gyr": float(np.sqrt(s2 * 1000)),
               "observed": summarize(b, o, r2),
               "null_bm": {"runs": N_NULL,
                           "slope_median": [r["slope_median"] for r in null_summ],
                           "r2_median": [r["r2_median"] for r in null_summ],
                           "pre_earth_frac": [r["pre_earth_frac"] for r in null_summ],
                           "positive_slope_frac": [r["positive_slope_frac"] for r in null_summ]}}
        return res, labels, b, o, np.concatenate(null_b)

    calib, panels = {}, {}
    for name, tid in [("Eukaryota", 2759), ("Metazoa", 33208), ("Viridiplantae", 33090)]:
        labs = [lab for lab, t in label_taxid.items() if t and tid in lin.get(t, ())]
        tr = pruned if name == "Eukaryota" else phylo.prune_to(pruned, labs)
        tr_vals = {leaf.label: vals[leaf.label] for leaf in tr.traverse_leaves()}
        res, labels, b, o, nb = calibrate(tr, tr_vals)
        calib[name] = res
        panels[name] = (b, nb)
        if name == "Eukaryota":
            focal_by_clade = []
            for cname, ctid in MAJOR_CLADES[1:]:
                mask = np.array([bool(label_taxid.get(lab)) and ctid in lin.get(label_taxid[lab], ())
                                 for lab in labels])
                if mask.sum() >= 20:
                    oo = o[mask][np.isfinite(o[mask])]
                    focal_by_clade.append({"clade": cname, "focal_lineages": int(mask.sum()),
                                           "slope_median": float(np.median(b[mask])),
                                           "origin_median": float(np.median(oo)),
                                           "origin_iqr": [float(np.percentile(oo, 25)), float(np.percentile(oo, 75))]})
            calib["origin_by_focal_clade"] = focal_by_clade
    out["calibration"] = calib

    with open(ROOT / "results" / "realdata.json", "w") as fh:
        json.dump(out, fh, indent=2, default=lambda o: o.item() if hasattr(o, "item") else str(o))
    figure(tab, fits, panels)
    print(json.dumps(out["calibration"], indent=1))
    print(tab[["group", "n_species_with_size", "min_mb", "min_species", "p01_mb", "median_mb",
               "crown_age_gya_timetree", "markov_mgs_mb", "markov_age_gya"]].to_string())
    print(json.dumps(fits, indent=1))
    print(json.dumps(by_clade, indent=1))


def figure(tab, fits, panels):
    fig, axes = new_figure(15.5, 4.4, ncols=3)
    ax = axes[0]
    t = tab.crown_age_gya_timetree.to_numpy()
    for col, color, lab in [("min_mb", COLORS[0], "minimum (Markov's statistic)"),
                            ("median_mb", COLORS[1], "median")]:
        y = np.log10(tab[col].to_numpy() * 1e6)
        ax.scatter(t, y, s=40, color=color, zorder=5, edgecolor="white", linewidth=1.2,
                   label=f"{lab}: rate {fits[col]['b']:.2f}, R² {fits[col]['r2']:.2f}")
        f = np.polyfit(-t, y, 1)
        xs = np.linspace(0, t.max(), 50)
        ax.plot(xs, np.polyval(f, -xs), color=color, lw=2)
    young = {"Tetrapods", "Amniotes", "Mammals", "Primates"}
    for ti, gi in zip(t, tab.group):
        if gi in young:
            continue
        ax.annotate(gi, (ti, np.log10(tab.loc[tab.group == gi, "min_mb"].iloc[0] * 1e6)),
                    xytext=(0, -13), textcoords="offset points", fontsize=7.5, color=INK2, ha="center")
    ax.text(0.2, 8.1, "upper right cluster:\ntetrapods, amniotes,\nmammals, primates", fontsize=7.5,
            color=INK2, ha="center")
    ax.set_xlim(t.max() * 1.08, -0.12)
    ax.set_xlabel("Crown age from TimeTree (Gya)")
    ax.set_ylabel("log10 genome size in clade (bp)")
    ax.set_title("A. Markov's table rebuilt from 17,000 genomes", loc="left", fontsize=10.5, color=INK)
    ax.legend(loc="upper left", frameon=False, fontsize=8.5)
    style_axes(ax)

    bins = np.linspace(-1, 6, 71)
    for ax, (name, title) in zip(axes[1:], [("Metazoa", "B. Animals"), ("Viridiplantae", "C. Green plants")]):
        b, nb = panels[name]
        ax.hist(nb, bins=bins, density=True, color=MUTED, alpha=0.55, label="no-trend Brownian motion, same tree")
        ax.hist(b, bins=bins, density=True, histtype="step", color=COLORS[0], lw=2, label="observed genome sizes")
        ax.axvline(0, color=INK2, lw=1, ls=":")
        ax.set_xlabel("Nested-minimum 'clock rate' per focal species (log10/Gyr)")
        ax.set_ylabel("Density")
        ax.set_title(f"{title}: every species as focal lineage", loc="left", fontsize=10.5, color=INK)
        ax.legend(loc="upper right", frameon=False, fontsize=8.5)
        style_axes(ax)
    fig.tight_layout()
    fig.savefig(ROOT / "figures" / "realdata.png", dpi=160)


if __name__ == "__main__":
    main()
