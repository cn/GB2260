all: parse
.PHONY: all

parse:
	python scripts/main.py sources.tsv .
.PHONY: parse
