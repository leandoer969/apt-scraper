# tests/conftest.py
# -----------------
# This file is automatically loaded by pytest before any tests run.
# We use it to configure test-wide fixtures, hooks, and imports.

import sys
import os
import pytest

# 1️⃣ Ensure our project root is on Python’s import path so we can do `import src.*`
#    without having to install the package or set PYTHONPATH manually.
PROJECT_ROOT = os.path.abspath(os.path.join(os.path.dirname(__file__), ".."))
sys.path.insert(0, PROJECT_ROOT)


@pytest.fixture(autouse=True)
def temp_log_path(tmp_path, monkeypatch):
    """
    Autouse fixture (runs before every test) that:
     - Creates a temporary file path
     - Monkey-patches src.cli.LOG_PATH to point at that temp file
    This means our tests never write to the real data/apartment_log.json.
    """
    # tmp_path is a pathlib.Path pointing at a fresh temp directory
    fake = tmp_path / "fake_log.json"
    # Import the module under test
    import src.cli as cli_mod

    # Replace the LOG_PATH constant with our fake path
    monkeypatch.setattr(cli_mod, "LOG_PATH", fake)
    return fake
