import pandas as pd
import matplotlib.pyplot as plt
from pathlib import Path

# Load data
df = pd.read_csv("data/jobs_sample.csv")
print(df.head())
print(f"\nTotal postings: {len(df)}")

# Folder for charts
Path("outputs").mkdir(exist_ok=True)

# Chart 1: postings by city
df["city"].value_counts().plot(kind="bar")
plt.title("Job postings by city (sample data)")
plt.ylabel("Postings")
plt.tight_layout()
plt.savefig("outputs/jobs_by_city.png")
plt.close()

# Chart 2: most requested skills
skills = df["skills"].str.split(";").explode().str.strip()
top_skills = skills.value_counts().head(8)
print("\nTop skills:")
print(top_skills)

top_skills.sort_values().plot(kind="barh")
plt.title("Most requested skills (sample data)")
plt.xlabel("Postings")
plt.tight_layout()
plt.savefig("outputs/top_skills.png")
plt.close()

print("\nCharts saved in the outputs folder.")