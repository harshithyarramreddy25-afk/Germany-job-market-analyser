import pandas as pd
import matplotlib.pyplot as plt

# Sample data (we'll replace this with real job data later)
data = {
    "job_title": ["Data Scientist", "Data Analyst", "ML Engineer", "Data Engineer"],
    "city": ["Berlin", "Munich", "Koblenz", "Hamburg"],
    "openings": [120, 200, 45, 90],
}

df = pd.DataFrame(data)
print(df)

df.plot(kind="bar", x="job_title", y="openings", legend=False)
plt.title("Sample job openings in Germany")
plt.ylabel("Openings")
plt.tight_layout()
plt.show()