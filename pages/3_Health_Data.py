import streamlit as st
import sqlite3
import pandas as pd

# Database connection
conn = sqlite3.connect("health_data.db")
cursor = conn.cursor()

# Create health data table
cursor.execute("""
CREATE TABLE IF NOT EXISTS health_data (
    id INTEGER PRIMARY KEY AUTOINCREMENT,
    date TEXT,
    weight REAL,
    steps INTEGER,
    sleep REAL
)
""")

conn.commit()

# Page title
st.title("📊 Health Data")
st.write("Log and track your daily health metrics.")

# Input section
st.subheader("Enter Health Data")

date = st.date_input("📅 Date")

weight = st.number_input(
    "⚖️ Weight (kg)",
    min_value=0.0,
    step=0.1
)

steps = st.number_input(
    "👟 Steps",
    min_value=0,
    step=100
)

sleep = st.number_input(
    "😴 Sleep (hours)",
    min_value=0.0,
    max_value=24.0,
    step=0.5
)

# Save health data
if st.button("Save Health Data"):
    cursor.execute(
        """
        INSERT INTO health_data
        (date, weight, steps, sleep)
        VALUES (?, ?, ?, ?)
        """,
        (str(date), weight, steps, sleep)
    )

    conn.commit()
    st.success("Health data saved successfully! ✅")

# Health history
st.subheader("📋 Your Health History")

cursor.execute(
    "SELECT date, weight, steps, sleep FROM health_data ORDER BY id DESC"
)

data = cursor.fetchall()

if data:
    df_history = pd.DataFrame(
        data,
        columns=["Date", "Weight (kg)", "Steps", "Sleep (hours)"]
    )

    st.dataframe(
        df_history,
        use_container_width=True
    )
else:
    st.info("No health data available yet.")

# Health charts
st.subheader("📊 Health Trends")

cursor.execute(
    "SELECT date, weight, steps, sleep FROM health_data ORDER BY id"
)

chart_data = cursor.fetchall()

if chart_data:
    df = pd.DataFrame(
        chart_data,
        columns=["Date", "Weight", "Steps", "Sleep"]
    )

    df["Date"] = pd.to_datetime(df["Date"])

    # Weight chart
    st.subheader("⚖️ Weight Trend")
    st.line_chart(
        df.set_index("Date")["Weight"]
    )

    # Steps chart
    st.subheader("👟 Steps Trend")
    st.line_chart(
        df.set_index("Date")["Steps"]
    )

    # Sleep chart
    st.subheader("😴 Sleep Trend")
    st.line_chart(
        df.set_index("Date")["Sleep"]
    )

else:
    st.info("No health data available for charts.")

# Close database connection
conn.close()
