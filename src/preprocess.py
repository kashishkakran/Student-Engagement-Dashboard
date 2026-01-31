# src/preprocess.py
import pandas as pd
import numpy as np

CAT_COLS_TO_STRIP = [
    "gender","NationalITy","PlaceofBirth","StageID","GradeID","SectionID",
    "Topic","Semester","Relation","ParentAnsweringSurvey",
    "ParentschoolSatisfaction","StudentAbsenceDays","Class"
]

ENGAGEMENT_COLS = ["raisedhands", "VisITedResources", "AnnouncementsView", "Discussion"]

def _standardize_text(df: pd.DataFrame) -> pd.DataFrame:
    for c in CAT_COLS_TO_STRIP:
        if c in df.columns:
            df[c] = (df[c].astype(str)
                           .str.strip()
                           .str.replace(r"\s+", " ", regex=True))
    # simple country name fix examples
    df["NationalITy"] = df["NationalITy"].str.title()
    df["PlaceofBirth"] = df["PlaceofBirth"].str.title()
    # unify Yes/No and Good/Bad
    for c in ["ParentAnsweringSurvey", "ParentschoolSatisfaction"]:
        if c in df.columns:
            df[c] = df[c].str.title()
    if "StudentAbsenceDays" in df.columns:
        df["StudentAbsenceDays"] = df["StudentAbsenceDays"].str.replace("Under-7","Under_7").str.replace("Above-7","Above_7")
    return df

def _coerce_numeric(df: pd.DataFrame) -> pd.DataFrame:
    for c in ENGAGEMENT_COLS:
        if c in df.columns:
            df[c] = pd.to_numeric(df[c], errors="coerce")
    return df

def _engagement_score(df: pd.DataFrame) -> pd.DataFrame:
    # Min-max scale each engagement column to [0,1] then take mean*100 for a 0-100 score
    scaled = []
    for c in ENGAGEMENT_COLS:
        if c in df.columns:
            col = df[c].astype(float)
            rng = col.max() - col.min()
            if rng == 0 or np.isnan(rng):
                scaled.append(pd.Series(np.zeros(len(col)), index=df.index))
            else:
                scaled.append((col - col.min()) / rng)
    if scaled:
        df["engagement_score"] = (pd.concat(scaled, axis=1).mean(axis=1) * 100).round(2)
    else:
        df["engagement_score"] = np.nan
    return df

def _class_order(df: pd.DataFrame) -> pd.DataFrame:
    if "Class" in df.columns:
        # Order: L < M < H
        df["Class"] = pd.Categorical(df["Class"], categories=["L","M","H"], ordered=True)
        df["Class_num"] = df["Class"].cat.codes  # L=0, M=1, H=2
    return df

def clean_and_engineer(df: pd.DataFrame) -> pd.DataFrame:
    df = df.copy()
    df = _standardize_text(df)
    df = _coerce_numeric(df)
    df = _engagement_score(df)
    df = _class_order(df)
    return df
