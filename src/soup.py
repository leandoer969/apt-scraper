import requests
from bs4 import BeautifulSoup

url = "https://flatfox.ch/de/wohnung/sevogelstr-140-4052-basel/1797445/"  # "https://flatfox.ch/de/wohnung/pfeffingerstrasse-78-4053-basel/1822657/"
headers = {"User-Agent": "Mozilla/5.0"}

res = requests.get(url, headers=headers)
res.raise_for_status()

soup = BeautifulSoup(res.text, "html.parser")

with open("data/flatfox_listing_2.html", "w", encoding="utf-8") as f:
    f.write(soup.prettify())

print("✅ Saved HTML to flatfox_listing.html")
