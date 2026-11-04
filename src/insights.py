import duckdb

DB = "data/jobs.duckdb"

def _query(sql):
    con = duckdb.connect(DB, read_only=True)
    df = con.execute(sql).df()
    con.close()
    return df

def postings_per_week():
    return _query("""
        SELECT date_trunc('week', CAST(published AS DATE)) AS week,
               COUNT(*) AS postings
        FROM postings
        WHERE published IS NOT NULL
        GROUP BY 1 ORDER BY 1
    """)

def homeoffice_by_term():
    return _query("""
        SELECT search_term,
               ROUND(AVG(CAST(homeoffice AS INT)) * 100, 1) AS homeoffice_pct
        FROM postings GROUP BY 1 ORDER BY 2 DESC
    """)