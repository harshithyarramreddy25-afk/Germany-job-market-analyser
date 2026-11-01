import pandas as pd
import streamlit as st

st.set_page_config(page_title="Germany Job Market Analyser", layout="wide")
st.title("Germany Job Market Analyser")

df = pd.read_csv("data/jobs_real.csv")
df["homeoffice"] = df["homeoffice"].fillna(False).astype(bool)

st.caption(
    f"Source: Bundesagentur für Arbeit · collected {df['collected_on'].iloc[0]} "
    f"· {len(df)} postings in sample"
)

# Sidebar filters
all_terms = sorted(df["search_term"].unique())
terms = st.sidebar.multiselect("Search term", all_terms, default=all_terms)
cities = st.sidebar.multiselect("City (optional)", sorted(df["city"].dropna().unique()))
homeoffice_only = st.sidebar.checkbox("Home office possible only")

filtered = df[df["search_term"].isin(terms)]
if cities:
    filtered = filtered[filtered["city"].isin(cities)]
if homeoffice_only:
    filtered = filtered[filtered["homeoffice"]]

# Key numbers
c1, c2, c3 = st.columns(3)
c1.metric("Postings", len(filtered))
c2.metric("Cities", filtered["city"].nunique())
share = filtered["homeoffice"].mean() * 100 if len(filtered) else 0
c3.metric("Home office possible", f"{share:.1f}%")

# Charts
left, right = st.columns(2)
with left:
    st.subheader("Top cities")
    st.bar_chart(filtered["city"].value_counts().head(10))
with right:
    st.subheader("Top employers")
    st.bar_chart(filtered["employer"].value_counts().head(10))

st.subheader("Postings")
st.dataframe(
    filtered[["title", "employer", "city", "region", "homeoffice", "published"]],
    width="stretch",
)