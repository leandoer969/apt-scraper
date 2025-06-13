import argparse
import json
from datetime import datetime
from pathlib import Path
from typing import Any, Dict, List  # , Union

import requests
from requests.exceptions import RequestException

from src.scraper import detect_platform_and_scrape

LOG_PATH = Path("data/apartment_log.json")


def load_log() -> List[Dict[str, Any]]:
    """
    Load the JSON log of past scrapes from disk.

    Returns:
        A list of scrape-result dictionaries, each containing keys like
        "Listing Link", "Address", "Scrape Time", etc.
    """
    if LOG_PATH.exists():
        with open(LOG_PATH, "r", encoding="utf-8") as f:
            return json.load(f)
    return []


def save_log(log: List[Dict[str, Any]]) -> None:
    """
    Save the given log list to disk as JSON.

    Args:
        log: List of scrape-result dictionaries to persist.
    """
    with open(LOG_PATH, "w", encoding="utf-8") as f:
        json.dump(log, f, ensure_ascii=False, indent=2)


def log_scrape(
    result: Dict[str, Any], log: List[Dict[str, Any]]
) -> List[Dict[str, Any]]:
    """
    Append a new listing result to the log if it's not a duplicate.

    Args:
        result: A dictionary representing the scraped listing data.
        log: Current list of logged listings.

    Returns:
        The updated log list (original list with new entry appended if unique).
    """
    for entry in log:
        if (
            entry["Listing Link"] == result["Listing Link"]
            or entry["Address"] == result["Address"]
        ):
            msg = (
                f"⚠️ Already scraped: {entry['Listing Title']} "
                f"({entry['Address']}) on {entry['Scrape Time']} "
                f"from {entry['Platform']}."
            )
            print(msg)
            return log

    # Add timestamp and save
    result["Scrape Time"] = datetime.now().isoformat()
    log.append(result)
    save_log(log)

    msg = (
        f"✅ Added new apartment: {result['Listing Title']} " + f"({result['Address']})"
    )
    print(msg)
    return log


def main() -> None:
    """
    CLI entry point for scraping apartment listings.

    Parses command-line arguments, fetches each URL provided,
    scrapes data, and logs results.
    """
    parser = argparse.ArgumentParser(description="Scrape apartment listings")
    parser.add_argument("urls", metavar="URL", nargs="+", help="Listing URLs")
    parser.add_argument(
        "-v", "--verbose", action="store_true", help="Enable verbose output"
    )
    args = parser.parse_args()

    log: List[Dict[str, Any]] = load_log()

    for url in args.urls:
        if args.verbose:
            print(f"📡 Fetching: {url}")

        try:
            headers = {"User-Agent": "Mozilla/5.0"}
            response = requests.get(url, headers=headers)
            response.raise_for_status()

            if args.verbose:
                print("✅ Page fetched, parsing...")

            result = detect_platform_and_scrape(response.text, url)

            if args.verbose:
                print(json.dumps(result, indent=2, ensure_ascii=False))

            log = log_scrape(result, log)

        except RequestException as e:
            print(f"❌ Failed to process {url}: {e}")


if __name__ == "__main__":
    main()
