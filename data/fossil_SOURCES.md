# Fossil genome-size data: sources and provenance

This note documents `fossil_genome_size.csv`, a dataset of genome sizes estimated from fossils. It was compiled
for a re-test of Sharov's (2006) genome-complexity clock. All sources were accessed on 2026-10-25. The note
contains no trend analysis.

Every number in the CSV was read from a file that was downloaded and opened: a PDF, an HTML table, a supplementary
spreadsheet, a figure image, or a JSON response from the Paleobiology Database (PBDB) API. Values were extracted by
script, not retyped. Where a number was derived, `value_type` or `notes` says how. The extraction scripts and the
downloaded files were kept outside the repository, because only these two files were to be written.

## Column conventions

| Column | Meaning |
|---|---|
| `taxon` | Name as printed by the source. Footnote markers, underscores and trailing spaces were removed from Simonin & Roddy names; the printed form is kept in `notes`. |
| `higher_clade` | Coarse clade label added for this dataset. For Simonin & Roddy rows it is their `clade` column. |
| `lineage_group` | One of the seven analysis groups in the brief. |
| `age_ma`, `age_min_ma`, `age_max_ma` | See "Ages" below. |
| `genome_size_pg` | Haploid nuclear DNA content (1C, pg) as estimated by the source. Empty for relative proxies. |
| `genome_size_low_pg`, `genome_size_high_pg` | The source's ±1 SD (or ±1σ) interval when one exists. Empty otherwise. |
| `value_type` | Applies to `genome_size_pg`: `reported` (printed in a table or text), `digitized` (read from a figure). For relative-proxy rows it applies to the proxy value in `notes`. No `computed` genome sizes were needed. Computed ages and ±SD bounds are flagged in `notes`. |
| `extant_calibration` | TRUE for living species that the source used to fit the cell-size-genome-size regression. They are at age 0 and are not fossil estimates. |
| `notes` | Alternative estimates, raw proxy data (lacuna volumes), age provenance and flags. Relative proxies appear as `relative_proxy=<measure>:<value>`. |

### Ages

- **Organ et al. 2007.** The paper prints no ages. `age_ma` is the tip age of each fossil in the time-scaled
  Supplementary Tree 2: 346.0 Myr minus the root-to-tip branch length. This is computed from the printed tree. Extant
  tips fall at 345.6-346.0, so tips carry about ±0.4 Myr of non-ultrametricity, and the SI says ages follow the 2004
  geologic time scale. `age_min_ma`/`age_max_ma` give the PBDB stratigraphic range of the taxon name. This is the
  range of all occurrences of the taxon, not of the sampled specimen. 16 rows are flagged `AGE CONFLICT` where the tree
  tip falls outside the PBDB range. Most of these are under 3 Myr and reflect the 2004 versus 2024 time scales
  (for example the K-Pg at 65.5 versus 66.0 Ma, and Campanian stage boundaries). Larger conflicts are
  *Psittacosaurus mongoliensis* (tip 99.7 Ma, PBDB 121.4-110.1), *Herrerasaurus* (221.1 vs 237-227.3),
  *Hypacrosaurus stebingeri* (67.3 vs 83.6-72.2) and *Euoplocephalus* (65.2 vs 83.6-72.2).
- **Organ et al. 2009.** The paper prints no ages. `age_min_ma`/`age_max_ma` give the PBDB range and `age_ma` is its
  midpoint (computed).
