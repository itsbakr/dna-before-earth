import numpy as np
import pytest
import treeswift

from clock import phylo

NEWICK = "((A:1,B:1):2,(C:2,D:2):1);"


def _tree():
    return treeswift.read_tree_newick(NEWICK)


def test_node_ages_on_ultrametric_tree():
    tree = _tree()
    ages = phylo.node_ages(tree)
    assert ages[tree.root] == pytest.approx(3)
    assert all(ages[leaf] == pytest.approx(0) for leaf in tree.traverse_leaves())


def test_pic_two_tips_matches_hand_calculation():
    tree = treeswift.read_tree_newick("(A:1,B:1);")
    s2, n = phylo.pic_sigma2(tree, {"A": 0.0, "B": 1.0}, eps=0)
    assert n == 1 and s2 == pytest.approx(0.5)      # (0 - 1)^2 / (1 + 1)


def test_pic_recovers_simulated_rate():
    rng = np.random.default_rng(0)
    # balanced tree with 1024 tips, all branches length 1
    nodes = [f"t{i}:1" for i in range(1024)]
    while len(nodes) > 1:
        nodes = [f"({a},{b}):1" for a, b in zip(nodes[::2], nodes[1::2])]
    tree = treeswift.read_tree_newick(nodes[0][:-2] + ";")
    est = [phylo.pic_sigma2(tree, phylo.simulate_bm(tree, 0.3, rng=rng), eps=0)[0] for _ in range(20)]
    assert np.mean(est) == pytest.approx(0.3, rel=0.05)


def test_clade_extremes_and_mrca():
    tree = _tree()
    lo, hi, n = phylo.clade_extremes(tree, {"A": 1, "B": 5, "C": 2, "D": 9})
    assert (lo[tree.root], hi[tree.root], n[tree.root]) == (1, 9, 4)
    m = phylo.mrca(tree, ["A", "B"])
    assert sorted(leaf.label for leaf in m.traverse_leaves()) == ["A", "B"]


def test_ou_transform_reduces_to_bm_for_small_alpha():
    tree = _tree()
    vals = {"A": 1.0, "B": 2.0, "C": 0.5, "D": 3.0}
    ll_bm, _ = phylo.pic_reml_loglik(tree, vals)
    ll_ou, _ = phylo.pic_reml_loglik(tree, vals, phylo.ou_lengths(tree, 1e-9))
    assert ll_ou == pytest.approx(ll_bm, abs=1e-6)


def test_fit_ou_detects_strong_pull():
    rng = np.random.default_rng(1)
    nodes = [f"t{i}:1" for i in range(512)]
    while len(nodes) > 1:
        nodes = [f"({a},{b}):1" for a, b in zip(nodes[::2], nodes[1::2])]
    tree = treeswift.read_tree_newick(nodes[0][:-2] + ";")
    vals = phylo.simulate_ou(tree, alpha=0.5, sigma2=1.0, theta=0.0, rng=rng)
    fit = phylo.fit_ou(tree, vals, alphas=np.logspace(-3, 1, 41))
    assert fit["delta_aic_bm_minus_ou"] > 10 and 0.1 < fit["alpha_per_myr"] < 2.5


def test_bounded_simulation_stays_in_bounds():
    vals = phylo.simulate_bounded(_tree(), 5.0, 0.0, 1.0, 0.5, rng=np.random.default_rng(2))
    assert all(0.0 <= v <= 1.0 for v in vals.values())
