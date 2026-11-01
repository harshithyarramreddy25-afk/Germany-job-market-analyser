import pandas as pd
import matplotlib.pyplot as plt
from pathlib import Path

df = pd.read_csv("data/jobs_real.csv")
collected = df["collected_on"].iloc[0]

print(df.head())
print(f"\nPostings analysed: {len(df)} (collected {collected})")

Path("outputs").mkdir(exist_ok=True)

# Chart 1: top cities
df["city"].value_counts().head(10).sort_values().plot(kind="barh")
plt.title(f"Top 10 cities in collected postings ({collected})")
plt.xlabel("Postings")
plt.tight_layout()
plt.savefig("outputs/jobs_by_city.png")
plt.close()

# Chart 2: share of postings that allow home office, per search term
share = df.groupby("search_term")["homeoffice"].mean().mul(100).round(1)
print("\nHome office share (%):")
print(share)

share.plot(kind="bar")
plt.title(f"Home office possible, % of postings ({collected})")
plt.ylabel("% of postings")
plt.xticks(rotation=20)
plt.tight_layout()
plt.savefig("outputs/homeoffice_by_role.png")
plt.close()

print("\nCharts saved in the outputs folder.")