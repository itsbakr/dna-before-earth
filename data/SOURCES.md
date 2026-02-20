# Data Sources and Provenance

Every data point in this analysis has a traceable chain of provenance. This is essential:
if the data cannot be challenged, the argument cannot be dismissed on data grounds alone.

## Primary Databases Used

| Database | Maintained By | URL | Standard? |
|----------|--------------|-----|-----------|
| NCBI GenBank | National Center for Biotechnology Information, NIH | https://www.ncbi.nlm.nih.gov/genbank/ | Yes, universal standard |
| Animal Genome Size Database | T. Ryan Gregory, University of Guelph | https://www.genomesize.com/ | Yes, standard reference |
| Published genome sequences | Various (cited per data point) | Various journals | Peer-reviewed |

**These are the same databases used by every evolutionary biologist worldwide
for phylogenetics, divergence dating, and comparative genomics.**

## Sharov (2006) -- 5 Data Points

Source: Sharov, A.A. (2006). "Genome increase as a clock for the origin and evolution
of life." *Biology Direct*, 1:17. doi:10.1186/1745-6150-1-17
[PMC1526419](https://pmc.ncbi.nlm.nih.gov/articles/PMC1526419/)

| Organism | Time (Bya) | Genome (bp) | Species | Source | Notes |
|----------|-----------|-------------|---------|--------|-------|
| Prokaryotes | 3.5 | 5 x 10^5 | *Nanoarchaeum equitans* / *Mycoplasma genitalium* | GenBank | Parasitic -- smallest known at the time. Sharov acknowledged this gives conservative estimate |
| Eukaryotes | 2.0 | 2.9 x 10^6 | *Encephalitozoon cuniculi* | GenBank | Intracellular parasite -- reduced genome |
| Worms | 1.0 | 7.3 x 10^7 | *Caenorhabditis elegans* | GenBank | Model organism, ~75% functional (9.7x10^7 total) |
| Fish | 0.5 | 1.3 x 10^8 | *Takifugu rubripes* | GenBank | Known compact genome (4x10^8 total, ~1/3 gene loci) |
| Mammals | 0.0 (present) | 4.8 x 10^8 | *Homo sapiens* | GenBank | ~15% functional (transposon-free fraction of 3.2x10^9) |

**Fossil dates**: Standard paleontological consensus, molecular clock estimates
(Hedges et al. 2004, Feng et al. 1997, Seilacher et al. 1998, Furnes et al. 2004).

**Critical note from Sharov's own text**: "Prokaryotes and eukaryotes with the smallest
genome are parasitic and may have a reduced genome size due to parasitism. However I
selected them to get the most conservative estimate for the time elapsed since the origin
of life." (Sharov 2006, Results section)

## Markov, Anisimov & Korotayev (2010) -- 9 Data Points

Source: Markov, A.V., Anisimov, V.A. & Korotayev, A.V. (2010). "Relationship between
genome size and organismal complexity in the lineage leading from prokaryotes to mammals."
*Paleontological Journal*, 44:363-373. doi:10.1134/S0031030110040015

| Group | MGS (Mb) | Time (Ma) | Species | Source |
|-------|----------|-----------|---------|--------|
| All living beings (Bacteria) | 1.3 | 4,000 | *Pelagibacter ubique* HTCC1062 | GenBank (1,308,759 bp verified) |
| Eukaryotes | 9.2 | 2,000 | *Ashbya gossypii* | GenBank |
| Animals (Metazoa) | 19.6 | 1,250 | *Pratylenchus coffeae* | Animal Genome Size Database |
| Chordates | 68.6 | 575 | *Oikopleura dioica* | GenBank |
| Vertebrates | 342 | 540 | *Tetraodon fluviatilis* | GenBank |
| Tetrapods | 931 | 375 | *Limnodynastes ornatus* | Animal Genome Size Database |
| Amniotes | 951 | 315 | *Phasianus colchicus* | Animal Genome Size Database |
| Mammals | 1,695 | 220 | *Miniopterus schreibersi* | Animal Genome Size Database |
| Primates | 2,215 | 65 | *Callicebus torquatus* | Animal Genome Size Database |

**Critical differences from Sharov**:
- Used **free-living organisms only** (not parasitically reduced)
- Used **minimal genome size (MGS)** within each taxonomic group
- Genome sizes are **2.6x to 3.2x larger** than Sharov's early points
- Result: origin pushed **further back** (10.9 Bya vs 9.8 Bya)

## Extended Dataset (This Study) -- 6 Additional Taxa

| Taxon | Time (Bya) | Genome (Mb) | Species | Source |
|-------|-----------|-------------|---------|--------|
| Cyanobacteria | 2.7 | 1.44 | *Prochlorococcus marinus* | GenBank |
| Red algae | 1.6 | 13.7 | *Cyanidioschyzon merolae* | GenBank |
| Fungi | 1.0 | 9.2 | *Ashbya gossypii* | GenBank |
| Land plants | 0.47 | 82 | *Genlisea tuberosa* | Published genome |
| Insects | 0.4 | 99 | *Belgica antarctica* | Published genome |
| Flowering plants | 0.14 | 63 | *Utricularia gibba* | Published genome |

## Verification Checklist

- [x] Pelagibacter ubique HTCC1062: 1,308,759 bp (NCBI Genome ID 491) -- matches 1.3 Mb
- [x] Mycoplasma genitalium: 580,070 bp (Fraser et al. 1995, Science 270:397)
- [x] Oldest stromatolites: ~3.48 Bya (Dresser Formation, Pilbara, Western Australia)
- [x] Markov et al. published in Paleontological Journal, Russian Academy of Sciences
- [x] All fossil dates consistent with standard paleontological consensus
