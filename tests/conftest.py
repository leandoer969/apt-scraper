# tests/conftest.py
# -----------------
# Test configuration: add project root to PYTHONPATH
# and patch LOG_PATH for isolated tests

# pytest fixtures & path hack
# pylint: disable=import-error

from pathlib import Path

import pytest

import src.cli as cli_mod


@pytest.fixture(autouse=True)
def temp_log_path(tmp_path: Path, monkeypatch: pytest.MonkeyPatch) -> Path:
    """
    Autouse fixture: redirect src.cli.LOG_PATH to a temp file so tests do not
    write to real data/apartment_log.json.

    Returns:
        A Path to the temporary log file.
    """
    fake = tmp_path / "fake_log.json"

    monkeypatch.setattr(cli_mod, "LOG_PATH", fake)
    return fake