- **Organ et al. 2016.** Table 1 prints an epoch (for example "Early Permian"), and the text gives the formation or
  stage for some taxa (Escuminac Fm., Frasnian; Britta Dal Fm., Famennian; Richards Spur, Artinskian; "Upper
  Tatarian"). The range is the corresponding interval in the ICS International Chronostratigraphic Chart v2024/12, as
  served by the PBDB intervals API (Cohen, Finney, Gibbard & Fan, ICS 2024). `age_ma` is the midpoint (computed). For
  the four taxa carried over from Organ et al. 2011, which was not accessed, no age is printed. Fig. 2 places their
  tips in the Permian band. For these, the PBDB genus range is used, or the whole Permian for the unidentified basal
  sauropsid.
- **Laurin et al. 2016.** The range is as printed ("Bathonian, 166-168 Ma"). `age_ma` is the midpoint.
- **Simonin & Roddy 2018.** The single `age` value is from their S1 Data; S1 Fig labels the axis "Time before present
  (millions of years)". No range is given.
- **Extant calibrators.** All are set to 0.

### One row per fossil taxon

Each fossil taxon appears once, with one exception: duplicate names inside the Simonin & Roddy compilation are kept,
flagged and cross-referenced (see below). When two sources estimate the same fossil, the row uses the estimate
printed with an uncertainty, and the other estimate is given in `notes`. Two taxa are affected:

- *Apatosaurus*: the row uses Organ et al. 2009 (2.31 ± 0.44 pg). Organ et al. 2007 gave 2.22 pg from the same
  lacuna data.
- *Marmorerpeton*: the row uses Laurin et al. 2016 (36.7 pg, printed). The Organ et al. 2016 Fig. 1A re-estimate is
  39.4 pg (digitized).

Extant calibrators are listed per source, because each source has its own calibration set. No extant species is
listed twice.

## Sources used for rows

### 1. Organ, Shedlock, Meade, Pagel & Edwards 2007

Organ CL, Shedlock AM, Meade A, Pagel M, Edwards SV (2007). Origin of avian genome size and structure in non-avian
dinosaurs. *Nature* 446:180-184. doi:10.1038/nature05621

- **Accessed.** The Supplementary Information PDF (41586_2007_BFnature05621_MOESM403_ESM.pdf, 27 pp.) from the
  Springer static-content server. The main article is paywalled, so only its abstract and figure legends were read.
- **Used.**
  - Supplementary Table 4 ("Summary of Inferences for Dinosaurs"): genome size mean for 31 taxa. 30 rows are used;
    *Apatosaurus* is taken from Organ et al. 2009, see above.
  - Supplementary Table 1: lacuna volumes for all taxa and C-values of the 26 extant calibrators. 26 calibrator rows.
  - Supplementary Tree 2 (Newick with branch lengths in Myr): tip ages.
  - Supplementary Tables 2, 3, 7 and 8: checks.
- **Proxy.** Osteocyte lacunae measured on 2D thin sections at ×200 (length and width of the larger lacunae;
  ellipsoid volume 4/3·π·r_w²·r_l). 825 lacunae from 26 extant species and 598 from the extinct taxa.
- **Calibration.** Bayesian phylogenetic GLS (BayesTraits/Continuous) of ln C-value on ln lacuna volume, with
  posterior predictive estimates for the fossils. Supplementary Table 3 gives posterior means α = −0.87 and β = 0.36
  (GLS R² = 0.32, n = 26 extant). That is, **ln C ≈ −0.87 + 0.36 ln V**. The Bayes factor for the correlation is 9.9;
  κ = 2.09, δ = 1.3, λ = 0.67. In leave-one-out tests (Supplementary Table 2), five extant species were predicted
  within 2-15%, with Bayesian SD 0.30-1.27 pg.
- **Caveats specific to this source.**
  - The "95% CI" printed in Table 4 (0.001-0.007 pg) is far narrower than the predictive SD. It appears to be Monte
    Carlo precision of the posterior mean, so `genome_size_low_pg`/`genome_size_high_pg` are left empty.
  - Supplementary Table 8 lists "Ln Genome Size" values for the extinct taxa that do not equal ln of the Table 4
    means. For example, Triceratops is exp(1.440) = 4.22 against 3.31. Each row's `notes` carries the Table 8 value.
  - Table 8 also appears to swap *Bos taurus* and *Canis familiaris*.
  - Table 1 gives *Meleagris* 1.54 pg; Table 2 gives 1.45 pg.
  - Bone elements differ between taxa (femur, tibia, skull, vertebra, "fragment").
  - Sample sizes are 8-40 lacunae.

### 2. Organ, Brusatte & Stein 2009

Organ CL, Brusatte SL, Stein K (2009). Sauropod dinosaurs evolved moderately sized genomes unrelated to body size.
*Proc R Soc B* 276:4303-4308. doi:10.1098/rspb.2009.1343 (PMC2817110)

- **Accessed.** The PMC full-text HTML. The electronic supplementary material was not accessed (see below).
- **Used.** Table 1 (10 sauropodomorphs: specimen, element, n, lacuna volume, C-value mean and s.d.). 10 rows.
  `genome_size_low_pg`/`genome_size_high_pg` are mean ∓ 1 s.d. (computed). The printed mean of the 10 is 2.02 pg
  (s.d. 0.41).
- **Calibration.** The same Bayesian approach, with 38 extant species from Organ & Shedlock 2009. The paper says the
  regression "did not differ from previous work". Organ & Shedlock (2009, Fig. 1a legend) print
  **ln genome size = −0.81 + 0.35 ln cell size**, r² = 0.43, n = 38.
- **Caveats specific to this source.**
  - *Saturnalia*'s s.d. is 0.282 in Table 1 but 0.82 in the Results text.
  - The *Barosaurus* specimen number "T16a" looks like Tendaguru material, while the text names *B. lentus*.

### 3. Organ, Struble, Canoville, de Buffrénil & Laurin 2016

Organ C, Struble M, Canoville A, de Buffrénil V, Laurin M (2016). Macroevolution of genome size in sarcopterygians
during the water-land transition. *C R Palevol* 15:65-73. doi:10.1016/j.crpv.2015.09.003

**Attribution note.** This is the paper with "eight taxa … between 3.2 and 3.9 pg" that the brief attributes to
Laurin et al. 2016. Laurin et al. 2016 (pp. 74-82) is the *Marmorerpeton* paper, entry 4 below.

- **Accessed.** The open PDF from MNHN Science Press (sciencepress.mnhn.fr). It has no supplementary data.
- **Used.**
  - Table 1: lacuna volumes, epoch ages, and C-values of 4 new extant calibrators. 4 calibrator rows.
  - Fig. 1B: retrodicted genome sizes ± 1 SD for 12 extinct taxa, **digitized** (12 rows).
  - Fig. 1A: *Marmorerpeton*, given in notes only.
  - Fig. 2: period placement of the four taxa from 2011.
  - **No table of fossil genome-size estimates exists in this paper.**
- **Digitizing method.**
  - Fig. 1 was extracted with `pdfimages` (1160 × 2202 px).
  - The y-axis was calibrated by linear fit to the white gridlines at 1, 2, 3, 4 and 5 pg inside the bars: 76.0 px per
    pg, maximum residual 0.005 pg.
  - The bar top is the 50% crossing between background and bar fill, interpolated below one pixel, on a column 8 px
    in from the bar edge to avoid the central error bar.
  - Error-bar caps are the centre row of the cap stroke.
  - Reading precision is about ±0.02 pg.
  - Validation: the *Latimeria* bar reads 4.34 pg, matching 4.34 pg in Table 1, and cap midpoints agree with bar tops
    within 0.01 pg except for *Ichthyostega* and *Wetlugasaurus*.
  - For those two, the bar top coincides with the 4-pg gridline and reads 4.00. The cap midpoints (4.02) are probably
    better.
- **Calibration.** BayesTraits phylogenetic multiple regression of log genome size on log lacuna volume, with a dummy
  variable separating urodeles, on 62 extant species. Printed posteriors are slope β2 μ = 0.60 (σ 0.21), interaction
  β4 μ = −0.35 (σ 0.22), r² μ = 0.59 and λ μ = 0.79. **Intercepts are not printed**, so the equation cannot be
  reconstructed. Back-transformation adds MSE/2 (antilog bias correction), so values run slightly higher than in
  Laurin et al. 2016.
- **Caveats specific to this source.**
  - The digitized *Ichthyostega* and *Wetlugasaurus* values (4.00-4.02 pg) exceed the abstract's stated range
    "3.2-3.9 pg".
  - The Introduction gives *Latimeria* as 3.61 pg, but Table 1 gives 4.34 pg.
  - *Cardiocephalus*, *Diplocaulus*, *Mycterosaurus* and the unidentified basal sauropsid are 2016 re-estimates from
    Organ et al. 2011 data, which was not accessed. The sauropsid has no name and no printed age.
  - *Mycterosaurus* (a varanopid) is placed with synapsids in Fig. 2; varanopid affinity is debated.
  - Sample sizes are as small as n = 8 lacunae (*Ichthyostega*).

### 4. Laurin, Canoville, Struble, Organ & de Buffrénil 2016

Laurin M, Canoville A, Struble M, Organ C, de Buffrénil V (2016). Early genome size increase in urodeles.
*C R Palevol* 15:74-82. doi:10.1016/j.crpv.2014.12.006

- **Accessed.** The open PDF and the SOM spreadsheet (raw lacuna measurements, 1-s2.0-S1631068315000111-mmc11.xls)
  from MNHN Science Press.
- **Used.**
  - Results text: *Marmorerpeton* ln C = 3.6, σ = 0.19, "about 36.7 pg, with σ encompassing values ranging from 30.2
    pg to 44.2 pg". 1 row.
  - Abstract: the age ("Bathonian, 166-168 Ma").
  - Table 4: lacuna volumes.
  - Discussion: the C-value of *Ambystoma mexicanum*, 21.40 pg. 1 calibrator row. The other two calibrators added in
    this paper (*Andrias japonicus*, *Cryptobranchus alleganiensis*) have no printed C-value and are omitted.
- **Calibration.** BayesTraits ln-ln multiple regression with a urodele dummy variable on 57 taxa (full data set):
  posterior r² = 0.6, λ = 0.76. On the long-bone-only data set (n = 36), the urodele slope is 0.67 and the non-urodele
  slope 0.25. **Intercepts are not printed.** The paper also gives a node estimate for the *Marmorerpeton* + urodele
  ancestor (ln C 3.5, about 33.1 pg); it is not included because it is not a fossil taxon.
- **Caveats specific to this source.**
  - Peripheral lacunae are larger and darker, which may be a permineralization artefact or reflect ontogeny.
  - The specimens are probably juveniles.

### 5. Simonin & Roddy 2018 (relative proxy only)

Simonin KA, Roddy AB (2018). Genome downsizing, physiological novelty, and the global dominance of flowering plants.
*PLoS Biol* 16:e2003706. doi:10.1371/journal.pbio.2003706 (PMC5764239, open access)

- **Accessed.** The full text (Europe PMC XML) and the supplementary files (Europe PMC supplementaryFiles endpoint),
  including S1 Data (pbio.2003706.s003.xlsx) and S1 Fig.
- **Used.** S1 Data, sheet "Fossil Data": all 210 records with a guard-cell length (`lg`); 387 records with only
  stomatal or vein density were skipped. `genome_size_pg` is empty, and `notes` carries
  `relative_proxy=guard_cell_length_um:<lg>` plus the original reference as given in S1 Data. Ages run 1.66-175 Ma.
  The fossil records are a compilation from the literature, in large part from Franks & Beerling 2009 and Beerling &
  Woodward 1997.
- **Scaling.** The authors do not convert fossil `lg` to pg. Their Table 1 gives standardized-major-axis fits for
  extant species on log10 data, of the form log10(lg, µm) = elevation + slope × log10(1C, pg):

  | Fit | Elevation | Slope | R² | n |
  |---|---|---|---|---|
  | All species | 1.43 | 0.272 | 0.544 | not printed |
  | Angiosperms | 1.438 | 0.294 | 0.497 | not printed |
  | Gymnosperms | 1.04 | 0.529 | 0.300 | not printed |
  | Ferns | 1.15 | 0.489 | 0.514 | not printed |
  | Phylogenetic SMA | 1.27 | 0.371 | 0.370 | not printed |

  Any conversion to pg is therefore the analyst's own step.
- **Caveats specific to this source.**
  - 123 of 210 `lg` values carry many decimals (for example 27.777…, 34.7027…). They look converted from another
    stomatal measure; the conversion is not documented. Each such row is flagged.
  - 59 rows share a taxon name with another row. Some disagree badly: *Pseudofrenelopsis dalatzensis* at 140 Ma
    appears with lg = 42.5, 104.0 and 170 µm. Each row lists its duplicates.
  - 17 values exceed 100 µm, while S1 Fig b clips the axis at 100.
  - Ages are single values without uncertainty.
  - Clade labels are inconsistent ("Cycad"/"cycad", "conifer"/"Gymnosperm").
  - There are no Paleozoic records.

## Sources accessed but not used for rows

| Source | What was read | Why no rows |
|---|---|---|
| **Organ CL, Shedlock AM (2009)**. Palaeogenomics of pterosaurs and the evolution of small genome size in flying vertebrates. *Biol Lett* 5:47-50. doi:10.1098/rsbl.2008.0491 (PMC2657748) | Main text (PMC HTML) and Fig. 2 image | Per-taxon estimates for 4 pterosaurs and 7 basal archosauromorphs are in ESM table 3, which was not reachable. The text gives only group means: pterosaurs 2.0 pg (σ 0.08), basal archosauromorphs 3.07 pg (σ 0.75). The Fig. 2a bar chart is 452×395 px with unlabeled bars, so it cannot be digitized per taxon. |
| **Franks PJ, Freckleton RP, Beaulieu JM, Leitch IJ, Beerling DJ (2012)**. Megacycles of atmospheric carbon dioxide concentration correlate with fossil plant genome size. *Phil Trans R Soc B* 367:556-564. doi:10.1098/rstb.2011.0269 (PMC3248711) | Main text and figures (PMC) | Per-taxon fossil data are in ESM tables A1 (211 fossil species, guard-cell width) and A3 (30 fossil clades), which were not reachable. Fig. 5b plots 1C (pg, log10) for the 30 fossil clades against age (about 400-0 Ma) but **was not digitized**: the image is 518×470 px, points overlap at about 200, 140-120 and 40-25 Ma so not all 30 can be resolved, and clade names exist only in table A3. Calibration: phylogenetic regression of log10 1C on log10 (guard-cell width³), y = 0.70x − 1.8, r² = 0.67, 36 extant species (Fig. 5a); across 11 genera, y = 1.83x − 5.46, r² = 0.94 (Fig. 2e). |
| **Davesne D, Friedman M, Schmitt AD, Fernandez V, Carnevale G, Ahlberg PE, Sanchez S, Benson RBJ (2021)**. Fossilized cell structures identify an ancient origin for the teleost whole-genome duplication. *PNAS* 118:e2101780118. doi:10.1073/pnas.2101780118 (PMC8325350) | Main text and figures (PMC HTML) | The per-specimen median lacuna volumes and fossil ages are in Datasets S1 and S4 and the SI Appendix, none of which were reachable (see below). The main text prints no per-taxon values. Proxy: median 3D osteocyte lacuna volume from synchrotron PPC-SRµCT of the dentary, log10-transformed, used as a relative genome-size proxy with no conversion to pg. It covers 61 fossil species aged 2.5-252 Ma plus 34 extant species from Davesne et al. 2020. The text reports an inferred ancestral increase in lacuna volume from 148 to 240 µm³ at the base of the teleost stem lineage, and oldest measured stem teleosts of Early Jurassic age (about 195 Ma). |
| **Montanari S, Brusatte SL, De Wolf W, Norell MA (2011)**. Variation of osteocyte lacunae size within the tetrapod skeleton: implications for palaeogenomics. *Biol Lett* 7:751-754. doi:10.1098/rsbl.2011.0173 (PMC3169053) | Full text (PMC HTML) | Critique only; no fossil estimates. |
| **Grunmeier O, D'Emic MD (2019)**. Scaling of statically derived osteocyte lacunae in extant birds: implications for palaeophysiological reconstruction. *Biol Lett* 15:20180837. doi:10.1098/rsbl.2018.0837 (PMC6501357) | Full text (PMC HTML) | Extant birds only; caveat. |
| **Jordan GJ, Carpenter RJ, Koutoulis A, Price A, Brodribb TJ (2015)**. Environmental adaptation in stomatal size independent of the effects of genome size. *New Phytol* 205:608-617. doi:10.1111/nph.13076 | Abstract (Europe PMC) | Extant Proteaceae; caveat for guard-cell proxies. |
| Jones et al. 2022 *PNAS* 119:e2114100119, doi:10.1073/pnas.2114100119 (Middle Jurassic salamanders); Satoh 2026 *J Dev Biol*, doi:10.3390/jdb14010011; Rogoff & Ullmann 2025 *PLoS ONE*, doi:10.1371/journal.pone.0335783; Weiss et al. 2025 *J Anat*, doi:10.1111/joa.14166 | Full texts (Europe PMC) | No new genome-size estimates. Satoh 2026 re-uses Organ et al. 2007. |

No other 2015-2026 study with per-taxon fossil genome-size estimates was found. The searches covered pterosaurs,
synapsids, therapsids, temnospondyls, lissamphibians, lungfishes, marine reptiles and fossil plants, using Europe PMC,
Crossref, the HAL API and web search.

## Not accessed

| Source | Attempted route(s) | Result |
|---|---|---|
| Organ CL, Canoville A, Reisz RR, Laurin M (2011). Paleogenomic data suggest mammal-like genome size in the ancestral amniote and derived large genome size in amphibians. *J Evol Biol* 24:372-380. doi:10.1111/j.1420-9101.2010.02176.x | Wiley (onlinelibrary, pdfdirect); OUP (academic.oup.com/jeb); HAL hal-00629003 | Wiley and OUP serve a Cloudflare JavaScript challenge (HTTP 403 "Just a moment…"). The HAL record has no file, and HAL pages sit behind a bot challenge. The abstract (Europe PMC) says 14 extinct genera with an average of 2.9-3.7 pg; no per-taxon values. Four of its taxa appear in this CSV via the Organ et al. 2016 re-estimates. |
| Organ & Shedlock 2009, ESM (tables 1-3) | PMC `bin/rsbl20080491s07.doc`; Europe PMC; royalsocietypublishing.org; figshare search | PMC file downloads serve a proof-of-work JavaScript challenge. Royal Society returns Cloudflare 403. Not on figshare. |
| Organ et al. 2009, ESM (calibration figure, character analysis) | royalsocietypublishing.org/doi/suppl/… | Cloudflare 403. |
| Organ et al. 2007, main article | nature.com | Paywall (SI was open and used). |
| D'Emic MD, Benson RBJ (2013). Measurement, variation, and scaling of osteocyte lacunae: a case study in birds. *Bone* 57:300-310. doi:10.1016/j.bone.2013.08.010 | ScienceDirect; OpenAlex and Semantic Scholar OA lookups | ScienceDirect 403; closed access. **Abstract only** (Europe PMC/PubMed). The abstract mentions 3D osteocyte volumes for four non-avian dinosaurs but no genome-size estimates; data not reachable. |
| Lomax BH, Hilton J, Bateman RM, Upchurch GR, Lake JA, Leitch IJ, Cromwell A, Knight CA (2014). Reconstructing relative genome size of vascular plants through geological time. *New Phytol* 201:636-644. doi:10.1111/nph.12523 | Wiley (full text, pdfdirect); University of Birmingham repository (research.birmingham.ac.uk/files/18666386/…); Kew repository; CORE | Wiley, the Birmingham repository and CORE all return Cloudflare 403. The pure-oai.bham.ac.uk host does not resolve. Kew lists no public file. **Abstract only**: "many of the earliest land plants had exceptionally large genome sizes"; the "trend of increasing genome size within individual lineages through geological time is not supported"; "maximum genome size steadily increases from the Mississippian (c. 360 Ma) to the present". Whether per-taxon values exist in its tables or SI could not be checked. |
| Franks et al. 2012, ESM tables A1-A3 | royalsocietypublishing.org/doi/suppl/10.1098/rstb.2011.0269; PMC lists no supplement | Cloudflare 403. |
| Davesne et al. 2021, SI Appendix and Datasets S1-S4 | PMC `bin/` files; pnas.org; Dryad doi:10.5061/dryad.bcc2fqzcc | PMC proof-of-work challenge; PNAS Cloudflare 403. The Dryad API lists no public version and the landing page returns 404. |
| Davesne D, Schmitt AD, Fernandez V, Benson RBJ, Sanchez S (2020). *J Evol Biol* 33:808-830. doi:10.1111/jeb.13612 (extant calibration for Davesne 2021) | Wiley; bioRxiv 10.1101/774778 (full text, JATS XML); HAL hal-04228686 | Wiley 403; bioRxiv Cloudflare rate-limit (429, error 1015); HAL bot challenge. Abstract only. Its Dryad dataset (doi:10.5061/dryad.xksn02vc2, extant fishes) is public but was not needed without the fossil data. |
| Thomson KS (1972). An attempt to reconstruct evolutionary changes in the cellular DNA content of lungfish. *J Exp Zool* 180:363-371. doi:10.1002/jez.1401800307 | Wiley | Cloudflare 403. |
| Thomson KS, Muraszko K (1978). Estimation of cell size and DNA content in fossil fishes and amphibians. *J Exp Zool* 205:315-320. doi:10.1002/jez.1402050216 | Wiley | Cloudflare 403. |
| Bomfleur B, McLoughlin S, Vajda V (2014). Fossilized nuclei and chromosomes reveal 180 million years of genomic stasis in royal ferns. *Science* 343:1376-1377. doi:10.1126/science.1249884 (candidate fossil-nucleus source) | science.org | Cloudflare 403. |
| Masterson J (1994). Stomatal size in fossil plants: evidence for polyploidy in majority of angiosperms. *Science* 264:421-424. doi:10.1126/science.264.5157.421 (candidate) | science.org | Cloudflare 403. |

TLS verification was never disabled. No JavaScript, Cloudflare or proof-of-work challenge was bypassed. The WebFetch
tool could not resolve any host in this session, so all retrieval used curl through the session proxy.

## Caveats raised in the literature

1. **Bone identity and section plane.** Montanari et al. (2011) sectioned 11 elements from one individual each of a
   mammal, amphibian, bird and reptile. Mean lacuna size differs significantly between elements in all four. Usually
   this does not change the phylogenetic genome-size estimate significantly, but "the spread of the estimations
   illustrates that this method may not be precise". The sources here mix elements (femur, tibia, skull, vertebra,
   "fragment", scapula, mandible, dentary).
