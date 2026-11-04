import sys
import datetime
import duckdb
import pandas as pd

DB = "data/jobs.duckdb"

def load_snapshot(csv_path):
    df = pd.read_csv(csv_path)
    if "collected_date" not in df.columns:
        df["collected_date"] = datetime.date.today().isoformat()
    # unique key per posting (so the same job is not saved twice)
    df["job_key"] = (
        df["title"].astype(str) + "|" + df["employer"].astype(str) + "|"
        + df["city"].astype(str) + "|" + df["published"].astype(str)
    )
    con = duckdb.connect(DB)
    con.register("new_df", df)
    con.execute("CREATE TABLE IF NOT EXISTS postings AS SELECT * FROM new_df LIMIT 0")
    con.execute("""
        INSERT INTO postings
        SELECT * FROM new_df
        WHERE job_key NOT IN (SELECT job_key FROM postings)
    """)
    total = con.execute("SELECT COUNT(*) FROM postings").fetchone()[0]
    con.close()
    return total

if __name__ == "__main__":
    print("Total postings in database:", load_snapshot(sys.argv[1]))