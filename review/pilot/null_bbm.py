"""Pilot null model: undirected random walk of log10 genome size on a branching tree.

No directional trend at all. Life starts at 4.0 Gya with a 1 Mb genome (so the true origin is known).
We then apply Markov et al.'s construction (minimal genome size of the extant members of each
nested clade on a focal lineage, regressed on clade age) and see what 'origin' it infers.
"""
import numpy as np
rng = np.random.default_rng(1)
AGES = np.array([4.0, 2.0, 1.25, 0.575, 0.54, 0.375, 0.315, 0.22, 0.065])  # Markov's clade ages (Gyr)

def simulate(lam=2.6, sigma=0.5, T=4.0, dt=0.004, start=6.0, floor=None, max_tips=60000):
    trait = np.array([start]); labels = np.zeros((1, len(AGES)), dtype=np.int64)
    t_now = T; next_label = 1; k_done = 0
    steps = int(round(T / dt))
    for s in range(steps):
        # label checkpoints: every lineage alive at a checkpoint age gets a unique id
        while k_done < len(AGES) and t_now <= AGES[k_done] + 1e-12:
            labels[:, k_done] = np.arange(next_label, next_label + len(trait)); next_label += len(trait); k_done += 1
        trait = trait + rng.normal(0, sigma * np.sqrt(dt), len(trait))
        if floor is not None:  # reflecting lower wall (minimum viable genome)
            trait = np.where(trait < floor, 2 * floor - trait, trait)
        split = rng.random(len(trait)) < lam * dt
        if split.any():
            trait = np.concatenate([trait, trait[split]]); labels = np.vstack([labels, labels[split]])
        if len(trait) > max_tips:
            return None
        t_now -= dt
    while k_done < len(AGES):
        labels[:, k_done] = np.arange(next_label, next_label + len(trait)); next_label += len(trait); k_done += 1
    return trait, labels

def nested_min_series(trait, labels, focal):
    return np.array([trait[labels[:, k] == labels[focal, k]].min() for k in range(len(AGES))])

def fit(y):
    b = np.polyfit(-AGES, y, 1); pred = np.polyval(b, -AGES)
    r2 = 1 - np.sum((y - pred)**2) / np.sum((y - y.mean())**2)
    return b[0], b[1] / b[0], r2   # slope (log10/Gyr), inferred 1 bp origin (Gya), R2

for floor in (None, 5.5):
    res = {"random": [], "max": []}
    reps = 0
    while reps < 60:
        out = simulate(floor=floor)
        if out is None or len(out[0]) < 2000:
            continue
        trait, labels = out; reps += 1
        for mode in res:
            focal = rng.integers(len(trait)) if mode == "random" else int(np.argmax(trait))
            res[mode].append(fit(nested_min_series(trait, labels, focal)))
    print(f"\nFloor = {floor} (true origin of life in every run: 4.0 Gya, starting at 1 Mb; NO trend)")
    for mode, rows in res.items():
        a = np.array(rows)
        ok = a[:, 0] > 0
        print(f"  focal lineage = {mode:<6}: positive slope in {ok.mean()*100:5.1f}% of runs | "
              f"median slope {np.median(a[:,0]):.2f} log10/Gyr | median R2 {np.median(a[:,2]):.2f} "
              f"(R2>0.8 in {np.mean(a[:,2]>0.8)*100:.0f}%) | inferred 'origin' median {np.median(a[ok,1]):.1f} Gya, "
              f"pre-Earth (>4.5) in {np.mean(a[ok,1]>4.5)*100:.0f}% of positive-slope runs")
