.PHONY: all reproduce reproduce-all fetch realdata prokaryotes statistics calibration report test legacy clean

# Full pipeline: data/*.csv -> results/*.json -> figures/*.png -> results/RESULTS.md
all: reproduce

reproduce: test statistics calibration report

# Adds the real-data analyses (WP3). Downloads ~500 MB of external data first.
reproduce-all: test fetch statistics calibration realdata prokaryotes report

fetch:
	python3 scripts/fetch_data.py
	cd data/external/ncbi && tar -xzf new_taxdump.tar.gz names.dmp taxidlineage.dmp

realdata:
	python3 scripts/run_realdata.py

prokaryotes:
	python3 scripts/run_prokaryotes.py

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
