# Student Engagement Dashboard

A clean Streamlit app analyzing the **xAPI-Edu-Data** dataset and visualizing student engagement.

## Features

- Data cleaning + engineered **engagement_score** (0-100)
- KPIs & interactive filters (Stage, Grade, Topic, Absence, Relation)
- Visuals: Histogram, Box by Class, Top Topics, Scatter (resources vs hands)

## Tech

- Python, Pandas, Plotly, Streamlit
- Project structured for clarity and interviews

## Setup (Mac)

```bash
python3 -m venv .venv
source .venv/bin/activate
pip install -r requirements.txt
# put the raw file at data/raw/xAPI-Edu-Data.csv.xls
streamlit run app.py
```
