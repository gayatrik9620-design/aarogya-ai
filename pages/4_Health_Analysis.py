import streamlit as st
import sqlite3
import pandas as pd
import matplotlib.pyplot as plt

# Page title
st.title("📊 Health Analysis")
st.write("Analyze your recorded health data and view simple trends.")

# Connect to database
try:
    conn = sqlite3.connect("health_data.db")

    query = """
    SELECT date, weight, steps, sleep
    FROM health_data
    ORDER BY date
    """

    df = pd.read_sql_query(query, conn)
    conn.close()

except Exception as e:
    st.error(f"Unable to load health data: {e}")
    st.stop()


# Check whether data exists
if df.empty:
    st.warning("⚠️ No health data available yet.")
    st.info("Please add your health data from the Health Data page.")

else:
    # Convert date column
    df["date"] = pd.to_datetime(df["date"], errors="coerce")

    # Remove invalid dates
    df = df.dropna(subset=["date"])

    st.success(f"✅ {len(df)} health record(s) found.")

    # --------------------------------
    # Latest Health Record
    # --------------------------------

    st.subheader("📌 Latest Health Record")

    latest = df.iloc[-1]

    col1, col2, col3 = st.columns(3)

    with col1:
        st.metric(
            "Weight",
            f"{latest['weight']:.1f} kg"
        )

    with col2:
        st.metric(
            "Steps",
            f"{latest['steps']:.0f}"
        )

    with col3:
        st.metric(
            "Sleep",
            f"{latest['sleep']:.1f} hrs"
        )

    # --------------------------------
    # Weight Analysis
    # --------------------------------

    st.subheader("⚖️ Weight Trend")

    fig1, ax1 = plt.subplots()

    ax1.plot(
        df["date"],
        df["weight"],
        marker="o"
    )

    ax1.set_xlabel("Date")
    ax1.set_ylabel("Weight (kg)")
    ax1.set_title("Weight Over Time")

    plt.xticks(rotation=45)
    plt.tight_layout()

    st.pyplot(fig1)

    # --------------------------------
    # Steps Analysis
    # --------------------------------

    st.subheader("🚶 Steps Trend")

    fig2, ax2 = plt.subplots()

    ax2.plot(
        df["date"],
        df["steps"],
        marker="o"
    )

    ax2.set_xlabel("Date")
    ax2.set_ylabel("Steps")
    ax2.set_title("Daily Steps Over Time")

    plt.xticks(rotation=45)
    plt.tight_layout()

    st.pyplot(fig2)

    # --------------------------------
    # Sleep Analysis
    # --------------------------------

    st.subheader("😴 Sleep Trend")

    fig3, ax3 = plt.subplots()

    ax3.plot(
        df["date"],
        df["sleep"],
        marker="o"
    )

    ax3.set_xlabel("Date")
    ax3.set_ylabel("Sleep (hours)")
    ax3.set_title("Sleep Duration Over Time")

    plt.xticks(rotation=45)
    plt.tight_layout()

    st.pyplot(fig3)

    # --------------------------------
    # Basic Statistics
    # --------------------------------

    st.subheader("📋 Health Statistics")

    col1, col2, col3 = st.columns(3)

    with col1:
        avg_weight = df["weight"].mean()
        st.metric(
            "Average Weight",
            f"{avg_weight:.2f} kg"
        )

    with col2:
        avg_steps = df["steps"].mean()
        st.metric(
            "Average Steps",
            f"{avg_steps:.0f}"
        )

    with col3:
        avg_sleep = df["sleep"].mean()
        st.metric(
            "Average Sleep",
            f"{avg_sleep:.2f} hrs"
        )

    # --------------------------------
    # Data Table
    # --------------------------------

    st.subheader("📑 Recorded Health Data")

    display_df = df.copy()

    display_df["date"] = display_df["date"].dt.strftime("%Y-%m-%d")

    st.dataframe(
        display_df,
        use_container_width=True
    )

    # --------------------------------
    # Simple Analysis Message
    # --------------------------------

    st.subheader("💡 Summary")

    st.write(
        "This dashboard provides a simple visualization of your "
        "recorded weight, daily steps, and sleep data."
    )

    st.caption(
        "Disclaimer: This analysis is for general wellness tracking "
        "and is not a medical diagnosis or medical advice."
    )