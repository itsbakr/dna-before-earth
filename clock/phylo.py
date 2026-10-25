"""Phylogenetic tools for the real-data test (WP3).

Trees are time-calibrated (branch lengths in Myr) and assumed ultrametric. Trait values are
log10 genome size (bp), keyed by species name with spaces (``"Homo sapiens"``).
"""

import warnings

import numpy as np
import treeswift


def normalize(label):
    return label.strip("'").replace("_", " ").strip() if label else label


def read_tree(path):
    tree = treeswift.read_tree_newick(str(path))
    for node in tree.traverse_preorder():
        if node.is_leaf():
            node.label = normalize(node.label)
    return tree


def prune_to(tree, labels):
    """Copy of ``tree`` restricted to leaves whose label is in ``labels``."""
    keep = {n.label for n in tree.traverse_leaves()} & set(labels)
    with warnings.catch_warnings():
        warnings.simplefilter("ignore", UserWarning)    # treeswift warns about dropping unlabeled nodes
        pruned = tree.extract_tree_with(keep, suppress_unifurcations=True)
    return pruned


def node_ages(tree):
    """Age (Myr before present) of every node, from root-to-node distances on an ultrametric tree."""
    dist = {}
    for node in tree.traverse_preorder():
        dist[node] = 0.0 if node.parent is None else dist[node.parent] + (node.edge_length or 0.0)
    height = max(dist[n] for n in tree.traverse_leaves())
    return {n: height - d for n, d in dist.items()}


def pic_contrasts(tree, values, lengths=None, eps=1e-6):
    """Felsenstein's independent contrasts. Returns (raw contrasts, their variance factors).

    ``lengths`` optionally maps node -> branch length (e.g. an OU-transformed tree); otherwise the
    tree's own edge lengths are used. Polytomies are paired sequentially with eps-length branches.
    """
    state, cs, vs = {}, [], []
    for node in tree.traverse_postorder():
        bl = lengths[node] if lengths is not None else (node.edge_length or 0.0)
        bl = max(bl, 0.0)
        if node.is_leaf():
            state[node] = (values[node.label], bl + eps)
            continue
        kids = [state[c] for c in node.children]
        x, v = kids[0]
        for x2, v2 in kids[1:]:
            cs.append(x - x2)
            vs.append(v + v2)
            x = (x / v + x2 / v2) / (1 / v + 1 / v2)
            v = v * v2 / (v + v2) + eps
        state[node] = (x, v + bl)
    return np.array(cs), np.array(vs)


def pic_sigma2(tree, values, eps=1e-6):
    """REML estimate of the Brownian-motion rate (trait units^2 per Myr). Returns (sigma2, n_contrasts)."""
    c, v = pic_contrasts(tree, values, eps=eps)
    return float(np.mean(c * c / v)), len(c)


def pic_reml_loglik(tree, values, lengths=None, eps=1e-6):
    """REML log-likelihood of a Brownian model on the (possibly transformed) tree, sigma2 profiled out."""
    c, v = pic_contrasts(tree, values, lengths, eps)
    n = len(c)
    s2 = float(np.mean(c * c / v))
    return -0.5 * (n * np.log(2 * np.pi * s2) + np.sum(np.log(v)) + n), s2


def ou_lengths(tree, alpha):
    """Branch lengths of the BM-equivalent tree for an OU process with fixed root on an ultrametric tree.

    Under OU the covariance of two tips depends only on the depth s of their MRCA:
    V(s) = sigma2 * exp(-2a(T - s)) * (1 - exp(-2a s)) / (2a). Mapping every node depth s to V(s)/sigma2
    turns the OU covariance into a Brownian covariance on the transformed tree.
    """
    depth = {}
    for node in tree.traverse_preorder():
        depth[node] = 0.0 if node.parent is None else depth[node.parent] + max(node.edge_length or 0.0, 0.0)
    T = max(depth[n] for n in tree.traverse_leaves())
    g = (lambda s: np.exp(-2 * alpha * (T - s)) * (-np.expm1(-2 * alpha * s)) / (2 * alpha)) if alpha > 0 else (lambda s: s)
    return {n: (g(depth[n]) - g(depth[n.parent])) if n.parent is not None else 0.0 for n in depth}


def fit_ou(tree, values, alphas=None):
    """Profile REML over alpha (per Myr). Returns dict with best alpha, sigma2, logliks for OU and BM."""
    alphas = np.logspace(-5, -1, 41) if alphas is None else alphas
    bm_ll, bm_s2 = pic_reml_loglik(tree, values)
    prof = [(a, *pic_reml_loglik(tree, values, ou_lengths(tree, a))) for a in alphas]
    a, ll, s2 = max(prof, key=lambda r: r[1])
    return {"alpha_per_myr": float(a), "half_life_myr": float(np.log(2) / a), "sigma2_per_myr": float(s2),
            "loglik_ou": float(ll), "loglik_bm": float(bm_ll), "sigma2_bm": float(bm_s2),
            "delta_aic_bm_minus_ou": float(2 * (ll - bm_ll) - 2),
            "profile": [(float(x), float(y)) for x, y, _ in prof]}


def clade_extremes(tree, values):
    """Min and max trait over the leaves below every node, and the leaf count."""
    lo, hi, n = {}, {}, {}
    for node in tree.traverse_postorder():
        if node.is_leaf():
            lo[node] = hi[node] = values[node.label]
            n[node] = 1
        else:
            lo[node] = min(lo[c] for c in node.children)
            hi[node] = max(hi[c] for c in node.children)
            n[node] = sum(n[c] for c in node.children)
    return lo, hi, n


