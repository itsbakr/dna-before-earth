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

**Important metric difference**: Sharov measured *functional non-redundant* genome --
the fraction of the genome that is coding + regulatory (e.g., human = 3.2 Gbp x 15%
= 480 Mbp). Markov measured *minimal genome size (MGS)* -- the total genome of the
smallest free-living species in each taxonomic group (e.g., bat = 1,695 Mbp total).
These are conceptually different metrics. Sharov's metric estimates how much of the
genome *does work*. Markov's metric finds the *smallest total genome* in each group.
Both track biological complexity, and both independently produce pre-Earth origins,
but they should not be treated as directly comparable numbers.

## Extended Dataset (This Study) -- 6 Additional Taxa

| Taxon | Time (Bya) | Genome (Mb) | Species | Source |
|-------|-----------|-------------|---------|--------|
| Cyanobacteria | 2.7 | 1.44 | *Prochlorococcus marinus* | GenBank |
| Red algae | 1.6 | 13.7 | *Cyanidioschyzon merolae* | GenBank |
| Fungi | 1.0 | 9.2 | *Ashbya gossypii* | GenBank |
| Land plants | 0.47 | 82 | *Genlisea tuberosa* | Published genome |
| Insects | 0.4 | 99 | *Belgica antarctica* | Published genome |
| Flowering plants | 0.14 | 63 | *Utricularia gibba* | Published genome |

**Methodological note**: Sharov (2006) deliberately excluded plants from his analysis,
writing: *"I have not included plants into this graph for the following two reasons.
First, their genomes are often highly redundant due to polyploidy, which makes it
difficult to estimate the size of the functional non-redundant fraction. Second,
functional non-redundant genomes in plants did not increase as fast as in vertebrates,
and our goal was to trace the genomes in best performing groups of organisms."*

Our extended dataset includes plants, fungi, and insects to test whether expanding
beyond the "leading edge" lineage affects the result. It does not -- the trend
strengthens. However, we acknowledge this is a departure from Sharov's original
selection criteria. The core 5-point (Sharov) and 9-point (Markov) analyses are
unaffected by this choice.

## Verification Checklist

- [x] Pelagibacter ubique HTCC1062: 1,308,759 bp (NCBI Genome ID 491) -- matches 1.3 Mb
- [x] Mycoplasma genitalium: 580,070 bp (Fraser et al. 1995, Science 270:397)
- [x] Oldest stromatolites: ~3.48 Bya (Dresser Formation, Pilbara, Western Australia)
- [x] Markov et al. published in Paleontological Journal, Russian Academy of Sciences
- [x] All fossil dates consistent with standard paleontological consensus
- [x] Adami "how not to analyze data" quote verified verbatim from Biology Direct open review
- [ ] Minor regression coefficient discrepancy: Sharov reports 8.64 + 0.89x (R²=0.97, 7.8x/Byr);
      we get 8.592 + 0.877x (R²=0.967, 7.5x/Byr). Likely due to rounding of data points.
      Both produce origin ~10 Bya. Flagged, not hidden.

## Probability Calculation Note

Sharov states spontaneous assembly probability for 400 bp DNA as p = 10^-126.
Our calculation for a *specific* 400 bp sequence: (1/4)^400 = 10^-241.
The discrepancy (10^-126 vs 10^-241) likely reflects Sharov allowing for sequence
degeneracy (many possible functional sequences, not just one specific one) or
calculating physical assembly probability rather than information-theoretic sequence
probability. Both numbers represent astronomically low probabilities. Our README uses
both estimates where relevant.
