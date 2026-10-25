import streamlit as st
import sqlite3
import pandas as pd

st.set_page_config(
    page_title="Health Recommendations",
    page_icon="💡",
    layout="wide"
)

st.title("💡 Health Recommendations")

st.write(
    "Get basic wellness recommendations based on your stored health data."
)

st.divider()


# Connect to health database
try:
    conn = sqlite3.connect("health_data.db")

    df = pd.read_sql_query(
        "SELECT date, weight, steps, sleep FROM health_data ORDER BY date DESC",
        conn
    )

    conn.close()

except Exception as e:
    st.error("Unable to load health data.")
    st.stop()


# Check if data is available
if df.empty:

    st.info(
        "No health data found. Please add your health data first "
        "from the Health Data page."
    )

else:

    st.subheader("📊 Latest Health Data")

    latest = df.iloc[0]

    col1, col2, col3 = st.columns(3)

    with col1:
        st.metric(
            "Weight",
            f"{latest['weight']} kg"
        )

    with col2:
        st.metric(
            "Daily Steps",
            f"{int(latest['steps'])}"
        )

    with col3:
        st.metric(
            "Sleep",
            f"{latest['sleep']} hrs"
        )

    st.divider()

    st.subheader("💡 Personalized Wellness Suggestions")

    recommendations = []

    # Step recommendation
    if latest["steps"] < 3000:

        recommendations.append(
            "🚶 Your recorded activity is low. "
            "Try to gradually increase your daily physical activity."
        )

    elif latest["steps"] < 7000:

        recommendations.append(
            "🚶 Your activity level can be improved gradually. "
            "Try to add more walking during the day."
        )

    else:

        recommendations.append(
            "✅ Your recorded daily activity looks good. "
            "Continue maintaining regular physical activity."
        )


    # Sleep recommendation
    if latest["sleep"] < 6:

        recommendations.append(
            "😴 Your recorded sleep is low. "
            "Try to maintain a regular sleep schedule and get adequate rest."
        )

    elif latest["sleep"] < 7:

        recommendations.append(
            "😴 You may benefit from getting a little more sleep."
        )

    else:

        recommendations.append(
            "✅ Your recorded sleep duration looks reasonable."
        )


    # Weight information
    if latest["weight"] > 0:

        recommendations.append(
            "⚖️ Continue monitoring your weight regularly "
            "and focus on balanced nutrition rather than sudden changes."
        )


    # Display recommendations
    for recommendation in recommendations:

        st.info(recommendation)


    st.divider()

    st.subheader("📈 Health Data History")

    st.dataframe(
        df,
        use_container_width=True
    )


    st.divider()

    st.warning(
        "⚠️ These recommendations are general wellness suggestions "
        "and are not a medical diagnosis or treatment."
    )

    st.caption(
        "Disclaimer: Aarogya AI is an AI-based wellness assistant, "
        "not a doctor. Please consult a qualified healthcare professional "
        "for personal medical advice."
    )