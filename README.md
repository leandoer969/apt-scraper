# apt-scraper

This project was set up using the Project Setup Tool v1.1.2 🚀

**Command used for setup:**
```
setup_project.sh -n apt-scraper -g
```

## Project Structure
- **src/**: Python source code package.
    - Contains `__init__.py` and a README explaining how to interact with the code.
- **data/**: Data files.
- **notebooks/**: Jupyter notebooks for interactive analysis.
- **logs/**: Log files.
- **tests/**: Test cases.
- **bin/**: Consolidated helper script `dev.sh`.
- **.vscode/**: VS Code configuration.
- **.venv/**: The Python virtual environment.
- **.env**: (Optional) Environment variables.

## Using the Project
- **Python Scripts:** Place your modules in `src/` and import them as part of the package.
- **Jupyter Notebooks:** Launch your notebooks from the project root so that `src/` is in your PYTHONPATH, or add it manually:
  ```python
  import sys, os
  sys.path.insert(0, os.path.abspath("src"))
  ```
