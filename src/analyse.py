import pandas as pd
import matplotlib.pyplot as plt
from pathlib import Path

df = pd.read_csv("data/jobs_real.csv")
totals = pd.read_csv("data/term_totals.csv")
collected = df["collected_on"].iloc[0]

print(df.head())
print(f"\nPostings analysed: {len(df)} (collected {collected})")

Path("outputs").mkdir(exist_ok=True)

# Chart 1: top cities in the collected sample
df["city"].value_counts().head(10).sort_values().plot(kind="barh")
plt.title(f"Top 10 cities in collected postings ({collected})")
plt.xlabel("Postings")
plt.tight_layout()
plt.savefig("outputs/jobs_by_city.png")
plt.close()

# Chart 2: total live postings per search term
totals.set_index("search_term")["total_postings"].plot(kind="bar")
plt.title(f"Live postings per search term in Germany ({collected})")
plt.ylabel("Postings")
plt.xticks(rotation=20)
plt.tight_layout()
plt.savefig("outputs/postings_by_role.png")
plt.close()

print("\nCharts saved in the outputs folder.")
