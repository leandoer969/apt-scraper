import argparse
import requests
import json
from datetime import datetime
from pathlib import Path
from src.scraper import detect_platform_and_scrape

LOG_PATH = Path("data/apartment_log.json")


def load_log():
    if LOG_PATH.exists():
        with open(LOG_PATH, "r", encoding="utf-8") as f:
            return json.load(f)
    return []


def save_log(log):
    with open(LOG_PATH, "w", encoding="utf-8") as f:
        json.dump(log, f, ensure_ascii=False, indent=2)


def log_scrape(result, log):
    # Match on link or address
    for entry in log:
        if (
            entry["Listing Link"] == result["Listing Link"]
            or entry["Address"] == result["Address"]
        ):
            print(
                f"⚠️ Already scraped: {entry['Listing Title']} "
                f"({entry['Address']}) on {entry['Scrape Time']} from {entry['Platform']}."
            )
            return log  # no change
    result["Scrape Time"] = datetime.now().isoformat()
    log.append(result)
    save_log(log)
    print(f"✅ Added new apartment: {result['Listing Title']} ({result['Address']})")
    return log


def main():
    parser = argparse.ArgumentParser(description="Scrape apartment listings")
    parser.add_argument("urls", metavar="URL", nargs="+", help="Listing URLs")
    parser.add_argument(
        "-v", "--verbose", action="store_true", help="Enable verbose output"
    )
    args = parser.parse_args()

    log = load_log()

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

        except Exception as e:
            print(f"❌ Failed to process {url}: {e}")


if __name__ == "__main__":
    main()
