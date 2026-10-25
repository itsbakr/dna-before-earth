"""Download the external datasets used by WP3 into data/external/ and record a manifest.

Raw files are git-ignored: TimeTree's terms forbid redistribution, and other sources have their own
licences. Only derived summary statistics are committed.
"""

import datetime as dt
import hashlib
import json
import sys
import urllib.request
from pathlib import Path

ROOT = Path(__file__).resolve().parent.parent
EXT = ROOT / "data" / "external"

GOAT = ("https://goat.genomehubs.org/api/v2/search?query=tax_tree%282759%29%20AND%20tax_rank%28species%29"
        "%20AND%20genome_size&result=taxon&fields=genome_size%2Cc_value&taxonomy=ncbi&size=50000"
        "&includeEstimates=false&excludeAncestral%5B0%5D=genome_size&excludeDescendant%5B0%5D=genome_size"
        "&tidyData=false")

SOURCES = {
    "goat/eukaryote_genome_size_direct.tsv": (GOAT, {"Accept": "text/tab-separated-values"}),
    "timetree/TimetreeOfLife2015.nwk": ("https://timetree.org/public/data/TimetreeOfLife2015.nwk", {}),
    "timetree/TT6_Tetrapods.nwk": ("https://timetree.org/downloads/biodiversity/TT6_Tetrapods.nwk", {}),
    "timetree/TT6_Tetrapods_tip_metrics.csv":
        ("https://timetree.org/downloads/biodiversity/TT6_Tetrapods_tip_metrics.csv", {}),
    "gtdb/VERSION.txt": ("https://data.gtdb.ecogenomic.org/releases/latest/VERSION.txt", {}),
    "gtdb/bac120_metadata.tsv.gz": ("https://data.gtdb.ecogenomic.org/releases/latest/bac120_metadata.tsv.gz", {}),
    "gtdb/ar53_metadata.tsv.gz": ("https://data.gtdb.ecogenomic.org/releases/latest/ar53_metadata.tsv.gz", {}),
    "eggnog/e6.og2seqs_and_species.tsv":
        ("https://eggnog6.embl.de/download/eggnog_6.0/e6.og2seqs_and_species.tsv", {}),
    "ncbi/new_taxdump.tar.gz": ("https://ftp.ncbi.nlm.nih.gov/pub/taxonomy/new_taxdump/new_taxdump.tar.gz", {}),
}


def fetch(rel, url, headers):
    dest = EXT / rel
    dest.parent.mkdir(parents=True, exist_ok=True)
    req = urllib.request.Request(url, headers={"User-Agent": "dna-before-earth/0.1", **headers})
    with urllib.request.urlopen(req, timeout=600) as r, open(dest, "wb") as fh:
        while chunk := r.read(1 << 20):
            fh.write(chunk)
    return {"file": rel, "url": url, "retrieved": dt.date.today().isoformat(),
            "bytes": dest.stat().st_size, "sha256": hashlib.sha256(dest.read_bytes()).hexdigest()}


def main(names):
    manifest_path = EXT / "manifest.json"
    manifest = json.loads(manifest_path.read_text()) if manifest_path.exists() else {}
    for rel, (url, headers) in SOURCES.items():
        if names and not any(n in rel for n in names):
            continue
        print("fetching", rel)
        manifest[rel] = fetch(rel, url, headers)
    manifest_path.write_text(json.dumps(manifest, indent=2))


if __name__ == "__main__":
    main(sys.argv[1:])