def focal_series(leaf, ages, stat, min_age=0.0):
    """(ages in Gyr, statistic) over all ancestral nodes of ``leaf`` older than ``min_age`` Myr."""
    t, y = [], []
    node = leaf.parent
    while node is not None:
        if ages[node] >= min_age:
            t.append(ages[node] / 1000.0)
            y.append(stat[node])
        node = node.parent
    return np.array(t), np.array(y)


def simulate_bm(tree, sigma2, root_value=0.0, rng=None):
    """Brownian motion down the tree (no trend). Returns {leaf label: value}."""
    return _simulate(tree, rng, root_value,
                     lambda x, t, r: x + r.normal(0.0, np.sqrt(sigma2 * t)))


def simulate_ou(tree, alpha, sigma2, theta, root_value=None, rng=None):
    """Ornstein-Uhlenbeck (exact transitions) pulling toward theta at rate alpha (per Myr)."""
    sd = lambda t: np.sqrt(sigma2 * -np.expm1(-2 * alpha * t) / (2 * alpha))
    return _simulate(tree, rng, theta if root_value is None else root_value,
                     lambda x, t, r: theta + (x - theta) * np.exp(-alpha * t) + r.normal(0.0, sd(t)))


def simulate_empirical(tree, sigma2, shape, root_value=0.0, rng=None):
    """Random walk whose increments have the empirical (heavy-tailed) shape of the standardized
    contrasts, scaled to variance sigma2 * t. ``shape`` must have mean 0 and variance 1."""
    return _simulate(tree, rng, root_value,
                     lambda x, t, r: x + np.sqrt(sigma2 * t) * shape[r.integers(len(shape))])


def simulate_bounded(tree, sigma2, lo, hi, root_value, rng=None):
    """Brownian motion reflected into [lo, hi] at the end of each branch."""
    def step(x, t, r):
        y = x + r.normal(0.0, np.sqrt(sigma2 * t))
        width = hi - lo
        y = (y - lo) % (2 * width)
        return lo + (y if y <= width else 2 * width - y)
    return _simulate(tree, rng, root_value, step)


def _simulate(tree, rng, root_value, step):
    rng = np.random.default_rng() if rng is None else rng
    val, out = {}, {}
    for node in tree.traverse_preorder():
        if node.parent is None:
            val[node] = root_value
        else:
            val[node] = step(val[node.parent], max(node.edge_length or 0.0, 0.0), rng)
        if node.is_leaf():
            out[node.label] = val[node]
    return out


def mrca(tree, labels):
    """Most recent common ancestor of the leaves with the given labels."""
    wanted = set(labels)
    leaves = [n for n in tree.traverse_leaves() if n.label in wanted]
    if not leaves:
        return None
    paths = []
    for leaf in leaves:
        path, node = [], leaf
        while node is not None:
            path.append(node)
            node = node.parent
        paths.append(path[::-1])
    common = None
    for nodes in zip(*paths):
        if all(n is nodes[0] for n in nodes):
            common = nodes[0]
        else:
            break
    return common


def quick_fit(ages_gyr, values, y0=0.0):
    """Fast clock fit y = a - b t: returns (b, origin age, R^2); origin is inf for b <= 0, R^2 nan if flat."""
    t, y = np.asarray(ages_gyr, float), np.asarray(values, float)
    tc, yc = t - t.mean(), y - y.mean()
    stt, syy = float(tc @ tc), float(yc @ yc)
    if stt == 0:
        return np.nan, np.nan, np.nan
    b = -float(tc @ yc) / stt
    a = y.mean() + b * t.mean()
    r2 = float((tc @ yc) ** 2 / (stt * syy)) if syy > 0 else np.nan
    return b, ((a - y0) / b if b > 0 else np.inf), r2


def nested_min_fits(tree, values, min_age=1.0):
    """Markov-style fit for every leaf as focal lineage: min trait below each ancestral node vs node age.

    Returns (labels, slopes, origins, r2s); ages in Gyr, slopes in trait units per Gyr.
    """
    ages = node_ages(tree)
    lo, _, _ = clade_extremes(tree, values)
    labels, b, o, r2 = [], [], [], []
    for leaf in tree.traverse_leaves():
        ts, ys = focal_series(leaf, ages, lo, min_age=min_age)
        if len(ts) < 3:
            continue
        fit = quick_fit(ts, ys)
        labels.append(leaf.label); b.append(fit[0]); o.append(fit[1]); r2.append(fit[2])
    return labels, np.array(b), np.array(o), np.array(r2)


def summarize_fits(slopes, origins, r2s, earth_gya=4.54):
    fin = origins[np.isfinite(origins)]
    return {"focal_lineages": int(len(slopes)), "slope_median": float(np.median(slopes)),
            "slope_iqr": [float(np.percentile(slopes, 25)), float(np.percentile(slopes, 75))],
            "positive_slope_frac": float(np.mean(slopes > 0)),
            "r2_median": float(np.nanmedian(r2s)),
            "origin_median": float(np.median(origins)),
            "origin_iqr": [float(np.percentile(fin, 25)), float(np.percentile(fin, 75))] if len(fin) else [None, None],
            "pre_earth_frac": float(np.mean(origins > earth_gya))}
