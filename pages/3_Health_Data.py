import streamlit as st
import sqlite3
import pandas as pd
from datetime import date

# -------------------------------
# 1. DATABASE CONNECTION
# -------------------------------

conn = sqlite3.connect(
    "health_data.db",
    check_same_thread=False
)

conn.execute("""
CREATE TABLE IF NOT EXISTS health_data (
    id INTEGER PRIMARY KEY AUTOINCREMENT,
    date TEXT,
    weight REAL,
    steps INTEGER,
    sleep REAL
)
""")
conn.commit()

# -------------------------------
# 2. PAGE CONFIGURATION
# -------------------------------

st.set_page_config(
    page_title="Healthcare AI Agent",
    page_icon="🏥",
    layout="wide"
)

st.title("🏥 Healthcare Monitoring AI Agent")
st.write(
    "Track your daily health data and view basic health insights."
)

st.info(
    "This application supports health tracking only. "
    "It does not diagnose diseases or replace a doctor."
)

# -------------------------------
# 3. SIDEBAR
# -------------------------------

st.sidebar.title("Navigation")

page = st.sidebar.radio(
    "Choose a section",
    [
        "Dashboard",
        "Enter Health Data",
        "Health Assistant"
    ]
)

# -------------------------------
# 4. ENTER HEALTH DATA
# -------------------------------

if page == "Enter Health Data":

    st.header("📝 Enter Daily Health Data")

    with st.form("health_form"):

        health_date = st.date_input(
            "Select Date",
            value=date.today()
        )

        weight = st.number_input(
            "Weight (kg)",
            min_value=0.0,
            max_value=500.0,
            value=50.0,
            step=0.1
        )

        steps = st.number_input(
            "Daily Steps",
            min_value=0,
            max_value=200000,
            value=0,
            step=100
        )

        sleep = st.number_input(
            "Sleep (hours)",
            min_value=0.0,
            max_value=24.0,
            value=7.0,
            step=0.5
        )

        submitted = st.form_submit_button(
            "Save Health Data"
        )

        if submitted:

            conn.execute(
                """
                INSERT INTO health_data
                (date, weight, steps, sleep)
                VALUES (?, ?, ?, ?)
                """,
                (
                    str(health_date),
                    weight,
                    int(steps),
                    sleep
                )
            )

            conn.commit()

            st.success(
                "Health data saved successfully!"
            )

# -------------------------------
# 5. LOAD HEALTH DATA
# -------------------------------

df = pd.read_sql_query(
    """
    SELECT date, weight, steps, sleep
    FROM health_data
    ORDER BY date DESC, rowid DESC
    """,
    conn
)

# -------------------------------
# 6. DASHBOARD
# -------------------------------

if page == "Dashboard":

    st.header("📊 Health Dashboard")

    if not df.empty:

        latest = df.iloc[0]

        col1, col2, col3 = st.columns(3)

        col1.metric(
            "Latest Weight",
            f"{latest['weight']:.1f} kg"
        )

        col2.metric(
            "Latest Steps",
            f"{int(latest['steps'])}"
        )

        col3.metric(
            "Latest Sleep",
            f"{latest['sleep']:.1f} hours"
        )

        st.subheader("📈 Daily Steps")

        chart_df = df.copy()
        chart_df["date"] = pd.to_datetime(
            chart_df["date"]
        )

        chart_df = chart_df.sort_values("date")

        st.bar_chart(
            chart_df.set_index("date")["steps"]
        )

        st.subheader("💤 Sleep History")

        st.line_chart(
            chart_df.set_index("date")["sleep"]
        )

        st.subheader("📋 Health Records")

        st.dataframe(
            df,
            use_container_width=True
        )

        st.subheader("📥 Download Health Report")

        csv_data = df.to_csv(index=False).encode("utf-8")

        st.download_button(
            label="Download CSV Report",
            data=csv_data,
            file_name="health_report.csv",
            mime="text/csv"
        )

    else:

        st.info(
            "No health data found. "
            "Open Enter Health Data to add your first record."
        )

# -------------------------------
# 7. BASIC HEALTH ASSISTANT TOOL
# -------------------------------

if page == "Health Assistant":

    st.header("🤖 Healthcare AI Assistant")

    st.write(
        "Ask questions about your recorded health data."
    )

    question = st.text_input(
        "Enter your question",
        placeholder=(
            "Example: Show my health summary"
        )
    )

    if st.button("Get Health Insights"):

        if df.empty:

            st.warning(
                "Please enter health data first."
            )

        elif not question.strip():

            st.warning(
                "Please enter a question."
            )

        else:

            q = question.lower()

            if "step" in q or "activity" in q:

                avg_steps = df["steps"].mean()

                st.success(
                    f"Your average recorded daily steps "
                    f"are {avg_steps:.0f}."
                )

            elif "sleep" in q:

                avg_sleep = df["sleep"].mean()

                st.success(
                    f"Your average recorded sleep is "
                    f"{avg_sleep:.1f} hours."
                )

            elif "weight" in q:

                latest_weight = df.iloc[0]["weight"]

                st.success(
                    f"Your latest recorded weight is "
                    f"{latest_weight:.1f} kg."
                )

            elif (
                "summary" in q
                or "health" in q
                or "report" in q
            ):

                st.subheader("Your Health Summary")

                st.write(
                    f"Total records: {len(df)}"
                )

                st.write(
                    f"Average steps: "
                    f"{df['steps'].mean():.0f}"
                )

                st.write(
                    f"Average sleep: "
                    f"{df['sleep'].mean():.1f} hours"
                )

                st.write(
                    f"Latest recorded weight: "
                    f"{df.iloc[0]['weight']:.1f} kg"
                )

            else:

                st.info(
                    "Try asking about steps, sleep, "
                    "weight, or health summary."
                )

            st.caption(
                "These insights summarize recorded data "
                "and are not medical advice."
            )

# -------------------------------
# 8. CLOSE DATABASE
# -------------------------------

conn.close()