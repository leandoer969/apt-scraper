# tests/test_logger.py
import pytest
import json
from datetime import datetime
from src.cli import log_scrape


@pytest.fixture
def dummy_listing():
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
        "Listing Link": "https://flatfox.ch/de/wohnung/pfeffingerstrasse-78-4053-basel/1822657/",
    }


def test_log_new_listing(dummy_listing, temp_log_path, capsys):
    log = []
    updated = log_scrape(dummy_listing.copy(), log)
    captured = capsys.readouterr()
    # should print success and add a Scrape Time
    assert "✅ Added new apartment" in captured.out
    assert len(updated) == 1
    assert "Scrape Time" in updated[0]
    # file on disk matches returned log
    data = json.loads(temp_log_path.read_text(encoding="utf-8"))
    assert data == updated


def test_duplicate_detection(dummy_listing, temp_log_path, capsys):
    scrape_time = datetime.now().isoformat()
    existing = dict(dummy_listing, **{"Scrape Time": scrape_time})
    log = [existing]
    updated = log_scrape(dummy_listing.copy(), log)
    captured = capsys.readouterr()
    # should warn and not modify the log
    assert "⚠️ Already scraped:" in captured.out
    assert updated == log
