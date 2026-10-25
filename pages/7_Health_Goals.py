import streamlit as st
import sqlite3
import pandas as pd

st.set_page_config(
    page_title="Health Goals",
    page_icon="🎯",
    layout="wide"
)

st.title("🎯 Health Goals & Progress")
st.write("Set simple wellness goals and track your progress.")

# -----------------------------
# Load health data
# -----------------------------

try:
    conn = sqlite3.connect("health_data.db")

    query = """
    SELECT date, weight, steps, sleep
    FROM health_data
    ORDER BY date ASC
    """

    df = pd.read_sql_query(query, conn)
    conn.close()

except Exception as e:
    st.error(f"Database error: {str(e)}")
    df = pd.DataFrame()


# -----------------------------
# Goal Settings
# -----------------------------

st.subheader("⚙️ Set Your Goals")

col1, col2, col3 = st.columns(3)

with col1:
    steps_goal = st.number_input(
        "Daily Steps Goal",
        min_value=100,
        value=5000,
        step=500
    )

with col2:
    sleep_goal = st.number_input(
        "Sleep Goal (hours)",
        min_value=1.0,
        max_value=24.0,
        value=7.0,
        step=0.5
    )

with col3:
    weight_goal = st.number_input(
        "Weight Tracking Value (kg)",
        min_value=1.0,
        value=40.0,
        step=0.1
    )


# -----------------------------
# Progress
# -----------------------------

if df.empty:

    st.info(
        "No health data available yet. "
        "Please add health data from the Health Data page."
    )

else:

    latest = df.iloc[-1]

    st.subheader("📊 Current Progress")

    col1, col2, col3 = st.columns(3)

    # Steps progress
    with col1:
        current_steps = float(latest["steps"])
        steps_progress = min(current_steps / steps_goal, 1.0)

        st.metric(
            "Steps",
            f"{int(current_steps)}",
            f"Goal: {int(steps_goal)}"
        )

        st.progress(steps_progress)

    # Sleep progress
    with col2:
        current_sleep = float(latest["sleep"])
        sleep_progress = min(current_sleep / sleep_goal, 1.0)

        st.metric(
            "Sleep",
            f"{current_sleep:.1f} hrs",
            f"Goal: {sleep_goal:.1f} hrs"
        )

        st.progress(sleep_progress)

    # Weight
    with col3:
        current_weight = float(latest["weight"])

        st.metric(
            "Latest Weight",
            f"{current_weight:.1f} kg"
        )

        st.write(
            f"Tracking value: {weight_goal:.1f} kg"
        )


# -----------------------------
# Historical Progress
# -----------------------------

if not df.empty:

    st.subheader("📈 Progress History")

    st.dataframe(
        df,
        use_container_width=True
    )

    st.subheader("📊 Steps Progress")

    if "steps" in df.columns:
        chart_data = df.set_index("date")[["steps"]]
        st.line_chart(chart_data)

    st.subheader("😴 Sleep Progress")

    if "sleep" in df.columns:
        sleep_data = df.set_index("date")[["sleep"]]
        st.line_chart(sleep_data)


# -----------------------------
# Goal Status
# -----------------------------

if not df.empty:

    st.subheader("✅ Goal Status")

    latest_steps = float(df.iloc[-1]["steps"])
    latest_sleep = float(df.iloc[-1]["sleep"])

    if latest_steps >= steps_goal:
        st.success("🎉 Daily steps goal reached!")
    else:
        remaining = int(steps_goal - latest_steps)
        st.info(f"🚶 {remaining} more steps to reach today's goal.")

    if latest_sleep >= sleep_goal:
        st.success("😴 Sleep goal reached!")
    else:
        remaining_sleep = sleep_goal - latest_sleep
        st.info(
            f"😴 {remaining_sleep:.1f} more hours needed to reach the selected goal."
        )

st.caption(
    "This feature is for general wellness tracking only and is not medical advice."
)