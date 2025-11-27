import streamlit as st
import pandas as pd
import sqlite3
import os
import time
import altair as alt

# Database Path
DB_PATH = os.path.join(os.path.dirname(os.path.dirname(os.path.dirname(__file__))), 'data', 'totem.db')

def load_data():
    """Loads data from the SQLite database."""
    if not os.path.exists(DB_PATH):
        # Initialize DB if it doesn't exist to avoid "no such table" error
        # We need to import init_db dynamically or duplicate logic to avoid circular imports if structure changes
        # For simplicity, we'll just return empty DF, but better to handle gracefully.
        # Actually, let's just create the table here too if needed.
        conn = sqlite3.connect(DB_PATH)
        cursor = conn.cursor()
        cursor.execute('''
            CREATE TABLE IF NOT EXISTS interactions (
                id INTEGER PRIMARY KEY AUTOINCREMENT,
                timestamp DATETIME DEFAULT CURRENT_TIMESTAMP,
                sensor_type TEXT NOT NULL,
                value TEXT,
                duration REAL
            )
        ''')
        conn.commit()
        conn.close()
        return pd.DataFrame()
    
    conn = sqlite3.connect(DB_PATH)
    try:
        df = pd.read_sql_query("SELECT * FROM interactions ORDER BY timestamp DESC LIMIT 1000", conn)
    except pd.errors.DatabaseError:
        # Table might not exist yet. Let's try to create it.
        cursor = conn.cursor()
        cursor.execute('''
            CREATE TABLE IF NOT EXISTS interactions (
                id INTEGER PRIMARY KEY AUTOINCREMENT,
                timestamp DATETIME DEFAULT CURRENT_TIMESTAMP,
                sensor_type TEXT NOT NULL,
                value TEXT,
                duration REAL
            )
        ''')
        conn.commit()
        # Try reading again (it will be empty, but no error)
        return pd.DataFrame()
    finally:
        conn.close()
    
    if not df.empty:
        df['timestamp'] = pd.to_datetime(df['timestamp'])
    return df

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
        conn = sqlite3.connect(DB_PATH)
        conn.execute("DELETE FROM interactions")
        conn.commit()
        conn.close()
        st.success("Database cleared!")

st.title("🤖 Totem Intelligence Center")
st.markdown("Real-time monitoring of user interactions and sensor data.")

# Auto-refresh logic
placeholder = st.empty()

while True:
    df = load_data()
    
    with placeholder.container():
        if df.empty:
            st.info("⏳ Waiting for sensor data... Start the simulation script.")
        else:
            # KPIs
            col1, col2, col3, col4 = st.columns(4)
            with col1:
                st.metric("Total Interactions", len(df), delta=1 if len(df) > 0 else 0)
            with col2:
                avg_duration = df['duration'].mean()
                st.metric("Avg Dwell Time", f"{avg_duration:.1f} s", delta_color="normal")
            with col3:
                last_type = df.iloc[0]['sensor_type'].upper()
                st.metric("Last Action", last_type)
            with col4:
                st.metric("Active Sensors", "3")
            
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
            
    time.sleep(1) # Faster refresh for demo
