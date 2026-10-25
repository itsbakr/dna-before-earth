# Pre-registration: gene-content and fossil tests of the genome-complexity clock (WP4)

*Written 25 October 2026, before the WP4 data below were examined. The git commit that adds this file
is its timestamp. For a formal registration, upload this text unchanged to OSF Registries
(https://osf.io/registries) or submit it as a PCI Registered Report Stage 1.*

## 1. Question

Sharov (2006) proposed that functional genome complexity on the leading lineage grew exponentially at
a roughly constant rate (about 0.89 log10 units per Gyr), so that extrapolating back dates the origin
of life to about 10 Gya. Our earlier work (`results/RESULTS.md`) shows that statistics built only from
living species cannot detect such a clock. The two data types that carry direct information about the
past are (a) **gene families inferred to be present in ancestors** (homologs shared across a node's
basal split) and (b) **genome sizes estimated from fossils**. This document fixes, in advance, how
those data will be used to test the clock.

## 2. Hypotheses

- **H1 (complexity clock).** Ancestral complexity along a lineage rises log-linearly with time at a
  roughly constant rate, similar across lineages and eras, including the prokaryotic era.
- **H0b (punctuated).** Complexity rises mainly at major transitions (origin of cells, eukaryogenesis,
  animal multicellularity, vertebrate genome duplications) with slower change or stasis between them.
- **H0a (no trend).** No consistent directional change.

## 3. Status of the data at registration

- **eggNOG 6** (`e6.og2seqs_and_species.tsv`) is being downloaded. Before writing this document we
  inspected only the list of taxonomic level IDs (to know which nodes exist), never any orthogroup
  counts or memberships.
- **Fossil genome-size estimates** are being compiled from the original publications by a separate
  process. We have **not** seen the compiled table. We have read published summary statements (for
  example, Organ et al. 2007 report small genomes in early saurischian dinosaurs; Lomax et al. 2014 report
  no steady within-lineage increase in plants), so the fossil test is not blind to those conclusions.

## 4. Gene-content test (WP4a)

### 4.1 Data
eggNOG 6 hierarchical orthologous groups (OGs) at each taxonomic level; NCBI Taxonomy (new_taxdump,
downloaded 25 October 2026) for species membership; node ages from the 2015 Timetree of Life (MRCA of
tree tips belonging to the node's ingroup and outgroup), with literature ages as a sensitivity analysis.

### 4.2 Nodes (ingroup vs outgroup defining the node's basal split)

**Human lineage (primary).**

| Level (eggNOG taxid) | Node | Ingroup | Outgroup |
|---|---|---|---|
| 1 | LUCA | Archaea + Eukaryota | Bacteria |
| 2759 | LECA | Amorphea (Opisthokonta, Amoebozoa, Apusozoa) | Diaphoretickes proxies (Viridiplantae, Sar, Rhodophyta) |
| 33154 | Opisthokonta | Holozoa (Metazoa, Choanoflagellata, Ichthyosporea) | Fungi |
| 33208 | Metazoa | other animals | Porifera + Ctenophora |
| 33213 | Bilateria | Deuterostomia | Protostomia |
| 7711 | Chordata | Craniata + Tunicata | Cephalochordata |
| 7742 | Vertebrata | Gnathostomata | Cyclostomata |
| 8287 | Sarcopterygii | Tetrapoda | Dipnoi + Actinistia |
| 40674 | Mammalia | Theria | Monotremata |
| 314146 | Euarchontoglires | Euarchonta | Glires |
| 9443 | Primates | Haplorrhini | Strepsirrhini |
| 376913 | Haplorrhini | Simiiformes | Tarsiiformes |
| 314293 | Simiiformes | Catarrhini | Platyrrhini |
| 9526 | Catarrhini | Hominoidea | Cercopithecoidea |
| 314295 | Hominoidea | Hominidae | Hylobatidae |
| 9604 | Hominidae | Homininae | Ponginae |

**Arabidopsis lineage (secondary):** LUCA; LECA (as above); Viridiplantae (Streptophyta vs Chlorophyta);
Streptophyta (Streptophytina vs other streptophytes); Streptophytina (Embryophyta vs other
Streptophytina); Magnoliopsida (Mesangiospermae vs other angiosperms); Brassicaceae (lineage child vs
other Brassicaceae).

**Yeast lineage (secondary):** LUCA; LECA; Opisthokonta (Fungi vs Holozoa); Fungi (Dikarya vs other
Fungi); Dikarya (Ascomycota vs Basidiomycota); Ascomycota (Saccharomycotina + Pezizomycotina vs
Taphrinomycotina); Saccharomycetales (lineage child vs others).

Where NCBI Taxonomy lacks a needed taxon, the closest available taxa will be used and the substitution
reported.

### 4.3 Statistics per node
- **S_a (primary): ancestral gene families** = the number of OGs at the node's level containing at least
  one ingroup species and at least one outgroup species.
- **S_b (secondary): focal genes with ancient homologs** = the number of focal-species proteins in such
  spanning OGs (human, *Arabidopsis thaliana* or *Saccharomyces cerevisiae*).

Known biases, both of which make older nodes look **smaller** and therefore favour H1: eggNOG clusters
deeper levels more coarsely (lumping families), and fast-evolving genes lose detectable homology over
time. Horizontal gene transfer (including from the mitochondrial ancestor) can inflate the LUCA count.

### 4.4 Tests and decision rules (y = log10 S, t = node age in Gyr)

- **P1, log-linearity.** OLS of y on t per lineage. Passes if (i) the rate is positive with a 95% CI
  excluding 0, (ii) R² ≥ 0.80, and (iii) a continuous two-segment model with the breakpoint counted as a
  parameter does not improve AICc by more than 2.
- **P2, backcasting.** Fit only nodes younger than 1.0 Gya. Passes if the observed LECA and LUCA values
  both lie inside their 95% prediction intervals.
- **P4, cross-lineage consistency.** Passes if the 95% CIs of the rates for the human, *Arabidopsis* and
  yeast lineages all overlap pairwise.
- **P5, plausibility.** The human-lineage line's extrapolated age at y = 0 (one gene family) must be
  younger than 13.8 Gya.
- **P6, prokaryotic era.** The rate between LUCA and LECA (difference in y over difference in t) must be
  at least 50% of the whole-lineage OLS rate.

**Verdict.** Gene content supports H1 only if P1, P2, P4, P5 and P6 all pass for S_a. S_b and the
literature-age sensitivity analysis are reported alongside, and a disagreement between them will be
stated, not resolved by choice.

## 5. Fossil test (WP4b)

### 5.1 Data
Genome sizes estimated from fossil cell-size proxies (osteocyte lacunae, guard cells), compiled with
source locations into `data/fossil_genome_size.csv`. Extant calibration species are excluded from the
tests. Taxa are grouped into the `lineage_group` values defined in that file.

### 5.2 Tests and decision rules
- **F1, per-lineage trend.** For each lineage group with at least 5 fossil taxa spanning at least 50 Myr,
  regress log10 genome size on age (Gyr). H1 predicts genomes larger toward the present at about
  +0.89 log10 per Gyr. A group is *consistent with H1* if the rate's 95% CI excludes 0 on the positive
  side and includes 0.89.
- **F2, pooled.** Linear model with lineage-group intercepts and a common rate. Same criterion as F1.
- **F3, sign consistency.** H1 predicts the same (positive) sign in every qualifying group.

For sources reporting only relative proxies (for example plant guard-cell size), only the sign of the
trend is tested. The minimum detectable rate given the observed residual variance will be reported, so
that a null result can be judged for power.

**Verdict.** The fossil data support H1 only if F2 passes and F3 holds.

## 6. Exploratory analyses (not covered by this registration)
Ornstein-Uhlenbeck, bounded and heavy-tailed null models for genome size; the pre-LUCA rate analysis
(WP5); any analysis of additional lineages. These will be labelled exploratory.

## 7. Deviations
Any deviation from this plan (for example a node unavailable in eggNOG, or a source that cannot be
parsed) will be listed with its reason in the results.
