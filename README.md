# apt-scraper

> A Python-based apartment listing scraper for Swiss platforms with logging, testing, linting, and CI.

---

## Project Setup

This project was originally scaffolded using the Project Setup Tool v1.1.2:

```bash
setup_project.sh -n apt-scraper -g
```


## Project Structure

```text
.
├── .github
│   └── workflows
│       └── ci.yml             # GitHub Actions CI pipeline
├── .gitignore                 # Ignored files/dirs
├── .pre-commit-config.yaml    # Pre-commit hooks configuration
├── Makefile                   # Common commands: setup, lint, test, ci, etc.
├── Dockerfile                 # Container build
├── README.md                  # This file
├── apartment_data_model.txt   # Data model reference
├── aptlogger/                 # Browser extension assets
├── bin/
│   └── dev.sh                 # Helper scripts
├── data/                      # JSON output: apartment_log.json
├── logs/                      # Runtime logs
├── notebooks/                 # Jupyter notebooks
├── requirements.in            # Direct dependencies for pip-tools
├── requirements-dev.in        # Dev dependencies for pip-tools
├── requirements.txt           # Pinned dependencies
├── requirements-dev.txt       # Pinned dev dependencies
├── pyproject.toml             # Project metadata and tool configs
├── src/                       # Main Python package
│   ├── __init__.py
│   ├── cli.py
│   ├── scraper.py
│   └── soup.py
├── tests/                     # pytest suite + fixtures
│   ├── fixtures/
│   ├── conftest.py
│   ├── test_logger.py
│   └── test_scraper.py
└── .helper/                   # Local-only files (patches, notes)
```

---

## Quick Start

### Clone the repo

```bash
git clone https://github.com/<YOUR-ORG>/apt-scraper.git
cd apt-scraper
```

### Create virtual environment & install

Using **Makefile**:

```bash
make setup       # create venv and install base tools
make sync        # sync venv to pinned requirements
make precommit   # install git hooks
```

Or manually:

```bash
python3 -m venv .venv
source .venv/bin/activate           # Windows: .venv\Scripts\activate.bat
pip install --upgrade pip
pip install -e '.[dev]'
pre-commit install
make sync
```

### Running the CLI

```bash
apt-scraper https://flatfox.ch/... https://homegate.ch/...
```

Results are logged to `data/apartment_log.json`.

---

## Development Tasks

- **Formatting**: `make format` (Black, isort)
- **Linting**: `make lint` (Flake8, configured via .flake8)
- **Type checking**: `make typecheck` (Mypy, configured via pyproject.toml)
- **Tests**: `make test` (pytest)
- **Coverage**: `make coverage`
- **Run all checks**: `make ci`

---

## Configuration

- **Black** and **isort**: via `[tool.black]` and `[tool.isort]` in `pyproject.toml`
- **Flake8**: via `.flake8` at project root
- **Mypy**: via `[tool.mypy]` in `pyproject.toml`
- **Pre-commit hooks**: via `.pre-commit-config.yaml`
- **CI workflow**: `.github/workflows/ci.yml`

---

For contributions, please fork, make changes, ensure `make ci` passes, and submit a pull request. Happy scraping!