2. **2D ellipsoid volumes are biased** (D'Emic & Benson 2013, abstract):
   - Lacunae in parallel-fibred bone are scalene, not prolate. The prolate model underestimates true volume by about
     2-7 times.
   - Volume varies 5.4-fold among bones of one bird.
   - In birds lacuna volume scales "moderately" with genome size, weakly with body mass and metabolic rate, and not
     with erythrocyte size.
   - Single-section estimates are relative underestimates in theropods compared with sauropods. This raises "the
     possibility that no major change in osteocyte volumes (and genome size) occurred within Theropoda on the lineage
     leading to birds", which directly challenges Organ et al. 2007.
3. **Osteogenesis type matters** (Grunmeier & D'Emic 2019). Lacunae from static and dynamic osteogenesis carry
   different signals. Genome size remained the best single predictor (R² = 0.38, n = 19), but growth- and
   metabolic-rate signals appear only in dynamically formed bone.
4. **Growth rate and tissue type** (Davesne et al. 2020, abstract). In ray-finned fishes, lacunae can be up to 6 times
   larger in woven than in organized bone, and vary 3.5-fold among the bones of one individual. Genome size and
   ploidy still give the best between-species explanation.
5. **Phylogenetic shrinkage.** The Organ-group estimates are phylogenetically informed posterior predictions (λ about
   0.67-0.83). They are pulled toward the genome sizes of extant relatives on the tree, so they are not independent of
   extant data or of the tree's ages. Organ et al. 2016 note that phylogeny matters less for their older taxa, which
   sit nearer the root. The ln-ln slope of about 0.35 also compresses variation: a doubling of lacuna volume maps to
   about a 1.28-fold change in predicted genome size.
6. **Guard-cell proxies confound genome size with environment.**
   - Franks et al. (2012) show that fossil guard-cell size covaries with atmospheric CO₂ over 400 Myr, and interpret
     it as selection on stomatal size.
   - Jordan et al. (2015) find that stomatal size adapts to habitat independently of genome size in Proteaceae.
   - Lomax et al. (2014, abstract) find no within-lineage increase through time, only a rising maximum.
7. **Thomson (1972)** is cited by Organ et al. (2016) as documenting a long-term gradual increase in genome size
   within lungfish. The values could not be checked (not accessed).

## Counts

By `lineage_group` (294 rows):

| lineage_group | Fossil, pg reported | Fossil, pg digitized | Fossil, relative proxy only | Extant calibrators | Total | Fossil age_ma range (Ma) |
|---|---|---|---|---|---|---|
| archosaurs / dinosaurs+birds | 40 | 0 | 0 | 7 | 47 | 3.0-221.4 |
| non-avian sauropsids | 0 | 1 | 0 | 4 | 5 | 275.4 (Permian, unidentified) |
| synapsids / mammals | 0 | 1 | 0 | 14 | 15 | 282.3 (*Mycterosaurus*) |
| amphibians / early tetrapods | 1 | 9 | 0 | 2 | 12 | 167.0-365.5 |
| ray-finned fishes | 0 | 0 | 0 | 3 | 3 | none |
| lobe-finned fishes | 0 | 1 | 0 | 1 | 2 | 377.2 (*Eusthenopteron*) |
| vascular plants | 0 | 0 | 210 | 0 | 210 | 1.66-175 |
| **Total** | **41** | **12** | **210** | **31** | **294** | |

By source:

| Source | Fossil rows | Extant calibrators | value_type |
|---|---|---|---|
| Organ et al. 2007 | 30 | 26 | reported |
| Organ et al. 2009 | 10 | 0 | reported |
| Organ et al. 2016 | 12 | 4 | fossil digitized; calibrators reported |
| Laurin et al. 2016 | 1 | 1 | reported |
| Simonin & Roddy 2018 | 210 (relative proxy) | 0 | reported (proxy) |

Overall, 53 fossil rows carry a pg value, spanning 3.0-377.2 Ma; 41 are reported and 12 digitized. There are no
pg-valued fossil plants and no fossil ray-finned fishes.
