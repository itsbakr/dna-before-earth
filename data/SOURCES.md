# Data Sources and Provenance

Every row in the CSV files in this folder carries its source. The analysis code in `clock/` reads these
files directly; no data values are typed into scripts. Columns ending in `_assumed` are uncertainty
values chosen for this project, not values reported by the original authors.

All quotes below were checked against the full texts in October 2026 (Sharov 2006 via PMC; Markov et al.
2010 via the authors' English reprint in *History & Mathematics: Big History Aspects*, 2019, pp. 122-141).
For the reasoning behind the corrections see `review/CRITIQUE_AND_RESEARCH_PLAN.md`.

## Primary databases

| Database | Maintained by | URL |
|----------|--------------|-----|
| NCBI GenBank / Datasets | National Center for Biotechnology Information, NIH | https://www.ncbi.nlm.nih.gov/datasets/ |
| Animal Genome Size Database | T. Ryan Gregory, University of Guelph | https://www.genomesize.com/ |
| Published genome papers | cited per row | |

External datasets used in the real-data analyses (GoaT, TimeTree, NCBI Taxonomy, GTDB) are described in
`data/external/README.md`.

## `sharov_2006.csv`: Sharov (2006), 5 points

Source: Sharov, A.A. (2006). Genome increase as a clock for the origin and evolution of life.
*Biology Direct* 1:17. doi:10.1186/1745-6150-1-17

**Sharov prints no data table.** Each value comes from his prose (Results, paragraph 2), and some must be
computed:

| Group | Age used (Gya) | Functional genome (bp) | Sharov's wording |
|-------|-----------|-------------|---------|
| Prokaryotes | 3.5 | 5 x 10^5 | "existed on earth as early as 3.5 billion years ago"; *N. equitans* / *M. genitalium* |
| Eukaryotes | 2.05 | 2.9 x 10^6 | "appeared between 2.3 and 1.8 billion years ago ... (± 250 Mya)"; *E. cuniculi* |
| Worms | 1.0 | 9.7 x 10^7 x 75% = 7.275 x 10^7 | "existed at least for 1 billion years"; *C. elegans* |
| Fish | 0.5 | 4 x 10^8 / 3 = 1.333 x 10^8 | "existed 0.5 billion years ago"; fugu, "1/3 of it is occupied by gene loci" |
| Mammals | 0.10 | 3.2 x 10^9 x 15% = 4.8 x 10^8 | "Mammals (mouse, rat, and human), which appeared just recently in earth history"; no date given |

The eukaryote and mammal ages are read from his Fig. 1 (eukaryotes plotted at about 2.1, mammals at about
0.1). Eukaryotes at 2.05 (the midpoint of his range, also used by Marzban et al. 2014) with mammals at 0.10
reproduce all four printed statistics: log10(y) = 8.64 + 0.89x, R² = 0.97, 7.8-fold per Gyr.

The column `time_bya_markov_reprint` holds the ages in Markov et al. (2010, **Table 2**), which reprints
Sharov's data with eukaryotes at 2.0 and mammals at 0.125. The 125 Ma figure appears in Sharov only in his
plants paragraph ("flowering plants appeared simultaneously with mammals ca. 125 million years ago").
The gloss "earliest placental mammals" is Markov et al.'s (p. 128). With the reprint ages the fit matches
Sharov's intercept but not his slope, R² or fold change.

Sharov on the parasites: "Prokaryotes and eukaryotes with the smallest genome are parasitic and may have a
reduced genome size due to parasitism. However I selected them to get the most conservative estimate for
the time elapsed since the origin of life."

Sharov's sensitivity analysis (Results, paragraphs 4 and 5): varying points by ±300 Myr and ±0.3 log bp
gave 4.6 to 15.3-fold per Gyr, and "the date of life origin may vary from 7 to 13 billion years". The
often-quoted "±2.5 billion years" first appears in Sharov & Gordon (2013).

## `markov_2010.csv`: Markov, Anisimov & Korotayev (2010), 9 points

Source: Markov, A.V., Anisimov, V.A. & Korotayev, A.V. (2010). Relationship between genome size and
organismal complexity in the lineage leading from prokaryotes to mammals. *Paleontological Journal*
44:363-373. doi:10.1134/S0031030110040015

Metric: minimal genome size (MGS), the smallest total genome among living members of each group. The
groups are nested (primates within mammals within amniotes, and so on).

- All nine rows (values, ages and species) were checked against Table 1 (p. 125). `markov_description`
  gives the species as printed.
- **Selection criterion.** Markov et al. exclude only "intracellular symbionts and parasites" (p. 124;
  Table 1 header) and describe their group 1 and 2 species as free-living ("we use minimal genomes of
  free-living species", p. 128). By that criterion *Ashbya gossypii* (a plant pathogen) and *Pratylenchus
  coffeae* (a plant-parasitic nematode) qualify, since both are extracellular. Calling them parasites is our
  classification, recorded in `lifestyle_note`.
- **Fit statistics.** Their exponential fit reports "the Pearson's correlation coefficient ... (R2 = 0.914)";
  0.914 is r, and R² = 0.836. Their biexponential reports 0.979, also r (R² = 0.959 on the log scale). The
  printed biexponential constant C = 1.069 x 10^8 is a typo; refitting gives C of about 1.07 x 10^6 bp.
- **Origin of life.** They give no date of their own. They wrote that Sharov's "at least 7 Ga ... can be
  considered rather seriously (but only if such extrapolation itself is assumed to be reliable)"
  (pp. 128-129), and left extrapolation "beyond the scope of this paper" (p. 136). Any origin date computed
  from this table is this project's own calculation.

## `extended_dataset.csv`: this project's extended set

Markov's rows plus additional taxa, with an `include` flag. Rows with `include = FALSE` are kept for
transparency and are excluded from analyses. `previous_value` shows the value used before correction.

Sharov excluded plants for two reasons (Results, paragraph after Fig. 1): "First, their genomes are often
highly redundant due to polyploidy, which makes it difficult to estimate the size of the functional
non-redundant fraction. Second, functional non-redundant genomes in plants did not increase as fast as in
vertebrates, and our goal was to trace the genomes in best performing groups of organisms." This set
includes plants, fungi and insects as a sensitivity analysis only; it mixes lineages and should not be read
as a single leading-edge series.

## `node_ages.csv`: published versus current clade ages

The ages used by Sharov, Markov and this repo, alongside current estimates. The `verification` column says
whether the current value was checked against an abstract or only a secondary source. Analyses run with
both the published ages and the current ages.

## Corrections log (October 2026)

| File | Change |
|------|--------|
| `sharov_2006.csv` | Ages set to those that reproduce Sharov's printed regression (eukaryotes 2.05, mammals 0.10; earlier versions used 2.0 and 0.0). Markov et al.'s reprint ages (2.0, 0.125) kept as a second column. Worms and fish computed exactly from Sharov's text. Mammals are "mouse, rat, and human", not *Homo sapiens* alone. Uncertainty columns renamed `*_assumed`. |
| `markov_2010.csv` | All rows verified against Table 1. Added the printed species descriptions and a lifestyle note; the earlier repo text that Markov used "free-living organisms only" paraphrases Markov's own wording, which excludes only intracellular parasites. |
| `extended_dataset.csv` | *Prochlorococcus* 1.44 to 1.658 Mb (MED4). *Cyanidioschyzon* 13.7 to 16.52 Mb and relabelled unicellular. Duplicate *Ashbya* "Fungi" row excluded. *Genlisea* (61 Mb, a flowering plant) removed from "earliest land plants" and used for flowering plants instead of the unsourced "63 Mb functional" *Utricularia* value. Added `include`, `previous_value` and `issue` columns. |
| `node_ages.csv` | New file. |

## Probability calculation note

Sharov states p = 10^-126 "for 400 bp DNA" (Discussion, paragraph on the RNA world: "Spontaneous
self-assembly of such a complex system had an extremely low probability even if all components were
immediately available and brought together"). The full text gives no derivation; the figure is not
(1/4)^400, which is about 10^-241. The random-assembly argument is not used in the analysis code (see the
review, Section 3.6).
