
document.getElementById("logBtn").addEventListener("click", async () => {
  const rawData = JSON.parse(document.getElementById("info").dataset.raw);
  const response = await fetch("http://localhost:5000/log", {
    method: "POST",
    headers: {"Content-Type": "application/json"},
    body: JSON.stringify(rawData)
  });

  const result = await response.json();
  alert(result.message);
});

document.getElementById("copyBtn").addEventListener("click", () => {
  const rawData = document.getElementById("info").dataset.raw;
  navigator.clipboard.writeText(rawData).then(() => {
    alert("📋 JSON copied to clipboard!");
  }).catch(err => {
    console.error("Failed to copy JSON:", err);
    alert("❌ Failed to copy to clipboard.");
  });
});

chrome.tabs.query({active: true, currentWindow: true}, (tabs) => {
  chrome.scripting.executeScript({
    target: {tabId: tabs[0].id},
    function: scrapeData
  }, (results) => {
    const result = results[0]?.result || { error: "Could not extract listing info" };
    renderFormatted(result);
  });
});

function renderFormatted(data) {
  const container = document.getElementById("info");
  container.dataset.raw = JSON.stringify(data);

  if (data.error) {
    container.innerText = "❌ " + data.error;
    return;
  }

  const fields = [
    ["Platform", data.Platform],
    ["Listing Title", data["Listing Title"]],
    ["Address", data.Address],
    ["Netto Miete (CHF)", data["Netto Miete (CHF)"]],
    ["Nebenkosten (CHF)", data["Nebenkosten (CHF)"]],
    ["Brutto Miete (CHF)", data["Brutto Miete (CHF)"]],
    ["Etage", data.Etage],
    ["Wohnfläche (m²)", data["Wohnfläche (m²)"]],
    ["Bezugstermin", data.Bezugstermin],
    ["Google Maps Link", data["Google Maps Link"]],
    ["Listing Link", data["Listing Link"]]
  ];

  container.innerHTML = fields
    .filter(([label, value]) => value !== undefined && value !== null)
    .map(([label, value]) => `<div class='field-label'>${label}:</div><div class='field-value'>${value}</div>`)
    .join("");
}

function scrapeData() {
  const title = document.querySelector("h1")?.innerText ?? null;
  const h2 = document.querySelector("h1 + h2")?.innerText ?? "";
  let address = null;
  let brutto = null;

  if (h2.includes(" - ")) {
    [address, brutto] = h2.split(" - ").map(s => s.trim());
  }

  let mapLink = null;
  document.querySelectorAll("a[href*='maps.google.com']").forEach(a => {
    if (!mapLink && a.href.includes("google.com/maps")) {
      mapLink = a.href;
    }
  });

  const getField = (label) => {
    const rows = document.querySelectorAll("table tr");
    for (const row of rows) {
      const tds = row.querySelectorAll("td");
      if (tds.length === 2 && tds[0].innerText.toLowerCase().includes(label)) {
        return tds[1].innerText.trim();
      }
    }
    return null;
  };

  return {
    Platform: "Flatfox",
    "Listing Title": title,
    Address: address,
    "Brutto Miete (CHF)": brutto,
    "Netto Miete (CHF)": getField("nettomiete"),
    "Nebenkosten (CHF)": getField("nebenkosten"),
    "Etage": getField("etage"),
    "Wohnfläche (m²)": getField("wohnfläche"),
    "Bezugstermin": getField("bezugstermin"),
    "Google Maps Link": mapLink,
    "Listing Link": window.location.href
  };
}
