import sys
import time
from pathlib import Path

import altair as alt
import pandas as pd
import streamlit as st

SRC_DIR = Path(__file__).resolve().parents[1]
if str(SRC_DIR) not in sys.path:
    sys.path.append(str(SRC_DIR))

from analytics.data_utils import (
    build_quality_summary,
    clean_interactions,
    fetch_interactions,
    prepare_ml_dataset,
)

st.set_page_config(page_title="Flexmedia Totem Analytics", layout="wide", page_icon="🤖")

# Custom CSS for "Premium" look
st.markdown("""
<style>
    .big-font {
        font-size:30px !important;
        font-weight: bold;
        color: #4CAF50;
    }
    .metric-card {
        background-color: #f0f2f6;
        padding: 20px;
        border-radius: 10px;
        border-left: 5px solid #4CAF50;
    }
</style>
""", unsafe_allow_html=True)

# Sidebar
with st.sidebar:
    st.image("https://cdn-icons-png.flaticon.com/512/4712/4712035.png", width=100) # Placeholder Icon
    st.title("Flexmedia Totem")
    st.markdown("---")
    st.write("**Status:** 🟢 Online")
    st.write("**Location:** Shopping Center Floor 1")
    st.write("**ID:** TOTEM-001")
    st.markdown("---")
    if st.button("Reset Database"):
        import sqlite3
        from database.db_manager import DB_PATH

        conn = sqlite3.connect(DB_PATH)
        conn.execute("DELETE FROM interactions")
        conn.commit()
        conn.close()
        st.success("Database cleared!")

st.title("🤖 Totem Intelligence Center")
st.markdown("Real-time monitoring of user interactions and sensor data.")

# Auto-refresh logic
placeholder = st.empty()

def run_ml_insights(df: pd.DataFrame):
    dataset = prepare_ml_dataset(df)
    if dataset.empty or dataset["label"].nunique() < 2:
        return None

    feature_cols = ["duration", "touch_x", "touch_y"]
    X = dataset[feature_cols]
    y = dataset["label"]

    from sklearn.model_selection import train_test_split
    from sklearn.pipeline import Pipeline
    from sklearn.preprocessing import StandardScaler
    from sklearn.linear_model import LogisticRegression
    from sklearn.metrics import accuracy_score

    X_train, X_test, y_train, y_test = train_test_split(
        X, y, test_size=0.2, stratify=y, random_state=42
    )

    pipeline = Pipeline(
        [
            ("scaler", StandardScaler()),
            ("clf", LogisticRegression(max_iter=300)),
        ]
    )

    pipeline.fit(X_train, y_train)
    preds = pipeline.predict(X_test)
    accuracy = accuracy_score(y_test, preds)
    latest_event = dataset.iloc[-1]
    latest_pred = pipeline.predict(latest_event[feature_cols].values.reshape(1, -1))[0]
    return {
        "accuracy": accuracy,
        "samples": len(dataset),
        "latest_label": latest_event["label"],
        "latest_prediction": latest_pred,
    }


while True:
    raw_df = fetch_interactions(limit=1000)
    df = clean_interactions(raw_df)
    summary = build_quality_summary(df)
    
    with placeholder.container():
        if df.empty:
            st.info("⏳ Waiting for sensor data... Start the simulation script.")
        else:
            # KPIs
            col1, col2, col3, col4 = st.columns(4)
            with col1:
                st.metric("Total Interactions", summary["total"], delta=1 if len(df) > 0 else 0)
            with col2:
                st.metric("Avg Dwell Time", f"{summary['avg_duration']:.1f} s", delta_color="normal")
            with col3:
                last_type = df.iloc[0]['sensor_type'].upper()
                st.metric("Last Action", last_type)
            with col4:
                st.metric("Touch Events %", f"{summary['touch_pct']}%")
            
            st.markdown("---")

            # Charts
            col_chart1, col_chart2 = st.columns([2, 1])
            
            with col_chart1:
                st.subheader("📈 Activity Timeline")
                chart_time = alt.Chart(df).mark_circle(size=60).encode(
                    x='timestamp',
                    y='duration',
                    color=alt.Color('sensor_type', legend=alt.Legend(title="Sensor Type")),
                    tooltip=['timestamp', 'sensor_type', 'value', 'duration']
                ).interactive()
                st.altair_chart(chart_time, use_container_width=True)
            
            with col_chart2:
                st.subheader("📊 Distribution")
                chart_type = alt.Chart(df).mark_arc(innerRadius=50).encode(
                    theta=alt.Theta(field="sensor_type", aggregate="count"),
                    color=alt.Color(field="sensor_type"),
                    tooltip=['sensor_type', 'count()']
                )
                st.altair_chart(chart_type, use_container_width=True)
            
            # Data Table
            st.subheader("📝 Live Logs")
            st.dataframe(
                df[['timestamp', 'sensor_type', 'value', 'duration']].head(10),
                use_container_width=True,
                hide_index=True
            )

            st.markdown("---")
            st.subheader("🧠 ML Insights (toque curto x longo)")
            ml_summary = run_ml_insights(df)
            if ml_summary:
                st.metric("Acurácia", f"{ml_summary['accuracy']*100:.1f}%")
                st.write(
                    f"Última interação real: **{ml_summary['latest_label']}** | "
                    f"Predição do modelo: **{ml_summary['latest_prediction']}**"
                )
                st.caption(
                    f"Modelo treinado dinamicamente com {ml_summary['samples']} eventos de toque limpos."
                )
            else:
                st.info("Aguardando mais eventos de toque para treinar o modelo supervisionado.")
            
    time.sleep(1) # Faster refresh for demo
