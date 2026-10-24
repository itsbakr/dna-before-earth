# Data Sources and Provenance

Every row in the CSV files in this folder carries its source. The analysis code in `clock/` reads these
files directly; no data values are typed into scripts. Columns ending in `_assumed` are uncertainty
values chosen for this project, not values reported by the original authors.

Corrections made in October 2026 are listed at the end. For the reasoning behind them see
`review/CRITIQUE_AND_RESEARCH_PLAN.md`.

## Primary databases

| Database | Maintained by | URL |
|----------|--------------|-----|
| NCBI GenBank / Datasets | National Center for Biotechnology Information, NIH | https://www.ncbi.nlm.nih.gov/datasets/ |
| Animal Genome Size Database | T. Ryan Gregory, University of Guelph | https://www.genomesize.com/ |
| Published genome papers | cited per row | |

## `sharov_2006.csv`: Sharov (2006), 5 points

Source: Sharov, A.A. (2006). Genome increase as a clock for the origin and evolution of life.
*Biology Direct* 1:17. doi:10.1186/1745-6150-1-17

| Group | Time (Gya) | Functional genome (bp) | Species |
|-------|-----------|-------------|---------|
| Prokaryotes | 3.5 | 5.0 x 10^5 | *Nanoarchaeum equitans* / *Mycoplasma genitalium* (both parasitic or symbiotic) |
| Eukaryotes | 2.0 | 2.9 x 10^6 | *Encephalitozoon cuniculi* (intracellular parasite) |
| Worms | 1.0 | 7.28 x 10^7 | *Caenorhabditis elegans* (75% of genome treated as functional) |
| Fish | 0.5 | 1.333 x 10^8 | *Takifugu rubripes* (gene loci about one third of 4 x 10^8) |
| Mammals | **0.125** | 4.8 x 10^8 | *Homo sapiens* (15% of 3.2 x 10^9 treated as functional) |

Sharov's printed regression: log10(y) = 8.64 + 0.89x, R² = 0.97, 7.8-fold per billion years.
Values are as reprinted in Markov et al. (2010, Table 1). Mammals are dated at 125 Ma (earliest placental
fossil), not at the present; the earlier version of this repo used 0.0, which is why its intercept
(8.59) did not match Sharov's (8.64). With 0.125 the fit gives 8.644 + 0.897x.

Sharov's own words on the parasites: "Prokaryotes and eukaryotes with the smallest genome are parasitic
and may have a reduced genome size due to parasitism. However I selected them to get the most
conservative estimate for the time elapsed since the origin of life."

## `markov_2010.csv`: Markov, Anisimov & Korotayev (2010), 9 points

Source: Markov, A.V., Anisimov, V.A. & Korotayev, A.V. (2010). Relationship between genome size and
organismal complexity in the lineage leading from prokaryotes to mammals. *Paleontological Journal*
44:363-373. doi:10.1134/S0031030110040015

Metric: minimal genome size (MGS), the smallest total genome among living members of each group.
The groups are nested (primates within mammals within amniotes, and so on).

- The first five rows (All living beings to Vertebrates) were checked against text from the paper.
  The last four rows come from the earlier version of this repo and are marked `verified_against_source = no`.
- **Not all species are free-living.** *Ashbya gossypii* is a plant pathogen of cotton, and
  *Pratylenchus coffeae* is a plant-parasitic nematode. The earlier claim that Markov et al. used
  "free-living organisms only" was wrong.
- Markov et al. fit a biexponential (hyperexponential) curve. No source found shows them estimating
  an origin-of-life date. Their preferred model has no finite crossing of 1 bp. Any origin date
  computed from this table is this project's own calculation.

## `extended_dataset.csv`: this project's extended set

Markov's rows plus additional taxa, with an `include` flag. Rows with `include = FALSE` are kept for
transparency and are excluded from analyses. `previous_value` shows the value used before correction.

Sharov deliberately excluded plants, which he said "did not increase as fast as in vertebrates". This
set includes plants, fungi and insects as a sensitivity analysis only; it mixes lineages and should not
be read as a single leading-edge series.

## `node_ages.csv`: published versus current clade ages

The ages used by Sharov, Markov and this repo, alongside current estimates. The `verification` column says
whether the current value was checked against an abstract or only a secondary source. Analyses run
with both the published ages and the current ages.

## Corrections log (October 2026)

| File | Change |
|------|--------|
| `sharov_2006.csv` | Mammals moved from 0.0 to 0.125 Gya (Sharov's own date). Worms 7.3e7 to 7.28e7, fish 1.3e8 to 1.333e8 (Sharov's values). The *M. genitalium* note no longer says "free-living". Uncertainty columns renamed `*_assumed`. |
| `markov_2010.csv` | Added `lifestyle` and `verified_against_source`. Removed the "free-living only" claim. |
| `extended_dataset.csv` | *Prochlorococcus* 1.44 to 1.658 Mb (MED4). *Cyanidioschyzon* 13.7 to 16.52 Mb and relabelled unicellular. Duplicate *Ashbya* "Fungi" row excluded. *Genlisea* (61 Mb, a flowering plant) removed from "earliest land plants" and used for flowering plants instead of the unsourced "63 Mb functional" *Utricularia* value. Added `include`, `previous_value` and `issue` columns. |
| `node_ages.csv` | New file. |

## Probability calculation note

Sharov states p = 10^-126 for "spontaneous self-assembly of a 400 bp DNA molecule". No derivation was
found; it is not (1/4)^400, which is about 10^-241. The random-assembly argument is not used in the
analysis code (see the review, Section 3.6).
