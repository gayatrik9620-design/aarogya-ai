import streamlit as st
import sqlite3

st.title("🩺 Aarogya AI")
st.write("Your AI-powered health companion.")

# Connect to database
conn = sqlite3.connect("health_data.db")
cursor = conn.cursor()

# Get latest health record
cursor.execute("""
    SELECT weight, steps, sleep
    FROM health_data
    ORDER BY id DESC
    LIMIT 1
""")

data = cursor.fetchone()

st.subheader("📊 Health Summary")

if data:
    weight, steps, sleep = data

    col1, col2, col3 = st.columns(3)

    with col1:
        st.metric("⚖️ Weight", f"{weight} kg")

    with col2:
        st.metric("👟 Steps", f"{steps}")

    with col3:
        st.metric("😴 Sleep", f"{sleep} hrs")

else:
    st.info("No health data available yet. Add your data from the Health Data page.")

conn.close()