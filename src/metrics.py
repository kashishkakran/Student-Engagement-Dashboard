# src/metrics.py
import pandas as pd

def kpis(df: pd.DataFrame) -> dict:
    return {
        "N Students": len(df),
        "Mean Engagement": round(df["engagement_score"].mean(), 2),
        "Median Engagement": round(df["engagement_score"].median(), 2),
        "Engagement-Score ↔ Class (corr)": round(df["engagement_score"].corr(df["Class_num"]), 3)
    }

def by_class(df: pd.DataFrame) -> pd.DataFrame:
    return (df
        .groupby("Class", observed=True)
        [["engagement_score","raisedhands","VisITedResources","AnnouncementsView","Discussion"]]
        .mean()
        .round(2)
        .reset_index())

def by_topic(df: pd.DataFrame) -> pd.DataFrame:
    return (df
        .groupby("Topic", observed=True)["engagement_score"]
        .mean()
        .round(2)
        .sort_values(ascending=False)
        .reset_index())