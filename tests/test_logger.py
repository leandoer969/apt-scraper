# tests/test_logger.py
# --------------------
# Tests for the log_scrape function in src/cli.py

# pylint: disable=import-error,redefined-outer-name

import json
from datetime import datetime
from pathlib import Path
from typing import Any, Dict, List

import pytest

from src.cli import log_scrape


@pytest.fixture
def dummy_listing() -> Dict[str, Any]:
    """
    Provide a fresh listing dict for testing log_scrape.

    Returns:
        A dictionary representing a flatfox listing.
    """
    return {
        "Platform": "Flatfox",
        "Listing Title": "Test Apartment",
        "Address": "Teststrasse 1, 8000 Zürich",
        "Netto Miete (CHF)": 1000,
        "Nebenkosten (CHF)": 150,
        "Brutto Miete (CHF)": 1150,
        "Etage": "1. Etage",
        "Wohnfläche (m²)": "50 m²",
        "Bezugstermin": "2025-08-01",
        "Google Maps Link": "https://maps.google.com/...",
        "Listing Link": (
            "https://flatfox.ch/de/wohnung/" "pfeffingerstrasse-78-4053-basel/1822657/"
        ),  # noqa: E501
    }


def test_log_new_listing(
    dummy_listing: Dict[str, Any], temp_log_path: Path, capsys: Any
) -> None:
    """
    New listings should be appended to an empty log,
    print a success message, and persist to disk.
    """
    log: List[Dict[str, Any]] = []
    updated = log_scrape(dummy_listing.copy(), log)
    captured = capsys.readouterr()

    assert "✅ Added new apartment" in captured.out
    assert len(updated) == 1
    assert "Scrape Time" in updated[0]

    # Verify file on disk matches returned log
    on_disk = json.loads(temp_log_path.read_text(encoding="utf-8"))
    assert on_disk == updated


def test_duplicate_detection(dummy_listing: Dict[str, Any], capsys: Any) -> None:
    """
    If the listing already exists by URL or address,
    the log remains unchanged and a warning is printed.
    """
    scrape_time = datetime.now().isoformat()
    existing = dict(dummy_listing, **{"Scrape Time": scrape_time})
    log: List[Dict[str, Any]] = [existing]

    updated = log_scrape(dummy_listing.copy(), log)
    captured = capsys.readouterr()

    assert "⚠️ Already scraped:" in captured.out
    assert updated == log
