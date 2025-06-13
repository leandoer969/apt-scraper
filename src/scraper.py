import re
from datetime import date, datetime
from typing import Any, Dict, Optional

from bs4 import BeautifulSoup


def clean_chf_amount(value: Optional[str]) -> Optional[int]:
    """
    Convert a Swiss-franc string (e.g., "CHF 1’200") into an integer.

    Args:
        value: Raw string potentially containing digits and separators.

    Returns:
        An integer amount if parsing succeeds, otherwise None.
    """
    if not value:
        return None
    digits = re.sub(r"[^\d]", "", value)
    return int(digits) if digits.isdigit() else None


def scrape_homegate(soup: BeautifulSoup, url: str) -> Dict[str, Any]:
    """
    Scrape listing data from a Homegate page.

    Args:
        soup: Parsed BeautifulSoup document.
        url: Original listing URL.

    Returns:
        A dict with keys: Platform, Listing Title, Address,
        Netto Miete (CHF), Nebenkosten (CHF), Brutto Miete (CHF), Listing Link.
    """
    data: Dict[str, Any] = {
        "Platform": "Homegate",
        "Listing Title": None,
        "Address": None,
        "Netto Miete (CHF)": None,
        "Nebenkosten (CHF)": None,
        "Brutto Miete (CHF)": None,
        "Listing Link": url,
    }
    title_tag = soup.find("h1")
    if title_tag:
        data["Listing Title"] = title_tag.get_text(strip=True)
    address_tag = soup.find("p", class_="Address")
    if address_tag:
        data["Address"] = address_tag.get_text(strip=True)

    for dt in soup.find_all("dt"):
        label = dt.get_text(strip=True)
        dd = dt.find_next_sibling("dd")
        value = dd.get_text(strip=True) if dd else ""
        if "Nettomiete" in label:
            data["Netto Miete (CHF)"] = value
        elif "Nebenkosten" in label:
            data["Nebenkosten (CHF)"] = value
        elif "Bruttomiete" in label:
            data["Brutto Miete (CHF)"] = value
    return data


def scrape_immoscout24(soup: BeautifulSoup, url: str) -> Dict[str, Any]:
    """
    Scrape listing data from an Immoscout24 page.
    """
    data: Dict[str, Any] = {
        "Platform": "Immoscout24",
        "Listing Title": None,
        "Address": None,
        "Netto Miete (CHF)": None,
        "Nebenkosten (CHF)": None,
        "Brutto Miete (CHF)": None,
        "Listing Link": url,
    }
    title_tag = soup.find("h1")
    if title_tag:
        data["Listing Title"] = title_tag.get_text(strip=True)
    address_tag = soup.find("span", class_="AddressDisplay")
    if address_tag:
        data["Address"] = address_tag.get_text(strip=True)

    for row in soup.find_all("li", class_="BoxRow"):
        label = row.find("span", class_="BoxLabel")
        value = row.find("span", class_="BoxValue")
        if not label or not value:
            continue
        label_text = label.get_text(strip=True)
        value_text = value.get_text(strip=True)
        if "Nettomiete" in label_text:
            data["Netto Miete (CHF)"] = value_text
        elif "Nebenkosten" in label_text:
            data["Nebenkosten (CHF)"] = value_text
        elif "Bruttomiete" in label_text:
            data["Brutto Miete (CHF)"] = value_text
    return data


# pylint: disable=too-many-locals,too-many-branches
def scrape_flatfox(soup: BeautifulSoup, url: str) -> Dict[str, Any]:
    """
    Scrape listing data from a Flatfox page.
    """
    data: Dict[str, Any] = {
        "Platform": "Flatfox",
        "Listing Title": None,
        "Address": None,
        "Netto Miete (CHF)": None,
        "Nebenkosten (CHF)": None,
        "Brutto Miete (CHF)": None,
        "Etage": None,
        "Wohnfläche (m²)": None,
        "Bezugstermin": None,
        "Google Maps Link": None,
        "Listing Link": url,
    }

    # Title
    h1 = soup.find("h1")
    if h1:
        data["Listing Title"] = h1.get_text(strip=True)

    # Address and Bruttomiete summary
    h2 = h1.find_next("h2") if h1 else None
    if h2:
        text = h2.get_text(strip=True)
        if " - " in text:
            address, rent_info = text.split(" - ", 1)
            data["Address"] = address.strip()
            match = re.search(r"CHF\s?([\d’'_.\s]+)", rent_info)
            if match:
                data["Brutto Miete (CHF)"] = clean_chf_amount(match.group(0))

    # Tables for Miete and Details
    for h2_tag in soup.find_all("h2"):
        heading = h2_tag.get_text(strip=True).lower()
        table = h2_tag.find_next("table")
        if not table:
            continue
        for row in table.find_all("tr"):
            cols = row.find_all("td")
            if len(cols) != 2:
                continue
            label = cols[0].get_text(strip=True).lower()
            value = cols[1].get_text(strip=True)
            if heading == "miete":
                if "bruttomiete" in label:
                    data["Brutto Miete (CHF)"] = clean_chf_amount(value)
                elif "nettomiete" in label:
                    data["Netto Miete (CHF)"] = clean_chf_amount(value)
                elif "nebenkosten" in label:
                    data["Nebenkosten (CHF)"] = clean_chf_amount(value)
            elif heading == "details":
                if "etage" in label:
                    data["Etage"] = value
                elif "wohnfläche" in label:
                    data["Wohnfläche (m²)"] = value
                elif "bezugstermin" in label:
                    try:
                        parsed_date: date = datetime.strptime(
                            value.strip(), "%d.%m.%Y"
                        ).date()
                        data["Bezugstermin"] = parsed_date.isoformat()
                    except ValueError:
                        data["Bezugstermin"] = value

    # Google Maps link
    for iframe in soup.find_all("iframe"):
        a_tag = iframe.find("a", href=True, attrs={"aria-label": True})
        if a_tag and "maps.google.com" in a_tag["href"]:
            data["Google Maps Link"] = a_tag["href"]
            break

    return data


def detect_platform_and_scrape(html: str, url: str) -> Dict[str, Any]:
    """
    Route HTML content to the correct platform-specific scraper.

    Args:
        html: Raw HTML string of the listing page.
        url: URL used to infer the platform.

    Returns:
        A dict of scraped data or a default "Unknown" platform dict.
    """
    soup = BeautifulSoup(html, "html.parser")
    if "homegate.ch" in url:
        return scrape_homegate(soup, url)
    if "immoscout24.ch" in url:
        return scrape_immoscout24(soup, url)
    if "flatfox.ch" in url:
        return scrape_flatfox(soup, url)
    # default for unknown platforms
    return {
        "Platform": "Unknown",
        "Listing Title": None,
        "Address": None,
        "Netto Miete (CHF)": None,
        "Nebenkosten (CHF)": None,
        "Brutto Miete (CHF)": None,
        "Listing Link": url,
    }
