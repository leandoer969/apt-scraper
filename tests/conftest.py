# tests/conftest.py
# -----------------
# Test configuration: add project root to PYTHONPATH
# and patch LOG_PATH for isolated tests

import sys
from pathlib import Path
import pytest

# Ensure project root is importable for src.* imports
PROJECT_ROOT = Path(__file__).parent.parent.resolve()
sys.path.insert(0, str(PROJECT_ROOT))


@pytest.fixture(autouse=True)
def temp_log_path(tmp_path: Path, monkeypatch: pytest.MonkeyPatch) -> Path:
    """
    Autouse fixture: redirect src.cli.LOG_PATH to a temp file so tests do not
    write to real data/apartment_log.json.

    Returns:
        A Path to the temporary log file.
    """
    fake = tmp_path / "fake_log.json"
    import src.cli as cli_mod

    monkeypatch.setattr(cli_mod, "LOG_PATH", fake)
    return fake
