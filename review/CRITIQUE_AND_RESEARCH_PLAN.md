# DNA Before Earth: Critical Review and Research Plan

*Review of the `dna-before-earth` repository (state at commit `ec2b7cd`), October 2026.*
*All pilot numbers below come from `review/pilot/` and can be rerun in about a minute.*

---

## 0. Bottom line

1. **The current repo would not survive peer review.** Several headline numbers are hard-coded rather than computed, and some contradict what the repo's own scripts output. The extended dataset has factual errors. The framing ("The Argument They Can't Answer", "paradigm protection") would get the paper desk-rejected before anyone reads the analysis.
2. **The statistics are not the real weakness. The model is.** Conditional on a straight line, the pre-Earth result is statistically solid (pilot: 99% inverse-prediction interval 6.5 to 23.9 Gya for Sharov's points). But the date comes almost entirely from one untested assumption: that complexity grew at the *same rate* in the unobserved interval before the first data point. The data cannot test that assumption. When they can test it, it fails. Fit only the Phanerozoic points and the "origin" is 3.8 Gya. Fit only the Precambrian points and it is 18.3 Gya.
3. **The method gives "pre-Earth" even when the truth is Earth.** In a pilot null model with *no* trend in genome size and life starting on Earth 4.0 Gya, Markov et al.'s construction ("minimal genome per nested clade vs clade age") gives a positive slope in 100% of runs, median R² of 0.93 to 0.96, and a pre-Earth "origin" in essentially every run. The log-linear pattern is what you expect from extreme values on a branching tree, so it cannot be evidence of a complexity clock.
4. **There is still a strong paper here, just not the one the README announces.** The strongest version is a *calibrated, pre-registered test* of the genome-complexity clock using modern data. That means 10^4 to 10^5 genome sizes, TimeTree ages, ancestral reconstructions, gene-family histories and fossil cell-size proxies. It gives the pre-Earth hypothesis a fair chance to pass, and it is publishable whichever way the result comes out. Sections 5 to 8 lay it out.

---

## 1. The hypothesis as the repo states it

- **Claim:** log10(functional or minimal genome size) along the "leading" lineage rises linearly with time, at about 7.5x per billion years (a doubling every ~340 Myr). Extrapolating back to 1 bp gives about 9.8 Gya (Sharov 2006), 10.9 Gya (Markov et al. 2010, 9 points) or 11.2 Gya (the repo's 14 points). All of these are before Earth formed (4.54 Gya).
- **Supporting moves in the repo:** Monte Carlo and bootstrap ("100% pre-Earth"), alternative curves (logistic, quadratic, hyperexponential), a "3x faster early rate" scenario, a threshold table, a random-assembly probability argument, and a "data provenance" argument that critics who accept GenBank data must accept the conclusion.

---

## 2. Reproducibility audit (what a referee will find first)

I re-ran both scripts unchanged (numpy 2.5, scipy 1.18). Items marked **Blocker** must be fixed before anything is shared as science.

| # | Severity | Finding | Evidence |
|---|---|---|---|
| 1 | **Blocker** | README says Markov 9-point R² = **0.914**. The repo's own script computes **0.836**. The 0.914 is typed into the final printed summary table. | `extended_analysis.py` Analysis 1 output vs. the "CONSOLIDATED FINDINGS" block |
| 2 | **Blocker** | The hyperexponential row (R² = 0.979, origin ">10 Bya") is hard-coded. With the parameters the script itself uses, it computes **R² = -54** and prints "never reaches 1 bp". The parameters are mis-transcribed, or the functional form is wrong. | Analysis 5 output |
| 3 | **Blocker** | "3x faster early rate gives 5.7 Bya" is not computed anywhere in the code (it is 3.5 + 5.70/(3 x 0.877)). README says "Every number in this README is reproduced by these scripts". That statement is false. | grep of `analysis/` |
| 4 | **Blocker** | Logistic "origin 20.5 Bya" is a boundary artifact. The fitted carrying capacity L sits exactly on the arbitrary upper bound (15). Raising the bound changes the answer (L = 17.2, "origin" 21.4). The "1% of L" origin rule is arbitrary. Fixing the lower asymptote at 1 bp builds the conclusion into the model. | pilot `stat_checks.py` section 3 |
| 5 | **Blocker** | Extended dataset errors. (a) *Ashbya gossypii* (9.2 Mb) is used twice, as "Eukaryotes" at 2.0 Gya and "Fungi" at 1.0 Gya. (b) *Cyanidioschyzon merolae* is unicellular but is labelled "multicellular" and dated with *Bangiomorpha*. (c) *Genlisea* is a flowering plant (angiosperm) but is used for "earliest land plants" at 470 Mya. (d) The "63 Mb functional" for *Utricularia* has no source. (e) The "free-living only" claim is wrong: *Pratylenchus coffeae* is a plant-parasitic nematode and *Ashbya gossypii* is a cotton pathogen. | `data/extended_dataset.csv`, `SOURCES.md` |
| 6 | High | The CSV files are never read by the code. All data are re-typed inside the scripts. The scripts' 14-point set differs from `extended_dataset.csv` (code has Flowering plants and no Amniotes; the CSV is the reverse). Two different "Sharov" datasets exist: mammals at 0.0 Gya in one script and 0.125 Gya in the other, with different values. | both scripts |
| 7 | High | The README lists files that do not exist: `paper/genome_clock_paper.docx`, `conversation/`, `visualization/`. | `find` |
| 8 | High | The best-fitting model by the repo's own AIC is the **quadratic** (-12.76 vs -12.00). It has no origin at all: going back in time, genome size reaches a minimum at about 5.9 Gya and then *grows*. That contradicts "every model confirms pre-Earth". Really it shows the extrapolation is arbitrary. With n = 5, AICc for any 3-parameter curve is undefined (n - k - 1 = 0), so none of these model comparisons are meaningful. | `full_analysis.py` Part 5; pilot section 2 |
| 9 | Medium | The bootstrap resamples only 5 points. 9.1% of resamples are silently dropped (fewer than 3 unique points), and both MC and bootstrap discard origins above 50 Gya. "100%" from 5 points is not informative. | Part 8 |
| 10 | Medium | The Monte Carlo only jiggles points around the *assumed* straight line. "100% pre-Earth" means "the straight-line extrapolation is insensitive to the stated measurement errors". It does **not** test whether the straight line is right. | Part 2 |
| 11 | Medium | R² falling from 0.97 to 0.84 to 0.71 as points are added is described as the result "strengthening". It means the scatter around the line grows. The p-value falls only because n grows. | README table |
| 12 | Medium | `sharov_2006.csv` calls *Mycoplasma genitalium* "smallest known free-living", but it is an obligate parasite. | CSV note |
| 13 | Medium | Divergence dates are outdated (e.g. Metazoa at 1.25 Gya; see Section 4 for current ages). | |
| 14 | Framing | "Nobody ever actually tested whether he was wrong" is false. Marzban et al. (2014) is a published statistical re-test, and Markov et al. (2010) is itself an extension. See Section 4. | |

**What is already good and worth keeping:** open code and data, an explicit limitations list, flagging the Sharov/Markov metric difference, flagging the coefficient mismatch with Sharov, the threshold table (which honestly shows the date depends on the assumed starting size), and the instinct to turn critics' verbal objections into quantitative tests.

---

## 3. Scientific critique, ranked by how much each point matters

### 3.1 Decisive: the rate before the first data point is unconstrained

Every origin estimate is "first data point + (log10 size of first point) / (assumed early rate)". The data say nothing about the early rate, and where the data *can* test rate constancy, it fails:

| Fit used | Slope (log10 per Gyr) | "Origin" | Note |
|---|---|---|---|
| All 9 Markov points | 0.83 | 10.9 Gya | |
| Phanerozoic only (6 pts) | 2.57 | **3.8 Gya** | Predicts the 4 Gya bacterium at 10^-0.6 bp. That is wrong by 6.7 orders of magnitude. |
| Precambrian only (3 pts) | 0.43 | **18.3 Gya** | Older than the universe |
| Drop the bacterium (leave-one-out) | 1.32 | 7.0 Gya | One point moves the answer by 4 Gyr |

*(pilot `stat_checks.py` sections 4 and 5; Figure, panel A)*

So rates differ about 6-fold between segments of the observed record, and the answer moves between "on Earth" and "before the Big Bang" depending on which segment you trust. Sharov's reply to Koonin ("a slower early rate pushes the origin further back") assumes the slow rate continued all the way back to 1 bp. That is the very assumption in question.

**The same method on other complexity metrics gives impossible answers.** Take LUCA at about 4.2 Gya with about 2,600 proteins (Moody et al. 2024) and humans with about 20,000 protein-coding genes. A constant-rate gene-count clock then puts the origin at **20.4 Gya**. With constrained DNA (LUCA ~2.3 Mb to human ~330 Mb) it is **16.6 Gya**. Both are older than the universe (13.8 Gyr). Any method that can return dates older than the universe proves its own constant-rate assumption false somewhere. Once rates are allowed to vary, nothing in the data anchors the extrapolation. *(pilot section 7)*

**What rate would a terrestrial origin require?** Going from 1 bp to Sharov's 0.5 Mb prokaryote by 3.5 Gya, starting at 4.4 Gya, needs about 7x Sharov's average rate (a doubling every ~50 Myr). Going to Moody's 2.5 Mb LUCA by 4.2 Gya needs about 24x to 37x (a doubling every 9 to 14 Myr). This is the real, interesting, quantitative question the project can own: *how fast did pre-LUCA evolution have to be, and is that implausible?* *(pilot section 6)*

### 3.2 Modern genomes are not ancestral genomes

Every point is a **living** organism's genome placed at the **age of its clade**. *Pelagibacter* (1.3 Mb) is not a 4-billion-year-old genome. It is a highly streamlined product of 4 Gyr of evolution. Genome reduction is common (Wolf & Koonin 2013), and so is genome expansion. The y-value of a modern representative is neither an upper nor a lower bound on the ancestor's genome. A defensible time series needs **ancestral reconstruction** (phylogenetic comparative methods, gene-content reconstruction) or **fossil proxies** (cell size to genome size). The current work has neither.

### 3.3 The nested-minimum and leading-edge construction manufactures a log-linear trend

Markov's points are minima over **nested** clades (Primates within Mammals within Amniotes, and so on down to all life). An older clade contains every younger one, so its minimum can only be lower: monotonicity is guaranteed by construction. It goes further than that. For an *undirected* random walk on a branching tree, the extreme value over a clade moves **linearly in time** (the classical result for branching Brownian motion; speed of about sigma x sqrt(2 x lambda)). A log-linear "clock" is therefore the *expected* signature of no trend at all.

Pilot (`null_bbm.py`): log10 genome size does a random walk with zero drift on a Yule tree. Life starts at 1 Mb, 4.0 Gya, so the true origin is known and terrestrial. Apply Markov's construction at Markov's clade ages:

| Null variant | Positive slope | Median R² | Median inferred "origin" | Inferred pre-Earth |
|---|---|---|---|---|
| Random focal lineage, no floor | 100% | 0.96 | 7.1 Gya | 100% |
| "Most complex" focal lineage, no floor | 100% | 0.97 | 5.5 Gya | 98% |
| Random focal, reflecting floor at 300 kb | 100% | 0.69 | 28 Gya | 100% |
| "Most complex" focal, floor at 300 kb | 100% | 0.82 | 8.8 Gya | 100% |

The method has essentially a 100% false-positive rate for "pre-Earth". The parameters here are illustrative (sigma = 0.5 log10 per sqrt(Gyr), lambda = 2.6 per Gyr). The full study must estimate them from real data (WP2). The qualitative result is robust because it follows from extreme-value theory, not from tuning. This is the most novel and publishable finding in the review (Figure, panel B).

### 3.4 Genome size is a poor and inconsistently defined complexity metric

- The C-value enigma: genome size varies over 100,000-fold among eukaryotes and tracks cell size, nucleotypic effects and drift, not organismal complexity. Examples are lungfish (~40 Gb) and *Paris japonica* / *Tmesipteris* (~150 Gb). Lynch & Conery's drift-barrier and mutational-hazard framework explains much of the variation with effective population size, not complexity.
- Sharov's "functional non-redundant" fraction is defined differently for every point: 75% of *C. elegans*, a third of fugu (by "gene loci"), and 15% of human (transposon-free). That is not one metric.
- Markov's metric (total genome of the smallest member) is a different quantity again. Mixing the two in a 14-point regression is not defensible.
- Section 3.1 shows the conclusion swings by 10 Gyr depending on the metric, so metric robustness is not a nice-to-have. It is the test.

### 3.5 Early complexity cuts both ways

Mushegian's "early overload" point is real: LUCA was already a complex cell (Moody et al. 2024: ~2.5 Mb, ~2,600 proteins, ~4.2 Gya). But reconstructed prokaryotic genome sizes have stayed roughly flat from LUCA to today (median modern prokaryote ~3 to 4 Mb). That is direct evidence of **stasis** for about 2 Gyr of prokaryote-only history, exactly as Koonin argued. So the constant-rate model is contradicted in the very era closest to the extrapolation. A complex LUCA shortly after Earth became habitable means early evolution was fast. Panspermia is one explanation for that, but the data do not single it out.

### 3.6 The probability "wall" argument should be removed from the scientific paper

(1/4)^N is the probability of one *specific* sequence. No origin-of-life model proposes assembling a 300 kb genome at random. The relevant quantity is *functional information*: the fraction of sequence space with a given function (Szostak 2003; Hazen et al. 2007). It is measured experimentally at around 10^-11 for ATP binding in random 80-mers (Keefe & Szostak 2001). Ligase ribozymes have also been isolated directly from random RNA pools. More importantly, the argument is **independent of the clock** and does not favour a pre-Earth origin: 5 extra billion years, or a whole galaxy, change 10^-180,618 by a negligible amount. Referees will read this section as an intelligent-design probability argument and stop taking the rest seriously.

### 3.7 "DNA before Earth" is not even what the hypothesis says

Sharov's claim is about *heritable information* (life), extrapolated to a "1 nucleotide" genome. DNA almost certainly came after RNA. Even if the clock were right, the title would be wrong.

### 3.8 Framing

The data-provenance argument ("accept GenBank, accept the conclusion") is a non sequitur. Critics accept the *measurements*. They reject the *inference*: constant rate, extant species as ancestors, and extrapolation 3x beyond the data. Kuhn, "paradigm protection", the critics-scorecard table, the "Argument They Can't Answer" heading, the theological material and the "AI shows" headline all signal advocacy. For the paper, cut all of it. The philosophy essay can live separately, clearly labelled as opinion.

---
<!-- SECTION 4+ appended below -->

## 5. Reframed research question and pre-registered hypotheses

**Paper question:** *Does genome complexity behave like a clock, and can it date the origin of life?*

This framing gives Sharov's hypothesis a genuine chance to win. It also makes the paper publishable if it loses, which is what makes it a strong case either way.

| Hypothesis | Statement | Signature in data |
|---|---|---|
| **H1: Complexity clock** (Sharov's "strong exponential hypothesis") | Functional complexity on the leading lineage grows log-linearly at a roughly constant rate | Reconstructed *ancestral* complexity is log-linear in time, with homogeneous rates across eras and lineages |
| **H0a: Passive / extreme-value** | No directional trend; apparent trend comes from clade extremes on a branching tree | Observed series indistinguishable from null simulations on the real tree |
| **H0b: Punctuated** | Growth concentrated in major transitions (LUCA, eukaryogenesis, animal multicellularity, vertebrate WGDs), stasis between | Change-point models beat log-linear; rates differ by more than 5x between eras |

**Pre-specified predictions. H1 is supported only if all of these hold:**

- **P1, ancestral linearity:** Reconstructed ancestral values (not extant minima) along the human lineage are log-linear in time. Use genome size, functional/constrained DNA, protein-coding gene families and protein-domain architectures.
- **P2, backcasting:** A rate estimated from younger nodes predicts held-out older nodes within their 95% intervals.
- **P3, beats the null:** The observed extreme-value series is steeper or more linear than at least 95% of null simulations on the real tree, with sigma and diversification rates estimated empirically.
- **P4, cross-lineage consistency:** Independent lineages (land plants, fungi, arthropods) give overlapping slope and intercept intervals.
- **P5, metric robustness:** No metric gives an origin older than 13.8 Gyr, and the metrics agree within error.
- **P6, prokaryotic era:** Complexity increases between LUCA and LECA at the same rate.

If all pass, the pre-Earth extrapolation becomes a serious quantitative hypothesis. Report it with a model-averaged interval that includes structural uncertainty. If they fail, the paper says that genome complexity cannot date the origin of life and quantifies exactly why. Either result is a contribution. Register the predictions on OSF *before* running WP3 to WP5, or submit as a Registered Report.

---

## 6. Work packages

### WP0. Clean, exact replication (1 to 2 weeks)
- Make `data/*.csv` the single source of truth, read by all code. Generate every number in the README from code. Add a test that fails if README numbers drift from outputs. Pin the environment (`requirements.lock` or `uv`/`conda`). Get a Zenodo DOI.
- Fix the items in Section 2 (Ashbya duplicate, mislabelled taxa, hard-coded R² values, logistic bound).
- Reproduce **exactly**: Sharov 2006 (his printed coefficients and dates; resolve the 8.64 + 0.89x mismatch), Markov et al. 2010 (their fitted function and parameters) and Marzban et al. 2014 (their intervals). The paper's credibility starts with matching each published number to the decimal, or explaining the difference.
- Write to Sharov (and ideally Marzban) for the exact inputs. Inviting the original authors to check your replication is good practice and disarms reviewers.

### WP1. Proper statistics on the published datasets (2 weeks)
- Errors-in-variables regression (York / Deming) with inverse-prediction (Fieller) intervals, and a Bayesian version (PyMC or Stan) with explicit priors.
- **Structural uncertainty model:** a piecewise or change-point model in which the rate during the unobserved pre-first-point interval is its own parameter. Show formally that the posterior on the origin date reproduces the prior on that rate (non-identifiability). The deliverable figure is the origin date against the assumed early-rate multiplier.
- Time-series cross-validation (fit younger, predict older), leave-one-out influence, and model averaging. Use AICc and LOO, with an explicit warning about small n.

### WP2. Simulation-based calibration of the method (3 to 4 weeks): the novel core
- Null and alternative trait models for log10 genome size: Brownian motion, Ornstein-Uhlenbeck, bounded diffusion (a "left wall" at the minimal viable genome), and a true directional trend (H1). Run them on (a) simulated birth-death trees and (b) the real TimeTree topology with real node ages.
- Apply Sharov's and Markov's constructions exactly. Measure the false-positive rate for "pre-Earth", the bias in slope and R², and the power to detect a true clock.
- Analytical companion: the extreme of a branching random walk advances at speed about sigma x sqrt(2 x lambda). The fitted "clock rate" is therefore set by trait variance and diversification rate, not by any growth in complexity. Fit sigma with phylogenetic comparative methods (e.g. `geiger::fitContinuous`, `phytools`) and lambda from diversification estimates, then predict the observed slope.
- Extend `review/pilot/null_bbm.py`; this is already the prototype.

### WP3. Large-scale real-data test (4 to 6 weeks)
- Assemble genome sizes for about 10^4 to 10^5 species: GoaT plus the C-value databases (eukaryotes) and GTDB / NCBI complete genomes (prokaryotes). Reconcile everything to NCBI taxids, and attach TimeTree 5 node ages with their confidence intervals.
- For about 20 focal lineages (human, chicken, zebrafish, *Drosophila*, *C. elegans*, *Arabidopsis*, rice, yeast, *Plasmodium*, *E. coli*, an archaeon, ...), compute nested-clade minimum, median and maximum series. Fit, extrapolate, and compare the distribution of "origins" across lineages with the WP2 null on the same tree.
- Prediction under H1: consistent origins across lineages. Under H0a: widely scattered origins that match the null.

### WP4. Ancestral reconstruction: the time series done properly (6 to 8 weeks)
- **Genome size:** ancestral-state reconstruction along each focal lineage (BM / OU / variable-rate models, e.g. RevBayes or BayesTraits). Constrain and validate against fossil cell-size proxies (dinosaur and pterosaur osteocytes; plant guard cells through 400 Myr; fossil fish and amphibian cell sizes).
- **Gene content:** count the gene families present at each ancestral node (LUCA, LECA, Opisthokonta, Metazoa, Bilateria, Vertebrata, Mammalia, ...). Use eggNOG 6 / OrthoDB hierarchical orthologous groups with gain-loss models (Count, ALE) and phylostratigraphy (GenEra) for the human lineage. Account for homology-detection bias (Moyers & Zhang 2015) with simulations.
- **Functional DNA:** constrained fractions where alignments exist (Siepel et al. 2005 across human, fly, worm and yeast; Zoonomia for mammals).
- Evaluate P1, P2, P4, P5 and P6 on these series. This is the analysis Sharov's idea actually calls for, and as far as the literature search found, it has not been done.

### WP5. The pre-LUCA interval: a fair hearing for "life before Earth" (3 to 4 weeks)
- Quantify the rate that a terrestrial origin requires: from habitability (after the Moon-forming impact) to a LUCA of about 2.5 Mb at about 4.2 Gya. Compare it with the fastest complexity gains observed anywhere in the tree (eukaryogenesis, vertebrate whole-genome duplications), with experimental evolution, and with models of pre-Darwinian, transfer-dominated evolution (Woese; Vetsigian, Woese & Goldenfeld 2006).
- Bayesian model comparison: (i) terrestrial origin with a fast early rate vs (ii) a pre-Earth origin with a constant rate. Give each hypothesis its *prior cost*. For (ii) that includes the availability of old rocky planets (the oldest known systems are about 11 Gyr old) and the probability of interstellar transfer (lithopanspermia within the Sun's birth cluster). This is where the pre-Earth hypothesis is taken seriously on its merits, rather than declared unanswerable.

### WP6. Information argument (1 week)
- Remove the (1/4)^N section from the paper, or rewrite it in terms of functional information and measured frequencies of function in random sequence space. State plainly that it is independent of the clock question.

### WP7. Writing, preprint, submission (4 weeks)
- Preprint on bioRxiv with code and data on Zenodo, then journal submission (Section 8).

**Total:** roughly 5 to 7 months part-time. WP0 to WP2 alone (about 2 months) are already enough for a solid short paper on calibrating the published method.

---

## 7. Paper outline

**Working title:** *Can genome size date the origin of life? A calibrated test of the genome-complexity clock*
(Alternative: *Revisiting "life before Earth": extreme-value artifacts and rate non-identifiability in genome-complexity extrapolations*)

1. **Introduction.** The clock idea (Sharov 2006; Sharov & Gordon 2013/2018; Markov et al. 2010), prior critiques (the open reviews, Marzban et al. 2014), and why the question still matters: LUCA's early complexity is a real puzzle.
2. **Methods.** Data (WP3 sources), exact replication, statistics (WP1), simulation calibration (WP2), ancestral reconstruction (WP4), early-interval modelling (WP5). Pre-registration link.
3. **Results.**
   - R1: exact replication, and the errors found in the published inputs.
   - R2: within-model uncertainty is small, but structural uncertainty is unbounded.
   - R3: the null calibration (false-positive rate, analytical slope).
   - R4: the multi-lineage real-data test.
   - R5: the ancestral time series against P1 to P6.
   - R6: the rate required in the pre-LUCA interval.
4. **Discussion.** What evidence *would* establish a complexity clock. Implications for the tempo of early evolution. Panspermia assessed with explicit priors. Limitations.
5. **Data and code availability.** Repo, Zenodo DOI, one command reproduces every figure.

Keep the philosophy, the AI-augmentation narrative and the critics-scorecard out of this paper. If you want the AI angle, write a separate short piece. *"What an audit of our AI-assisted replication found, and the guardrails we added"* (hard-coded numbers, missing files, tests binding text to output) would be honest, useful and novel.

---

## 8. Where to publish and who to involve

- **Biology Direct.** The original venue, with open peer review that publishes reviewer reports. A follow-up there is natural, and Sharov's reviewers or Marzban may well review it.
- **Royal Society Open Science.** Accepts replications and Registered Reports, and judges soundness rather than novelty.
- **Origins of Life and Evolution of Biospheres** or **Astrobiology.** Best fit for WP5 if that becomes the centre of gravity.
- **Journal of Molecular Evolution**, **Genome Biology and Evolution** or **BMC Ecology and Evolution.** Best fit for the WP3 and WP4 genome-evolution results.
- **Co-authors to recruit:** someone in phylogenetic comparative methods (for WP2 and WP4) and a genome-size or gene-content evolution specialist. A co-author from the field roughly doubles the chance of a fair review.

---

## 9. Immediate next steps (the first two weeks)

1. Retitle and reframe the README. Move the philosophy and critics material to a clearly labelled essay. Fix or remove every number not generated by code.
2. Fix the dataset errors (Section 2 #5) and make the CSVs the single source of truth.
3. Get the exact Sharov, Markov and Marzban numbers (Section 4 lists what is verified).
4. Turn `review/pilot/` into a tested module, and draft the OSF pre-registration from Section 5.
5. Pull the GoaT, TimeTree and eggNOG exports (Section 4.3) and build the taxid-joined master table.

---

## Appendix A. Pilot results reproduced in this review

```
python3 review/pilot/stat_checks.py      # replication, Fieller CIs, AICc, logistic bound, LOO, backcasting, required rates, metric reductio
python3 review/pilot/null_bbm.py         # no-trend branching random-walk null (about 30 s)
python3 review/pilot/figure.py review/pilot review/pilot/clock_critique_figure.png
```

Key outputs (seeded):

- Sharov 5-pt (mammals at 0): origin 9.79 Gya; 95% Fieller CI [7.63, 14.16]; 99% CI [6.51, 23.85].
- Sharov 5-pt (mammals at 0.125): origin 9.65 Gya; 95% CI [7.43, 14.37].
- Markov 9-pt: R² 0.836; origin 10.87 Gya; 95% CI [8.05, 17.32].
- Phanerozoic-only fit: origin 3.77 Gya. Precambrian-only fit: 18.29 Gya. Dropping the bacterium: 7.04 Gya.
- Required pre-LUCA rate for an origin at 4.4 Gya: 7x Sharov's rate (to 0.5 Mb at 3.5 Gya) or 37x (to 2.5 Mb at 4.2 Gya).
- Null model (no trend, true origin 4.0 Gya): 100% positive slopes; median R² 0.96; "pre-Earth" in 98 to 100% of runs.

![Pilot figure](pilot/clock_critique_figure.png)
