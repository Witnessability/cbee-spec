PYTHON ?= python3

.PHONY: all review check test build
all: check test build

review:
	$(PYTHON) tools/draft.py review

check:
	$(PYTHON) tools/draft.py check

test:
	$(PYTHON) -m unittest discover -s tests -v

build:
	$(PYTHON) tools/draft.py build

