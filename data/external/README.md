# External datasets for WP3 and WP4 (not yet downloaded)

These sources feed the real-data analyses (WP3). Download them with `make fetch`
(`scripts/fetch_data.py`), which writes `manifest.json` with each file's URL, retrieval date and SHA-256.
Raw files are git-ignored and must not be redistributed: TimeTree's terms forbid redistribution of its
data and transformations, and the other sources have their own licences. Only derived summary
statistics (`results/realdata.json`, `results/prokaryotes.json`) are committed.

Status (2026-10-25): GoaT, TimeTree (2015 Timetree of Life; TimeTree 6 tetrapods), NCBI taxonomy and
GTDB R232 are downloaded and used. eggNOG, OrthoDB, Open Tree and the fossil cell-size tables are
reachable but not yet used (WP4).

| Dataset | What we need from it | Host(s) to allow |
|---|---|---|
| Genomes on a Tree (GoaT) | Genome size (C-value and assembly span) for all eukaryotes, with NCBI taxids | `goat.genomehubs.org` |
| NCBI Datasets / Taxonomy | Assembly statistics; taxid lineages for joining everything | `api.ncbi.nlm.nih.gov`, `ftp.ncbi.nlm.nih.gov`, `www.ncbi.nlm.nih.gov` |
| GTDB R11-RS232 | Prokaryote genome sizes with CheckM completeness; GTDB trees | `data.gtdb.ecogenomic.org` |
| TimeTree 5 | Divergence times with confidence intervals | `timetree.org` |
| Open Tree of Life | Synthetic topology for the WP2 simulations on the real tree | `api.opentreeoflife.org`, `files.opentreeoflife.org` |
| Animal Genome Size Database | C-values for animals (cross-check of GoaT) | `www.genomesize.com` |
| Kew Plant DNA C-values | C-values for plants | `cvalues.science.kew.org` |
| eggNOG 6 | Hierarchical orthologous groups for ancestral gene content | `eggnog6.embl.de` |
| OrthoDB v12 | Alternative orthology for ancestral gene content | `data.orthodb.org`, `www.orthodb.org` |
| Zenodo / Dryad / journal supplements | LUCA proteome (Moody et al. 2024), consensus LUCA (Crapitto et al. 2022), fossil cell-size tables | `zenodo.org`, `datadryad.org`, `static-content.springer.com` |
| Full texts for citation checks | Sharov 2006, Marzban 2014, Markov 2010, Sharov & Gordon 2013/2018 | `pmc.ncbi.nlm.nih.gov`, `biologydirect.biomedcentral.com`, `arxiv.org`, `link.springer.com` |

