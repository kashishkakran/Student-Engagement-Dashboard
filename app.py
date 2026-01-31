# app.py
import streamlit as st
import pandas as pd

from src.load_data import load_raw, save_processed
from src.preprocess import clean_and_engineer
from src.metrics import kpis
from src.visuals import (
    hist_engagement,
    box_by_class,
    bar_topic,
    scatter_resources_vs_hands
)

st.set_page_config(page_title="Student Engagement Dashboard", page_icon="📊", layout="wide")


@st.cache_data
def prepare_data():
    raw = load_raw()
    df = clean_and_engineer(raw)
    save_processed(df)
    return df


def sidebar_filters(df: pd.DataFrame):
    st.sidebar.header("🔎 Filters")

    # Optional: reset filters button
    if "reset_filters" not in st.session_state:
        st.session_state.reset_filters = 0

    if st.sidebar.button("♻️ Reset filters"):
        st.session_state.reset_filters += 1

    # Helper: default to all values selected
    def all_values(col):
        return sorted(df[col].dropna().unique().tolist())

    stage_all = all_values("StageID")
    grade_all = all_values("GradeID")
    topic_all = all_values("Topic")
    absence_all = all_values("StudentAbsenceDays")
    relation_all = all_values("Relation")
    class_all = all_values("Class")
    gender_all = all_values("gender")
    semester_all = all_values("Semester")

    # Filters (defaults = ALL selected)
    stage = st.sidebar.multiselect(
        "Stage",
        stage_all,
        default=stage_all,
        key=f"stage_{st.session_state.reset_filters}",
    )
    grade = st.sidebar.multiselect(
        "Grade",
        grade_all,
        default=grade_all,
        key=f"grade_{st.session_state.reset_filters}",
    )
    topic = st.sidebar.multiselect(
        "Topic",
        topic_all,
        default=topic_all,
        key=f"topic_{st.session_state.reset_filters}",
    )
    semester = st.sidebar.multiselect(
        "Semester",
        semester_all,
        default=semester_all,
        key=f"semester_{st.session_state.reset_filters}",
    )
    gender = st.sidebar.multiselect(
        "Gender",
        gender_all,
        default=gender_all,
        key=f"gender_{st.session_state.reset_filters}",
    )
    student_class = st.sidebar.multiselect(
        "Performance Class",
        class_all,
        default=class_all,
        key=f"class_{st.session_state.reset_filters}",
    )
    absence = st.sidebar.multiselect(
        "Absence Days",
        absence_all,
        default=absence_all,
        key=f"absence_{st.session_state.reset_filters}",
    )
    relation = st.sidebar.multiselect(
        "Parent Relation",
        relation_all,
        default=relation_all,
        key=f"relation_{st.session_state.reset_filters}",
    )

    # Apply mask
    mask = pd.Series(True, index=df.index)
    mask &= df["StageID"].isin(stage)
    mask &= df["GradeID"].isin(grade)
    mask &= df["Topic"].isin(topic)
    mask &= df["Semester"].isin(semester)
    mask &= df["gender"].isin(gender)
    mask &= df["Class"].isin(student_class)
    mask &= df["StudentAbsenceDays"].isin(absence)
    mask &= df["Relation"].isin(relation)

    return df[mask]


def main():
    st.title("📊 Student Engagement Analytics Dashboard")
    st.caption("Built with Python + Streamlit | by Kashish Kakran")

    with st.spinner("Loading & cleaning data..."):
        df = prepare_data()

    # Filters
    dff = sidebar_filters(df)

    # If filter results empty
    if dff.empty:
        st.warning("No data matches the selected filters. Try resetting filters.")
        st.stop()

    # =========================
    # KPI ROW
    # =========================
    st.subheader("Key Metrics")

    stats = kpis(dff)

    # Extra KPIs (derived from raw columns)
    avg_absence = round(dff["StudentAbsenceDays"].map(
        {"Under-7": 0, "Above-7": 1}
    ).mean(), 2) if "StudentAbsenceDays" in dff.columns else None

    top_topic = dff["Topic"].value_counts().idxmax() if "Topic" in dff.columns else "-"
    top_class = dff["Class"].value_counts().idxmax() if "Class" in dff.columns else "-"

    c1, c2, c3, c4, c5 = st.columns(5)
    c1.metric("Students", stats["N Students"])
    c2.metric("Mean Engagement", stats["Mean Engagement"])
    c3.metric("Median Engagement", stats["Median Engagement"])
    c4.metric("Most Common Topic", top_topic)
    c5.metric("Most Common Class", top_class)

    st.divider()

    # Visuals 
    st.subheader("Visual Insights")

    # Row 1
    col1, col2 = st.columns(2)
    with col1:
        st.plotly_chart(hist_engagement(dff), width="stretch")
    with col2:
        st.plotly_chart(box_by_class(dff), width="stretch")

    # Row 2
    col3, col4 = st.columns(2)
    with col3:
        st.plotly_chart(bar_topic(dff, top_n=10), width="stretch")
    with col4:
        st.plotly_chart(scatter_resources_vs_hands(dff), width="stretch")

    st.divider()

    
    # Data table
    st.subheader("Data Preview")

    with st.expander("Preview Filtered & Processed Data"):
        st.dataframe(dff.head(100), width="stretch")


if __name__ == "__main__":
    main()
