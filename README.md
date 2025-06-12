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
├── .github/               # GitHub Actions workflows
│   └── workflows/
│       └── ci.yml         # CI pipeline (tests, linting, coverage, formatting)
├── .flake8                # Flake8 configuration
├── mypy.ini               # Mypy configuration
├── Dockerfile             # Container build instructions
├── README.md              # This file
├── apartment_data_model.txt # Data model reference
├── aptlogger/             # Browser extension assets
├── bin/                   # Helper scripts
│   └── dev.sh             # Development entrypoint
├── data/                  # JSON log output (`apartment_log.json`)
├── logs/                  # Runtime logs
├── notebooks/             # Jupyter notebooks for analysis
├── requirements.txt       # Python dependencies
├── pytest.ini             # Pytest configuration
├── src/                   # Main Python package
│   ├── __init__.py
│   ├── cli.py             # Command-line interface
│   ├── scraper.py         # Scraping logic
│   └── soup.py            # Shared parsing utilities
├── tests/                 # pytest test suite + fixtures
│   ├── fixtures/          # Sample HTML files
│   ├── conftest.py        # Test configuration & fixtures
│   ├── test_logger.py
│   └── test_scraper.py
└── .helper/               # Local-only files (patches, notes)
```

## Quick Start

### 1. Clone & Create Virtual Environment

```bash
git clone https://github.com/<YOUR-ORG>/apt-scraper.git
cd apt-scraper
python3 -m venv .venv
source .venv/bin/activate      # macOS/Linux
# .venv\\Scripts\\activate.bat # Windows
```

### 2. Install Dependencies

```bash
pip install --upgrade pip
pip install -r requirements.txt
```

### 3. Run the CLI

```bash
# Scrape one or more URLs:
apt-scraper https://flatfox.ch/... https://homegate.ch/...
```

Results are appended to `data/apartment_log.json`.

## Testing & Quality

### Run Tests

```bash
pytest               # run all tests
pytest -q            # quiet output
pytest --maxfail=1   # stop after first failure
```

### Coverage Report

```bash
pip install pytest-cov
pytest --cov=src --cov-report=term-missing
```

## Linting & Formatting

We use Black, Flake8, and Mypy to enforce style and catch issues:

1. **Black** for auto-formatting (line-length 88):
   ```bash
   black .
   ```
2. **Flake8** for linting, configured via `.flake8`:
   ```bash
   flake8 src tests
   ```
   - Create a `.flake8` file at the project root:
     ```ini
     [flake8]
     max-line-length = 88
     extend-ignore = E203, W503
     ```
3. **Mypy** for static type checking, configured via `mypy.ini`:
   ```bash
   mypy src
   ```
   - Create a `mypy.ini` file at the project root:
     ```ini
     [mypy]
     python_version = 3.11
     ignore_missing_imports = True
     ```

This setup ensures Black and Flake8 agree on wrapping, and Mypy ignores missing stubs for third-party libs like `requests`.

## Continuous Integration (GitHub Actions)

All CI steps are defined in `.github/workflows/ci.yml` and run on every push or pull request against `main`:

1. Checkout code
2. Set up Python 3.11 environment
3. Install dependencies (including pytest, Black, Flake8, Mypy)
4. Run **Black** in check mode
5. Run **Flake8**
6. Run **mypy**
7. Run **pytest** with coverage
8. Upload coverage report as artifact

Check results under the **Actions** tab in GitHub.

## Contributing

1. Fork the repo and create a feature branch
2. Write or update tests in `tests/`
3. Ensure all checks pass locally:
   ```bash
   black --check . && flake8 src tests && mypy src && pytest --cov=src
   ```
4. Open a pull request against `main`

---

*Happy scraping!*

