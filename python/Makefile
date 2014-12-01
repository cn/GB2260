PYTHON := python

.PHONY: all build

all: build

build: gb2260/data.py
	$(PYTHON) setup.py sdist bdist_wheel

gb2260/data.py: ../GB2260.txt
	$(PYTHON) generate.py $< $@
