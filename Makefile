all: parse
.PHONY: all

parse:
	python scripts/parse.py sources.tsv .
.PHONY: parse
