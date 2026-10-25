"""Shared loaders for the real-data analyses (GoaT genome sizes on the 2015 Timetree of Life)."""

from functools import lru_cache
from pathlib import Path

import numpy as np
import pandas as pd

from . import phylo, taxonomy

EXT = Path(__file__).resolve().parent.parent / "data" / "external"


def load_goat():
    g = pd.read_csv(EXT / "goat" / "eukaryote_genome_size_direct.tsv", sep="\t", dtype={"taxon_id": str})
    g = g[g.genome_size > 0].copy()
    g["log10_bp"] = np.log10(g.genome_size)
    g["ncbi"] = g.taxon_id.str.fullmatch(r"\d+")
    return g


@lru_cache(maxsize=1)
def timetree():
    return phylo.read_tree(EXT / "timetree" / "TimetreeOfLife2015.nwk")


@lru_cache(maxsize=1)
def tip_taxonomy():
    """(tip label -> taxid, taxid -> set of ancestor taxids) for all tips of the 2015 tree and GoaT species."""
    tips = [leaf.label for leaf in timetree().traverse_leaves()]
    tip_taxid = taxonomy.scientific_names_to_taxids(tips)
    g = load_goat()
    lin = taxonomy.lineages(list(tip_taxid.values()) + g[g.ncbi].taxon_id.astype(int).tolist())
    return tip_taxid, lin


def pruned_genome_tree(clade_taxid=None):
    """2015 Timetree pruned to species with directly measured genome size, optionally to one clade.

    Returns (tree, {label: log10 bp})."""
    g = load_goat()
    values = dict(zip(g.scientific_name, g.log10_bp))
    tree = phylo.prune_to(timetree(), values.keys())
    if clade_taxid is not None:
        tip_taxid, lin = tip_taxonomy()
        labs = [leaf.label for leaf in tree.traverse_leaves()
                if tip_taxid.get(leaf.label) and clade_taxid in lin.get(tip_taxid[leaf.label], ())]
        tree = phylo.prune_to(tree, labs)
    vals = {leaf.label: values[leaf.label] for leaf in tree.traverse_leaves()}
    return tree, vals
