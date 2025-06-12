import argparse
import requests
import json
from src.scraper import detect_platform_and_scrape

def main():
    parser = argparse.ArgumentParser(description="Scrape apartment listings")
    parser.add_argument("urls", metavar="URL", nargs="+", help="Listing URLs")
    parser.add_argument("-v", "--verbose", action="store_true", help="Enable verbose debug output")
    args = parser.parse_args()

    for url in args.urls:
        if args.verbose:
            print(f"📡 Fetching: {url}")

        try:
            headers = {"User-Agent": "Mozilla/5.0"}
            response = requests.get(url, headers=headers)
            response.raise_for_status()

            if args.verbose:
                print("✅ Page fetched, parsing...")
                print(f"🔍 First 500 chars of response:\n{response.text[:500]}\n...")

            data = detect_platform_and_scrape(response.text, url)

            if args.verbose:
                print("✅ Parsed result:")
            print(json.dumps(data, indent=2, ensure_ascii=False))

        except Exception as e:
            print(f"❌ Error while processing {url}: {e}")