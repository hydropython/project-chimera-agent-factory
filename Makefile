PYTHON := python
PIP := pip

.PHONY: setup test spec-check build-image

setup:
	$(PIP) install -r requirements.txt

test:
	pytest -q

spec-check:
	python scripts/validate_specs.py

build-image:
	docker build -t chimera:latest .
