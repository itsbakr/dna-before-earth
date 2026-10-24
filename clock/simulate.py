"""Branching random walks of log10 genome size, for calibrating clock methods.

Lineages split at rate ``lam`` and go extinct at rate ``mu`` (per Gyr). Along
each lineage log10 genome size follows Brownian motion with volatility
``sigma`` (log10 units per sqrt(Gyr)) and an optional directional ``drift``
(log10 units per Gyr; positive means growth toward the present). An optional
reflecting ``floor`` stands in for a minimum viable genome.

At each checkpoint age every living lineage gets a fresh clade label and its
trait value is recorded, so after the run we can reconstruct, for any extant
"focal" lineage, (a) the members of each of its ancestral clades and (b) the
true trait value of its ancestor at each checkpoint.
"""

from dataclasses import dataclass

import numpy as np


@dataclass
class Run:
    traits: np.ndarray        # extant trait values, shape (n,)
    labels: np.ndarray        # clade label at each checkpoint, shape (n, K)
    anc_traits: np.ndarray    # ancestor's trait at each checkpoint, shape (n, K)
    checkpoints: np.ndarray   # checkpoint ages (Gya), shape (K,)


def branching_walk(T, lam, sigma, checkpoints, mu=0.0, drift=0.0, start=6.0, floor=None,
                   dt=0.004, rng=None, max_lineages=250_000):
    """Simulate from age T to the present. Returns a Run, or None if the process
    dies out or exceeds ``max_lineages``."""
    rng = np.random.default_rng() if rng is None else rng
    cps = np.asarray(sorted(checkpoints, reverse=True), float)
    if cps[0] > T + 1e-9:
        raise ValueError("checkpoints must not be older than T")
    K = len(cps)
    trait = np.array([float(start)])
    labels = np.zeros((1, K), dtype=np.int64)
    anc = np.zeros((1, K))
    next_label, k = 1, 0
    steps = int(round(T / dt))
    age = T
    for _ in range(steps + 1):
        while k < K and age <= cps[k] + 1e-9:
            labels[:, k] = np.arange(next_label, next_label + len(trait))
            anc[:, k] = trait
            next_label += len(trait)
            k += 1
        if age <= 1e-9:
            break
        trait = trait + drift * dt + rng.normal(0.0, sigma * np.sqrt(dt), len(trait))
        if floor is not None:
            trait = np.where(trait < floor, 2 * floor - trait, trait)
        if mu > 0:
            alive = rng.random(len(trait)) >= mu * dt
            trait, labels, anc = trait[alive], labels[alive], anc[alive]
            if len(trait) == 0:
                return None
        split = rng.random(len(trait)) < lam * dt
        if split.any():
            trait = np.concatenate([trait, trait[split]])
            labels = np.vstack([labels, labels[split]])
            anc = np.vstack([anc, anc[split]])
        if len(trait) > max_lineages:
            return None
        age -= dt
    return Run(trait, labels, anc, cps)


def nested_series(run, focal, stat="min"):
    """Minimum (or maximum) extant trait over each ancestral clade of ``focal``."""
    f = np.min if stat == "min" else np.max
    return np.array([f(run.traits[run.labels[:, k] == run.labels[focal, k]])
                     for k in range(len(run.checkpoints))])


def ancestor_series(run, focal):
    """True trait of the focal lineage's ancestor at each checkpoint age."""
    return run.anc_traits[focal].copy()


def fit_line(ages, values, y0=0.0):
    """Clock fit y = a - b t. Returns slope b (log10/Gyr), origin age and R^2."""
    b_neg, a = np.polyfit(-np.asarray(ages, float), values, 1)
    pred = a + b_neg * (-np.asarray(ages, float))
    ss = np.sum((values - np.mean(values)) ** 2)
    r2 = 1 - np.sum((values - pred) ** 2) / ss if ss > 0 else np.nan
    origin = (a - y0) / b_neg if b_neg > 0 else np.inf
    return float(b_neg), float(origin), float(r2)


def extreme_speed(sigma, r):
    """Asymptotic speed of the extreme of a branching Brownian motion with net growth rate r."""
    return sigma * np.sqrt(2 * r)
