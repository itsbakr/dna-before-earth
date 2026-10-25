"""WP3c: has the prokaryotic genome grown since LUCA?

Compares the genome-size distribution of modern prokaryote species (GTDB species representatives,
CheckM2 completeness >= 95%, contamination <= 5%) with the LUCA estimate of Moody et al. (2024):
at least 2.5 Mb (2.49 to 2.99 Mb) about 4.2 Gya. Writes results/prokaryotes.json.
"""

import json
from pathlib import Path

import numpy as np
import pandas as pd

ROOT = Path(__file__).resolve().parent.parent
GTDB = ROOT / "data" / "external" / "gtdb"
LUCA_MB = (2.49, 2.99)
COLS = ["accession", "checkm2_completeness", "checkm2_contamination", "genome_size",
        "gtdb_representative", "gtdb_taxonomy", "ncbi_genome_category"]
QUANTS = [0.01, 0.05, 0.25, 0.5, 0.75, 0.95, 0.99]


def load(name):
    df = pd.read_csv(GTDB / name, sep="\t", usecols=COLS, low_memory=False)
    df = df[(df.gtdb_representative.astype(str).str.lower().str.startswith("t"))
            & (df.checkm2_completeness >= 95) & (df.checkm2_contamination <= 5)].copy()
    df["size_mb"] = df.genome_size / 1e6 / (df.checkm2_completeness / 100)   # completeness-adjusted
    df["isolate"] = ~df.ncbi_genome_category.astype(str).str.contains("metagenome|single cell", case=False)
    return df


def describe(sizes):
    sizes = np.asarray(sizes)
    return {"n": int(len(sizes)), **{f"q{int(q * 100):02d}_mb": float(np.quantile(sizes, q)) for q in QUANTS},
            "max_mb": float(sizes.max()),
            "frac_below_luca_low": float(np.mean(sizes < LUCA_MB[0])),
            "frac_below_luca_high": float(np.mean(sizes < LUCA_MB[1]))}


def main():
    version = (GTDB / "VERSION.txt").read_text().split()[0]
    out = {"gtdb_version": version, "luca_mb_interval": LUCA_MB, "filters":
           "species representatives; CheckM2 completeness >= 95%, contamination <= 5%; size / completeness"}
    for domain, fname in [("bacteria", "bac120_metadata.tsv.gz"), ("archaea", "ar53_metadata.tsv.gz")]:
        df = load(fname)
        out[domain] = {"all": describe(df.size_mb), "isolates": describe(df[df.isolate].size_mb),
                       "metagenome_or_single_cell": describe(df[~df.isolate].size_mb)}
    both = pd.concat([load("bac120_metadata.tsv.gz"), load("ar53_metadata.tsv.gz")])
    out["all_prokaryotes_isolates"] = describe(both[both.isolate].size_mb)
    luca_log, modern_log = np.log10(2.5e6), np.log10(np.median(both[both.isolate].size_mb) * 1e6)
    out["implied_rate_luca_to_present_log10_per_gyr"] = float((modern_log - luca_log) / 4.2)
    (ROOT / "results").mkdir(exist_ok=True)
    with open(ROOT / "results" / "prokaryotes.json", "w") as fh:
        json.dump(out, fh, indent=2)
    print(json.dumps(out, indent=1))


if __name__ == "__main__":
    main()
