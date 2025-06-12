# tests/test_scraper.py
# ---------------------
# Tests for src.scraper scraping logic

import pytest
from pathlib import Path
from typing import Any, Dict, Optional

from bs4 import BeautifulSoup
from src.scraper import (
    scrape_flatfox,
    clean_chf_amount,
    detect_platform_and_scrape,
)


@pytest.fixture
def flatfox_soup() -> BeautifulSoup:
    """
    Load the Flatfox HTML fixture into BeautifulSoup for parsing.
    """
    fixture = Path(__file__).parent / "fixtures" / "flatfox_listing.html"
    html = fixture.read_text(encoding="utf-8")
    return BeautifulSoup(html, "html.parser")


@pytest.fixture
def sample_url() -> str:
    """
    URL for the Flatfox listing to feed into scrape_flatfox.
    """
    return "https://flatfox.ch/de/wohnung/" "pfeffingerstrasse-78-4053-basel/1822657/"


@pytest.fixture
def flatfox_data(flatfox_soup: BeautifulSoup, sample_url: str) -> Dict[str, Any]:
    """
    Cache the output of scrape_flatfox for reuse in multiple tests.
    """
    return scrape_flatfox(flatfox_soup, sample_url)


def test_flatfox_all_fields(flatfox_data: Dict[str, Any]) -> None:
    """
    Ensure that text fields are non-empty and numeric fields are int or None.
    """
    text_fields = [
        "Listing Title",
        "Address",
        "Etage",
        "Wohnfläche (m²)",
        "Bezugstermin",
        # "Google Maps Link",
    ]
    for fld in text_fields:
        assert flatfox_data[fld], f"{fld!r} should not be empty"

    numeric_fields = [
        "Netto Miete (CHF)",
        "Nebenkosten (CHF)",
        "Brutto Miete (CHF)",
    ]
    for fld in numeric_fields:
        val = flatfox_data[fld]
        assert val is None or isinstance(val, int), f"{fld!r} should be int or None"

    # Google Maps Link is optional; if present, ensure it’s a valid URL string
    gm_link = flatfox_data.get("Google Maps Link")
    if gm_link is not None:
        assert isinstance(gm_link, str) and gm_link.startswith(
            "http"
        ), "Google Maps Link should be a valid URL if present"


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
def test_clean_chf_amount(raw: Optional[str], expected: Optional[int]) -> None:
    """
    clean_chf_amount should strip non-digits and convert to int if possible.
    """
    assert clean_chf_amount(raw) == expected


def test_detect_unknown_platform() -> None:
    """
    detect_platform_and_scrape should return a default dict for unknown URLs.
    """
    html = "<html><body><h1>Test</h1></body></html>"
    url = "https://example.com/foo"
    res = detect_platform_and_scrape(html, url)

    assert res["Platform"] == "Unknown"
    assert res["Listing Link"] == url
    assert res["Listing Title"] is None
