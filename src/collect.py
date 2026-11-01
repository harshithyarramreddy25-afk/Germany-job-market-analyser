import time
from datetime import date

import pandas as pd
import requests

URL = "https://rest.arbeitsagentur.de/jobboerse/jobsuche-service/pc/v6/jobs"
HEADERS = {"X-API-Key": "jobboerse-jobsuche"}

SEARCH_TERMS = ["Data Scientist", "Data Analyst", "Data Engineer", "Machine Learning"]
PAGES = 4    # 4 pages x 50 = up to 200 postings per search term
SIZE = 50


def find_offers(node):
    """Find the list of job postings anywhere in the response."""
    if isinstance(node, list):
        if node and isinstance(node[0], dict) and "referenznummer" in node[0]:
            return node
        for item in node:
            found = find_offers(item)
            if found:
                return found
    elif isinstance(node, dict):
        for value in node.values():
            found = find_offers(value)
            if found:
                return found
    return []


rows = []

for term in SEARCH_TERMS:
    for page in range(1, PAGES + 1):
        params = {"was": term, "angebotsart": 1, "page": page, "size": SIZE}
        r = requests.get(URL, headers=HEADERS, params=params, timeout=30)
        if r.status_code != 200:
            print(f"{term} page {page}: HTTP {r.status_code}, stopping this term")
            break

        data = r.json()
        if page == 1 and term == SEARCH_TERMS[0]:
            print("Top-level keys in response:", list(data.keys()))

        offers = find_offers(data)
        if not offers:
            break

        for o in offers:
            locations = o.get("stellenlokationen") or [{}]
            adresse = (locations[0] or {}).get("adresse", {}) or {}
            rows.append({
                "refnr": o.get("referenznummer"),
                "search_term": term,
                "title": o.get("stellenangebotsTitel"),
                "role": o.get("hauptberuf"),
                "employer": o.get("firma"),
                "city": adresse.get("ort"),
                "region": adresse.get("region"),
                "homeoffice": o.get("homeofficemoeglich"),
                "fulltime": o.get("arbeitszeitVollzeit"),
                "contract": o.get("vertragsdauer"),
                "published": o.get("datumErsteVeroeffentlichung"),
            })
        time.sleep(1)  # be polite to the server
    print(f"Done: {term}")

df = pd.DataFrame(rows).drop_duplicates(subset="refnr")
df["collected_on"] = date.today().isoformat()
df.to_csv("data/jobs_real.csv", index=False)

print(f"\nSaved {len(df)} postings to data/jobs_real.csv")
print(df.head())