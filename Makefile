# Makefile: shortcuts for environment setup and project tasks

# Virtual environment directory
VENV := .venv
PYTHON := $(VENV)/bin/python
PIP := $(VENV)/bin/pip
PIPSYNC := $(VENV)/bin/pip-sync
PIP_COMPILE := $(VENV)/bin/pip-compile
PRECOMMIT := $(VENV)/bin/pre-commit
BLACK := $(VENV)/bin/black
ISORT := $(VENV)/bin/isort
FLAKE8 := $(VENV)/bin/flake8
MYPY := $(VENV)/bin/mypy
PYTEST := $(VENV)/bin/pytest

.PHONY: help setup install precommit format lint typecheck test coverage ci snapshot clean

help:
	@echo "Available targets:"
	@echo "  setup       Create virtualenv and install base tools"
	@echo "  install     Install project dependencies"
	@echo "  precommit   Run pre-commit hooks on all files"
	@echo "  format      Run black and isort"
	@echo "  lint        Run flake8"
	@echo "  typecheck   Run mypy"
	@echo "  test        Run pytest"
	@echo "  coverage    Run tests with coverage report"
	@echo "  ci          Run format, lint, typecheck, precommit, test, coverage"
	@echo "  snapshot    Save Flatfox HTML snapshot via src/soup.py"
	@echo "  clean       Remove virtualenv and caches"
	@echo "  requirements.txt  Compile requirements.in to requirements.txt"
	@echo "  requirements-dev.txt  Compile requirements-dev.in to requirements-dev.txt"
	@echo "  lock         Update both requirements.txt and requirements-dev.txt"

setup: $(VENV)/bin/activate

$(VENV)/bin/activate:
	python3 -m venv $(VENV)
	$(PIP) install --upgrade pip
	$(PIP) install -r requirements.txt pre-commit
	@echo "Virtual environment created and pre-commit installed."
	@echo "To activate, run: source $(VENV)/bin/activate"

install:
	$(PIP) install -e .
	$(PIP) install -r requirements-dev.txt

##------------------------------------------------------------------
# Compile .in into pinned .txt
requirements.txt: requirements.in
	$(PIP_COMPILE) requirements.in

requirements-dev.txt: requirements-dev.in
	$(PIP_COMPILE) requirements-dev.in

lock: requirements.txt requirements-dev.txt
	@echo "👉 Updated lock files: requirements.txt & requirements-dev.txt"

sync:
	$(PIPSYNC) requirements.txt requirements-dev.txt

precommit:
	$(PRECOMMIT) run --all-files

format:
	$(BLACK) .
	$(ISORT) .

lint:
	$(FLAKE8) src tests

typecheck:
	$(MYPY) src

test:
	$(PYTEST)

coverage:
	$(PYTEST) --cov=src --cov-report=term-missing --cov-report=xml

ci: format lint typecheck precommit test coverage

snapshot:
	$(PYTHON) src/soup.py

clean:
	rm -rf $(VENV) __pycache__ .pytest_cache htmlcov coverage.xml
