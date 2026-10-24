import sys, numpy as np, matplotlib
matplotlib.use("Agg"); import matplotlib.pyplot as plt
sys.path.insert(0, sys.argv[1]); import null_bbm as nb   # reuse simulator (prints its summary on import)

BLUE, ORANGE, AQUA = "#2a78d6", "#eb6834", "#1baf7a"
INK, INK2, MUTED, GRID, SURF = "#0b0b0b", "#52514e", "#8a8984", "#e6e5e1", "#fcfcfb"
plt.rcParams.update({"font.family": "DejaVu Sans", "font.size": 10, "text.color": INK, "axes.labelcolor": INK2,
                     "xtick.color": INK2, "ytick.color": INK2, "axes.edgecolor": GRID})

t = np.array([4.0, 2.0, 1.25, 0.575, 0.54, 0.375, 0.315, 0.22, 0.065])
y = np.log10(np.array([1.3, 9.2, 19.6, 68.6, 342, 931, 951, 1695, 2215]) * 1e6)
fig, axes = plt.subplots(1, 2, figsize=(12.5, 4.8), facecolor=SURF)
for ax in axes:
    ax.set_facecolor(SURF); ax.grid(color=GRID, lw=0.6); ax.set_axisbelow(True)
    for s in ("top", "right"): ax.spines[s].set_visible(False)

# Panel A: segment fits
ax = axes[0]
ax.axvspan(4.54, 22, color="#f1f0ec", zorder=0); ax.text(13.5, 9.6, "before Earth formed", color=MUTED, ha="center", fontsize=9)
ax.axvline(4.54, color=MUTED, lw=1, ls="--")
for mask, col, lab in [(np.ones(9, bool), BLUE, "All 9 points"), (t <= 0.6, ORANGE, "Phanerozoic only (6)"),
                       (t > 0.6, AQUA, "Precambrian only (3)")]:
    b = np.polyfit(-t[mask], y[mask], 1); origin = b[1] / b[0]
    xs = np.linspace(0, origin, 200); ax.plot(xs, np.polyval(b, -xs), color=col, lw=2)
    ax.annotate(f"{lab}\n'origin' {origin:.1f} Gya", xy=(origin, 0), xytext=(origin, 0.6 + (0.9 if col == ORANGE else 0)),
                color=INK, fontsize=9, ha="center", arrowprops=dict(arrowstyle="-", color=col, lw=1))
ax.scatter(t, y, s=46, color=INK, zorder=5, edgecolor=SURF, linewidth=1.5)
ax.set_xlim(20, -0.3); ax.set_ylim(-0.2, 10)
ax.set_xlabel("Clade age (billions of years ago)"); ax.set_ylabel("log10 minimal genome size (bp)")
ax.set_title("A. Markov et al. 2010 data: which slope you trust sets the 'origin'", loc="left", fontsize=11, color=INK)

# Panel B: null model
ax = axes[1]
rng = np.random.default_rng(7); runs = []; origins = []
while len(runs) < 40:
    out = nb.simulate()
    if out is None or len(out[0]) < 2000: continue
    tr, lab = out; f = rng.integers(len(tr)); s = nb.nested_min_series(tr, lab, f); runs.append(s)
    b = np.polyfit(-nb.AGES, s, 1); origins.append(b[1] / b[0])
for s in runs: ax.plot(nb.AGES, s, color=MUTED, lw=0.8, alpha=0.45)
ax.plot([], [], color=MUTED, lw=1.5, label="40 null runs (no trend, true origin 4.0 Gya)")
ax.scatter(t, y, s=46, color=BLUE, zorder=5, edgecolor=SURF, linewidth=1.5, label="Markov et al. observed")
ax.set_xlim(4.3, -0.1); ax.set_xlabel("Clade age (billions of years ago)"); ax.set_ylabel("log10 minimal genome size (bp)")
r2 = [1 - np.sum((s - np.polyval(np.polyfit(-nb.AGES, s, 1), -nb.AGES))**2) / np.sum((s - s.mean())**2) for s in runs]
ax.text(4.2, 9.7, f"Null runs: median R² {np.median(r2):.2f}\ninferred 'origin' median {np.median(origins):.1f} Gya\npre-Earth in {np.mean(np.array(origins) > 4.5)*100:.0f}% of runs, yet life\nbegan on Earth (4.0 Gya) in every run\n(level depends on starting size;\nthe rising shape does not)", fontsize=9, color=INK, va="top")
ax.set_ylim(1, 10); ax.legend(loc="lower right", frameon=False, fontsize=9)
ax.set_title("B. Same 'minimal genome per nested clade' method on a no-trend null", loc="left", fontsize=11, color=INK)
fig.tight_layout(); fig.savefig(sys.argv[2], dpi=160, facecolor=SURF); print("saved", sys.argv[2])
