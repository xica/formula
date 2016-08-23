# Makefile for formula
#
# This contains a set of rules for helping developers.

PYTHON=/usr/bin/env python

all:

test:
	$(PYTHON) -m unittest discover -v test

.PHONY: test
