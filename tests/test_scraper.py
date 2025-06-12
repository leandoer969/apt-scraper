# tests/test_scraper.py
# ---------------------
# Tests for the scraper logic in src/scraper.py

import pytest
from pathlib import Path
from bs4 import BeautifulSoup

from src.scraper import (
    scrape_flatfox,
    clean_chf_amount,
    detect_platform_and_scrape,
)


@pytest.fixture
def flatfox_soup():
    """
    Load our saved HTML fixture into a BeautifulSoup object
    so tests don’t hit the network.
    """
    fixture_path = Path(__file__).parent / "fixtures" / "flatfox_listing.html"
    html = fixture_path.read_text(encoding="utf-8")
    return BeautifulSoup(html, "html.parser")


@pytest.fixture
def sample_url():
    """A dummy URL matching the Flatfox domain logic."""
    return "https://flatfox.ch/de/wohnung/pfeffingerstrasse-78-4053-basel/1822657/"


@pytest.fixture
def flatfox_data(flatfox_soup, sample_url):
    """
    Run scrape_flatfox once per test session and cache the result.
    This DRYs up tests that just inspect the output dict.
    """
    return scrape_flatfox(flatfox_soup, sample_url)


def test_flatfox_all_fields(flatfox_data):
    """
    Ensure required fields are populated:
     - String fields should be non-empty
     - Numeric rent fields should be int or None
    """
    # Fields expected to always be non-empty strings
    text_fields = [
        "Listing Title",
        "Address",
        "Etage",
        "Wohnfläche (m²)",
        "Bezugstermin",
        # "Google Maps Link",
    ]
    for field in text_fields:
        assert flatfox_data[field], f"{field!r} should not be empty"

    # Fields that might be missing (None) or an integer
    numeric_fields = [
        "Netto Miete (CHF)",
        "Nebenkosten (CHF)",
        "Brutto Miete (CHF)",
    ]
    for field in numeric_fields:
        val = flatfox_data[field]
        assert val is None or isinstance(val, int), f"{field!r} should be int or None"


@pytest.mark.parametrize(
    "raw,expected",
    [
        ("CHF 1’200", 1200),
        ("1_500 CHF", 1500),
        ("", None),
        (None, None),
        ("foobar", None),
    ],
)
def test_clean_chf_amount(raw, expected):
    """
    Test the helper that strips non-digits and converts to int.
    Parametrize lets us run the same logic with different inputs.
    """
    assert clean_chf_amount(raw) == expected


def test_detect_unknown_platform():
    """
    If the URL doesn’t match any known site, we should:
     - get Platform="Unknown"
     - preserve the listing link
     - leave title as None
    """
    html = "<html><body><h1>Test</h1></body></html>"
    url = "https://example.com/foo"
    result = detect_platform_and_scrape(html, url)

    assert result["Platform"] == "Unknown"
    assert result["Listing Link"] == url
    assert result["Listing Title"] is None
