.PHONY: all reproduce reproduce-all fetch realdata prokaryotes nullmodels wp5 genecontent fossils statistics calibration report test legacy clean

# Full pipeline: data/*.csv -> results/*.json -> figures/*.png -> results/RESULTS.md
all: reproduce

reproduce: test statistics calibration report

# Adds the real-data analyses (WP3). Downloads ~500 MB of external data first.
reproduce-all: test fetch statistics calibration realdata prokaryotes nullmodels wp5 genecontent fossils report

fetch:
	python3 scripts/fetch_data.py
	cd data/external/ncbi && tar -xzf new_taxdump.tar.gz names.dmp taxidlineage.dmp

realdata:
	python3 scripts/run_realdata.py

prokaryotes:
	python3 scripts/run_prokaryotes.py

nullmodels:
	python3 scripts/run_nullmodels.py

wp5:
	python3 scripts/run_wp5.py

# Pre-registered (prereg/WP4_preregistration.md). Needs eggnog/e6.og2seqs_and_species.tsv (10.6 GB).
genecontent:
	python3 scripts/run_genecontent.py
	python3 scripts/analyze_genecontent.py

# Pre-registered. Uses the committed compilation data/fossil_genome_size.csv (no download needed).
fossils:
	python3 scripts/analyze_fossils.py

test:
	python3 -m pytest -q tests

statistics:
	python3 scripts/run_statistics.py

calibration:
	python3 scripts/run_calibration.py

report:
	python3 scripts/make_report.py

# Original 2025 scripts, kept for reference. Some of their printed numbers are hard-coded;
# see review/CRITIQUE_AND_RESEARCH_PLAN.md, Section 2.
legacy:
	@mkdir -p results
	python3 analysis/full_analysis.py
	python3 analysis/extended_analysis.py

clean:
	rm -f results/statistics.json results/calibration.json results/RESULTS.md figures/*.png
