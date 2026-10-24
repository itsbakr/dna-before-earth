# External datasets for WP3 and WP4 (not yet downloaded)

These sources are needed for the large-scale tests in the research plan
(`review/CRITIQUE_AND_RESEARCH_PLAN.md`, Sections 4.3 and 6). They could not be fetched from the
analysis environment because its network policy blocks the hosts below. To enable them, add the hosts
under **Allowed domains** in the environment's Network access settings
(https://code.claude.com/docs/en/cloud-environments#network-access).

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

Downloads will go in this folder with a manifest recording URL, date, release and checksum.
