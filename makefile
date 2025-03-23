# Makefile for setting up the development environment
#
# This Makefile defines targets for:
# - dev: setting up the development environment
# - dev_docs: setting up the documentation development environment
# - tests: running tests using pytest
# - docs: serving the documentation locally using MkDocs
#
# Usage:
# - To set up the development environment, run: `make dev`
# - To set up the documentation development environment, run: `make dev_docs`
# - To run the tests, run: `make tests`
# - To serve the documentation locally, run: `make docs`

.PHONY: dev dev_docs tests docs

# Target to set up the development environment.
# Installs required dependencies from requirements.txt, and installs the current package in editable mode,
dev:
	python -m pip install -r requirements.txt
	python -m pip install -e .

# Target to set up the documentation development environment.
# Installs the required dependencies for documentation from docs/requirements.txt
# and installs the current package in editable mode (overriding FauxPy in docs/requirements.txt).
dev_docs:
	python -m pip install -r docs/requirements.txt
	python -m pip install -e .

# Target to run the tests.
# Uses pytest to execute all tests located in the tests directory.
tests:
	python -m pytest tests

# Target to serve the documentation locally.
# Starts the MkDocs server for local preview of the documentation.
docs:
	mkdocs serve
