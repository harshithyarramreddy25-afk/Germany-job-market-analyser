import time
from datetime import date

import pandas as pd
import requests

URL = "https://rest.arbeitsagentur.de/jobboerse/jobsuche-service/pc/v4/jobs"
HEADERS = {"X-API-Key": "jobboerse-jobsuche"}

SEARCH_TERMS = ["Data Scientist", "Data Analyst", "Data Engineer", "Machine Learning"]
PAGES = 4    # 4 pages x 50 = up to 200 postings per search term
SIZE = 50

rows = []
totals = []

for term in SEARCH_TERMS:
    for page in range(1, PAGES + 1):
        params = {"was": term, "angebotsart": 1, "page": page, "size": SIZE}
        r = requests.get(URL, headers=HEADERS, params=params, timeout=30)
        if r.status_code != 200:
            print(f"{term} page {page}: HTTP {r.status_code}, stopping this term")
            break

        data = r.json()
        if page == 1:
            totals.append({"search_term": term, "total_postings": data.get("maxErgebnisse")})

        offers = data.get("stellenangebote", [])
        if not offers:
            break

        for o in offers:
            ort = o.get("arbeitsort", {}) or {}
            rows.append({
                "refnr": o.get("refnr"),
                "search_term": term,
                "title": o.get("titel"),
                "employer": o.get("arbeitgeber"),
                "city": ort.get("ort"),
                "region": ort.get("region"),
                "published": o.get("aktuelleVeroeffentlichungsdatum"),
            })
        time.sleep(1)  # be polite to the server
    print(f"Done: {term}")

df = pd.DataFrame(rows).drop_duplicates(subset="refnr")
df["collected_on"] = date.today().isoformat()
df.to_csv("data/jobs_real.csv", index=False)

pd.DataFrame(totals).to_csv("data/term_totals.csv", index=False)

print(f"\nSaved {len(df)} postings to data/jobs_real.csv")
print(pd.DataFrame(totals))