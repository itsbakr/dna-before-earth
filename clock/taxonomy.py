"""NCBI taxonomy lookups (scientific names and lineages) from the new_taxdump files."""

from pathlib import Path

NCBI = Path(__file__).resolve().parent.parent / "data" / "external" / "ncbi"


def scientific_names_to_taxids(wanted):
    """Map scientific names (with spaces) to NCBI taxids, for names in ``wanted`` only."""
    wanted = set(wanted)
    out = {}
    with open(NCBI / "names.dmp") as fh:
        for line in fh:
            parts = line.split("\t|\t")
            if parts[3].startswith("scientific name") and parts[1] in wanted:
                out[parts[1]] = int(parts[0])
    return out


def lineages(taxids):
    """Map each taxid to the set of its ancestor taxids (including itself)."""
    taxids = set(int(t) for t in taxids)
    out = {}
    with open(NCBI / "taxidlineage.dmp") as fh:
        for line in fh:
            tid, rest = line.split("\t|\t", 1)
            tid = int(tid)
            if tid in taxids:
                out[tid] = {int(x) for x in rest.strip().rstrip("|").split()} | {tid}
    return out
