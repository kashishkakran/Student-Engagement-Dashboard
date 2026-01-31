# src/visuals.py
import plotly.express as px
import pandas as pd

def hist_engagement(df: pd.DataFrame):
    return px.histogram(
        df, x="engagement_score", nbins=30, title="Distribution of Engagement Score",
        color="Class", barmode="overlay", opacity=0.75
    )

def box_by_class(df: pd.DataFrame):
    return px.box(
        df, x="Class", y="engagement_score", color="Class",
        title="Engagement by Class (L/M/H)"
    )

def bar_topic(df: pd.DataFrame, top_n: int = 10):
    topic_mean = (df.groupby("Topic", observed=True)["engagement_score"]
                    .mean().sort_values(ascending=False).head(top_n).reset_index())
    return px.bar(topic_mean, x="Topic", y="engagement_score",
                  title=f"Top {top_n} Topics by Mean Engagement", text_auto=True)

def scatter_resources_vs_hands(df: pd.DataFrame):
    return px.scatter(df, x="VisITedResources", y="raisedhands",
                      color="Class", trendline="ols",
                      title="Visited Resources vs Raised Hands")
