.PHONY: all clean setup

all: setup analysis

setup:
	@mkdir -p results

analysis:
	@echo "Running Sharov (2006) replication and extension..."
	python3 analysis/full_analysis.py
	@echo ""
	@echo "Running extended dataset analysis (Markov 2010 + additional taxa)..."
	python3 analysis/extended_analysis.py
	@echo ""
	@echo "All analyses complete. Results in results/"

clean:
	rm -f results/*.json
