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


def pic_sigma2(tree, values, eps=1e-6):
    """REML estimate of the Brownian-motion rate (trait units^2 per Myr) from independent contrasts.

    Polytomies are handled by sequential pairing with zero-length (eps) internal branches.
    Returns (sigma2, number_of_contrasts).
    """
    state = {}
    contrasts = []
    for node in tree.traverse_postorder():
        bl = max(node.edge_length or 0.0, 0.0)
        if node.is_leaf():
            state[node] = (values[node.label], bl + eps)
            continue
        kids = [state[c] for c in node.children]
        x, v = kids[0]
        for x2, v2 in kids[1:]:
            contrasts.append((x - x2) ** 2 / (v + v2))
            x = (x / v + x2 / v2) / (1 / v + 1 / v2)
            v = v * v2 / (v + v2) + eps
        state[node] = (x, v + bl)
    c = np.array(contrasts)
    return float(c.mean()), len(c)


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
    rng = np.random.default_rng() if rng is None else rng
    val = {}
    out = {}
    for node in tree.traverse_preorder():
        if node.parent is None:
            val[node] = root_value
        else:
            val[node] = val[node.parent] + rng.normal(0.0, np.sqrt(sigma2 * max(node.edge_length or 0.0, 0.0)))
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
