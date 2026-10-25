import streamlit as st
import sqlite3
import pandas as pd

st.set_page_config(page_title="Health Report", page_icon="📋")

st.title("📋 Health Report")
st.write("Generate a simple summary of your health data.")

try:
    conn = sqlite3.connect("health_data.db")

    query = """
    SELECT date, weight, steps, sleep
    FROM health_data
    ORDER BY date DESC
    """

    df = pd.read_sql_query(query, conn)
    conn.close()

    if df.empty:
        st.info("No health data available. Please add data first.")
    else:
        st.subheader("Health Summary")

        latest = df.iloc[0]

        col1, col2, col3 = st.columns(3)

        with col1:
            st.metric("Weight", f"{latest['weight']} kg")

        with col2:
            st.metric("Steps", f"{latest['steps']}")

        with col3:
            st.metric("Sleep", f"{latest['sleep']} hrs")

        st.subheader("Health Data")
        st.dataframe(df, use_container_width=True)

        st.subheader("Report")
        st.write(
            f"Latest recorded weight is {latest['weight']} kg, "
            f"with {latest['steps']} steps and {latest['sleep']} hours of sleep."
        )

except Exception as e:
    st.error(f"Error: {str(e)}")