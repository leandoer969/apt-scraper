import requests
from bs4 import BeautifulSoup
from typing import Union
from pathlib import Path


def save_flatfox_snapshot(url: str, output_path: Union[str, Path]) -> None:
    """
    Fetch a Flatfox listing page and save a prettified HTML snapshot.

    Args:
        url: The Flatfox listing URL to fetch.
        output_path: Filesystem path to write the HTML snapshot.
    """
    output_path = Path(output_path)
    output_path.parent.mkdir(parents=True, exist_ok=True)

    headers = {"User-Agent": "Mozilla/5.0"}
    response = requests.get(url, headers=headers)
    response.raise_for_status()

    soup = BeautifulSoup(response.text, "html.parser")

    html_bytes: bytes = soup.prettify(encoding="utf-8")
    # Write bytes to match prettify() output

    with open(output_path, "wb") as f:
        f.write(html_bytes)

    print(f"✅ Saved HTML snapshot to {output_path}")


if __name__ == "__main__":
    url_flatfox = "https://flatfox.ch/de/wohnung/sevogelstr-140-4052-basel/1797445/"
    output_path = Path(__file__).parent.parent / "data" / "flatfox_snapshot.html"
    save_flatfox_snapshot(url_flatfox, str(output_path))
