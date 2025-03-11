.PHONY: dev dev_docs tests docs

dev:
	python -m pip install -r requirements.txt
	python -m pip install -e .

dev_docs:
	python -m pip install -r docs/requirements.txt
	python -m pip install -e .

tests:
	python -m pytest tests

docs:
	mkdocs serve
