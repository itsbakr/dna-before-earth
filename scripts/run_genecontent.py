"""WP4a (pre-registered, prereg/WP4_preregistration.md): ancestral gene content from eggNOG 6.

Pass 1 collects the species present at the relevant taxonomic levels; pass 2 counts, for every node on the
human, Arabidopsis and yeast lineages:
  S_a  orthologous groups (OGs) at the node's level with >= 1 ingroup and >= 1 outgroup species
  S_b  focal-species proteins in such spanning OGs
  S_c  spanning OGs that contain the focal species
Writes results/genecontent_counts.json (counts only; tests are in scripts/test_genecontent.py).
"""

import json
import sys
import time
from pathlib import Path

ROOT = Path(__file__).resolve().parent.parent
sys.path.insert(0, str(ROOT))

from clock import taxonomy  # noqa: E402

EGG = ROOT / "data" / "external" / "eggnog" / "e6.og2seqs_and_species.tsv"

# (node name, eggNOG level, ingroup taxids, outgroup taxids). "LEVEL-minus" means: members of the level
# not in the other group. Substitutions relative to the pre-registration are listed in DEVIATIONS.
LINEAGES = {
    "human": {"focal": "9606", "nodes": [
        ("LUCA", 1, [2157, 2759], [2]),
        ("LECA", 2759, [33154, 554915, 554296], [33090, 2698737, 2763]),
        ("Opisthokonta", 33154, [33208, 28009, 127916], [4751]),
        ("Metazoa", 33208, "LEVEL-minus", [6040, 10197]),
        ("Bilateria", 33213, [33511], [33317]),
        ("Chordata", 7711, [89593, 7712], [7735]),
        ("Vertebrata", 7742, [7776], [1476529]),
        ("Sarcopterygii", 8287, [32523], [7878, 118072]),
        ("Mammalia", 40674, [32525], [9255]),
        ("Euarchontoglires", 314146, "LEVEL-minus", [314147]),
        ("Primates", 9443, [376913], [376911]),
        ("Haplorrhini", 376913, [314293], [376912]),
        ("Simiiformes", 314293, [9526], [9479]),
        ("Catarrhini", 9526, [314295], [314294]),
        ("Hominoidea", 314295, [9604], [9577]),
        ("Hominidae", 9604, [207598], [607660]),
    ]},
    "arabidopsis": {"focal": "3702", "nodes": [
        ("LUCA", 1, [2157, 2759], [2]),
        ("LECA", 2759, [33154, 554915, 554296], [33090, 2698737, 2763]),
        ("Viridiplantae", 33090, [35493], [3041]),
        ("Streptophyta", 35493, [131221], "LEVEL-minus"),
        ("Streptophytina", 131221, [3193], "LEVEL-minus"),
        ("Magnoliopsida", 3398, [1437183], "LEVEL-minus"),
        ("Brassicaceae", 3700, [980083], "LEVEL-minus"),
    ]},
    "yeast": {"focal": "559292|4932", "nodes": [
        ("LUCA", 1, [2157, 2759], [2]),
        ("LECA", 2759, [33154, 554915, 554296], [33090, 2698737, 2763]),
        ("Opisthokonta", 33154, [33208, 28009, 127916], [4751]),
        ("Fungi", 4751, [451864], "LEVEL-minus"),
        ("Dikarya", 451864, [4890], [5204]),
        ("Ascomycota", 4890, [147537, 147538], [451866]),
        ("Saccharomycetales", 4892, [4893], "LEVEL-minus"),
    ]},
}
DEVIATIONS = [
    "Sarcopterygii outgroup: NCBI has no 'Dipnoi'/'Actinistia'; used Dipnomorpha (7878) and Coelacanthimorpha (118072).",
    "Euarchontoglires ingroup: NCBI has no 'Euarchonta'; used Euarchontoglires minus Glires.",
    "Yeast focal species: S. cerevisiae S288C (559292) or 4932, whichever eggNOG uses.",
]


def relevant_levels():
    return {str(lvl) for lin in LINEAGES.values() for _, lvl, _, _ in lin["nodes"]}


def pass1(levels):
    species = set()
    with open(EGG) as fh:
        for line in fh:
            lvl, rest = line.split("\t", 1)
            if lvl in levels:
                species.update(rest.split("\t", 4)[3].split(","))
    return species


def node_sets(species, lin_of):
    """For every (lineage, node): (ingroup species set, outgroup species set) as strings."""
    sets = {}
    for lname, lin in LINEAGES.items():
        for node, lvl, ing, outg in lin["nodes"]:
            members = {s for s in species if lvl == 1 or lvl in lin_of.get(int(s), ())}
            def within(taxa):
                return {s for s in members if lin_of.get(int(s), set()) & set(taxa)}
            if ing == "LEVEL-minus":
                o = within(outg)
                i = members - o
            elif outg == "LEVEL-minus":
                i = within(ing)
                o = members - i
            else:
                i, o = within(ing), within(outg)
            sets[(lname, node)] = (frozenset(i), frozenset(o), str(lvl))
    return sets


def pass2(sets):
    by_level = {}
    for key, (i, o, lvl) in sets.items():
        by_level.setdefault(lvl, []).append((key, i, o))
    counts = {key: {"S_a": 0, "S_b": 0, "S_c": 0, "ogs_at_level": 0} for key in sets}
    focal = {lname: tuple(f + "." for f in lin["focal"].split("|")) for lname, lin in LINEAGES.items()}
    with open(EGG) as fh:
        for line in fh:
            lvl, rest = line.split("\t", 1)
            if lvl not in by_level:
                continue
            f = rest.rstrip("\n").split("\t")
            sp = f[3].split(",")
            prots = f[4]
            for key, i, o in by_level[lvl]:
                c = counts[key]
                c["ogs_at_level"] += 1
                has_i = has_o = False
                for s in sp:
                    if not has_i and s in i:
                        has_i = True
                    elif not has_o and s in o:
                        has_o = True
                    if has_i and has_o:
                        break
                if has_i and has_o:
                    c["S_a"] += 1
                    nf = sum(prots.count("," + p) + prots.startswith(p) for p in focal[key[0]])
                    if nf:
                        c["S_b"] += nf
                        c["S_c"] += 1
    return counts


def main():
    t0 = time.time()
    levels = relevant_levels()
    species = pass1(levels)
    print(f"pass 1: {len(species)} species at relevant levels ({time.time() - t0:.0f} s)", flush=True)
    lin_of = taxonomy.lineages(int(s) for s in species)
    sets = node_sets(species, lin_of)
    counts = pass2(sets)
    print(f"pass 2 done ({time.time() - t0:.0f} s)", flush=True)
    out = {"source": "eggNOG 6.0 e6.og2seqs_and_species.tsv", "deviations": DEVIATIONS,
           "species_at_relevant_levels": len(species), "lineages": {}}
    for lname, lin in LINEAGES.items():
        out["lineages"][lname] = [
            {"node": node, "level": lvl, "n_ingroup_species": len(sets[(lname, node)][0]),
             "n_outgroup_species": len(sets[(lname, node)][1]), **counts[(lname, node)]}
            for node, lvl, _, _ in lin["nodes"]]
    with open(ROOT / "results" / "genecontent_counts.json", "w") as fh:
        json.dump(out, fh, indent=2)
    print("wrote results/genecontent_counts.json")


if __name__ == "__main__":
    main()
