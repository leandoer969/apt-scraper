from bs4 import BeautifulSoup

def scrape_homegate(soup, url):
    data = {"Platform": "Homegate", "Listing Title": None, "Address": None, "Netto Miete (CHF)": None, "Nebenkosten (CHF)": None, "Brutto Miete (CHF)": None, "Listing Link": url}
    title_tag = soup.find("h1")
    if title_tag: data["Listing Title"] = title_tag.get_text(strip=True)
    address_tag = soup.find("p", class_="Address")
    if address_tag: data["Address"] = address_tag.get_text(strip=True)
    for dt in soup.find_all("dt"):
        label = dt.get_text(strip=True)
        dd = dt.find_next_sibling("dd")
        value = dd.get_text(strip=True) if dd else ""
        if "Nettomiete" in label: data["Netto Miete (CHF)"] = value
        elif "Nebenkosten" in label: data["Nebenkosten (CHF)"] = value
        elif "Bruttomiete" in label: data["Brutto Miete (CHF)"] = value
    return data

def scrape_immoscout24(soup, url):
    data = {"Platform": "Immoscout24", "Listing Title": None, "Address": None, "Netto Miete (CHF)": None, "Nebenkosten (CHF)": None, "Brutto Miete (CHF)": None, "Listing Link": url}
    title_tag = soup.find("h1")
    if title_tag: data["Listing Title"] = title_tag.get_text(strip=True)
    address_tag = soup.find("span", class_="AddressDisplay")
    if address_tag: data["Address"] = address_tag.get_text(strip=True)
    rent_info = soup.find_all("li", class_="BoxRow")
    for row in rent_info:
        label = row.find("span", class_="BoxLabel")
        value = row.find("span", class_="BoxValue")
        if not label or not value: continue
        label_text, value_text = label.get_text(strip=True), value.get_text(strip=True)
        if "Nettomiete" in label_text: data["Netto Miete (CHF)"] = value_text
        elif "Nebenkosten" in label_text: data["Nebenkosten (CHF)"] = value_text
        elif "Bruttomiete" in label_text: data["Brutto Miete (CHF)"] = value_text
    return data

def scrape_flatfox(soup, url):
    data = {"Platform": "Flatfox", "Listing Title": None, "Address": None, "Netto Miete (CHF)": None, "Nebenkosten (CHF)": None, "Brutto Miete (CHF)": None, "Listing Link": url}
    title_tag = soup.find("h1")
    if title_tag: data["Listing Title"] = title_tag.get_text(strip=True)
    address_tag = soup.find("div", class_="ListingDetailHeader-address")
    if address_tag: data["Address"] = address_tag.get_text(strip=True)
    price_info = soup.find_all("div", class_="DetailsBox-row")
    for row in price_info:
        label = row.find("div", class_="DetailsBox-label")
        value = row.find("div", class_="DetailsBox-value")
        if not label or not value: continue
        label_text, value_text = label.get_text(strip=True), value.get_text(strip=True)
        if "Nettomiete" in label_text: data["Netto Miete (CHF)"] = value_text
        elif "Nebenkosten" in label_text: data["Nebenkosten (CHF)"] = value_text
        elif "Bruttomiete" in label_text or "Miete inkl." in label_text: data["Brutto Miete (CHF)"] = value_text
    return data

def detect_platform_and_scrape(html, url):
    soup = BeautifulSoup(html, "html.parser")
    if "homegate.ch" in url:
        return scrape_homegate(soup, url)
    elif "immoscout24.ch" in url:
        return scrape_immoscout24(soup, url)
    elif "flatfox.ch" in url:
        return scrape_flatfox(soup, url)
    else:
        return {"Platform": "Unknown", "Listing Title": None, "Address": None, "Netto Miete (CHF)": None, "Nebenkosten (CHF)": None, "Brutto Miete (CHF)": None, "Listing Link": url}
    


