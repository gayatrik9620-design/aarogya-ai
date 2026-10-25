import streamlit as st
import pandas as pd
import sqlite3
import json
import os

st.set_page_config(
    page_title="Import Health Data",
    page_icon="📂",
    layout="wide"
)

st.title("📂 Import Health Data")
st.write("Upload and preview your health data in CSV or JSON format.")

# File uploader
uploaded_file = st.file_uploader(
    "Choose a CSV or JSON file",
    type=["csv", "json"]
)

if uploaded_file is not None:

    try:
        # Read CSV file
        if uploaded_file.name.lower().endswith(".csv"):
            df = pd.read_csv(uploaded_file)

        # Read JSON file
        elif uploaded_file.name.lower().endswith(".json"):
            df = pd.read_json(uploaded_file)

        # Show success message
        st.success("File uploaded successfully!")

        # Show file information
        st.subheader("📄 File Information")

        col1, col2, col3 = st.columns(3)

        with col1:
            st.metric("File Name", uploaded_file.name)

        with col2:
            st.metric("Rows", len(df))

        with col3:
            st.metric("Columns", len(df.columns))

        # Preview data
        st.subheader("📊 Health Data Preview")

        st.dataframe(
            df,
            use_container_width=True
        )

        # Basic statistics
        st.subheader("📈 Basic Statistics")

        numeric_columns = df.select_dtypes(
            include=["number"]
        ).columns

        if len(numeric_columns) > 0:
            st.dataframe(
                df[numeric_columns].describe(),
                use_container_width=True
            )
        else:
            st.info("No numerical health data found.")

        # Download converted CSV
        st.subheader("💾 Download Data")

        csv_data = df.to_csv(index=False)

        st.download_button(
            label="⬇️ Download as CSV",
            data=csv_data,
            file_name="health_data_export.csv",
            mime="text/csv"
        )

    except Exception as e:
        st.error(f"Error while reading file: {str(e)}")

else:
    st.info("Please upload a CSV or JSON health data file.")

    st.write("### Example CSV format")

    example_data = pd.DataFrame({
        "date": ["2026-10-25", "2026-10-26"],
        "weight": [40, 40.2],
        "steps": [5000, 6500],
        "sleep": [7, 7.5]
    })

    st.dataframe(
        example_data,
        use_container_width=True
    )