import os
import re
import sqlite3
from typing import Dict, Tuple

import pandas as pd

# Determine database path (repo_root/data/totem.db)
DB_PATH = os.path.join(
    os.path.dirname(os.path.dirname(os.path.dirname(os.path.abspath(__file__)))),
    "data",
    "totem.db",
)


def _ensure_database():
    """Guarantee that the SQLite file and table exist before any read."""
    os.makedirs(os.path.dirname(DB_PATH), exist_ok=True)
    conn = sqlite3.connect(DB_PATH)
    cursor = conn.cursor()
    cursor.execute(
        """
        CREATE TABLE IF NOT EXISTS interactions (
            id INTEGER PRIMARY KEY AUTOINCREMENT,
            timestamp DATETIME DEFAULT CURRENT_TIMESTAMP,
            sensor_type TEXT NOT NULL,
            value TEXT,
            duration REAL
        )
        """
    )
    conn.commit()
    conn.close()


def fetch_interactions(limit: int = 1000) -> pd.DataFrame:
    """Fetch raw interactions from SQLite ordered by timestamp DESC."""
    _ensure_database()
    conn = sqlite3.connect(DB_PATH)
    try:
        df = pd.read_sql_query(
            "SELECT * FROM interactions ORDER BY timestamp DESC LIMIT ?",
            conn,
            params=(limit,),
        )
    finally:
        conn.close()
    return df


def parse_touch_coordinates(value: str) -> Tuple[float, float]:
    """Extract X/Y coordinates from a touch value string."""
    if not isinstance(value, str):
        return (None, None)
    match = re.search(r"x:(?P<x>\d+),y:(?P<y>\d+)", value)
    if not match:
        return (None, None)
    return (float(match.group("x")), float(match.group("y")))


def clean_interactions(df: pd.DataFrame) -> pd.DataFrame:
    """Normalize columns, drop duplicates and enforce numeric types."""
    if df.empty:
        return df

    df = df.copy()
    df["timestamp"] = pd.to_datetime(df["timestamp"])
    df["sensor_type"] = df["sensor_type"].str.lower().str.strip()
    df["value"] = df["value"].fillna("")
    df["duration"] = pd.to_numeric(df["duration"], errors="coerce").fillna(0.0)
    df["duration"] = df["duration"].clip(lower=0.0)

    df = df.sort_values("timestamp").drop_duplicates(
        subset=["timestamp", "sensor_type", "value"], keep="last"
    )
    df.reset_index(drop=True, inplace=True)

    # Feature extraction for touch events
    df["touch_x"] = None
    df["touch_y"] = None
    touch_mask = df["sensor_type"] == "touch"
    if touch_mask.any():
        coords = df.loc[touch_mask, "value"].apply(parse_touch_coordinates)
        df.loc[touch_mask, "touch_x"] = [c[0] for c in coords]
        df.loc[touch_mask, "touch_y"] = [c[1] for c in coords]

    return df


def build_quality_summary(df: pd.DataFrame) -> Dict[str, float]:
    """Provide quick stats for dashboard copy."""
    if df.empty:
        return {"total": 0, "touch_pct": 0.0, "avg_duration": 0.0}
    total = len(df)
    touch_pct = (
        len(df[df["sensor_type"] == "touch"]) / total * 100 if total else 0.0
    )
    return {
        "total": total,
        "touch_pct": round(touch_pct, 1),
        "avg_duration": round(df["duration"].mean(), 2),
    }


def prepare_ml_dataset(df: pd.DataFrame) -> pd.DataFrame:
    """Return only touch rows with engineered features for ML."""
    if df.empty:
        return pd.DataFrame()

    touch_df = df[df["sensor_type"] == "touch"].copy()
    touch_df.dropna(subset=["touch_x", "touch_y"], inplace=True)

    if touch_df.empty:
        return pd.DataFrame()

    touch_df["label"] = touch_df["duration"].apply(
        lambda d: "long_press" if d >= 1.0 else "short_press"
    )

    feature_cols = ["duration", "touch_x", "touch_y", "label", "timestamp"]
    return touch_df[feature_cols].reset_index(drop=True)

