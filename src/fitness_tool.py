
import sqlite3
import pandas as pd


def get_fitness_summary():
    try:
        conn = sqlite3.connect("health_data.db")

        query = """
            SELECT date, weight, steps, sleep
            FROM health_data
            ORDER BY date DESC, id DESC
        """

        df = pd.read_sql_query(query, conn)
        conn.close()

        if df.empty:
            return "## Fitness Summary\n\nNo health records found."

        avg_steps = df["steps"].mean()
        avg_sleep = df["sleep"].mean()

        if df["weight"].notna().any():
            avg_weight = df["weight"].dropna().mean()
            weight_text = f"{avg_weight:.1f} kg"
        else:
            weight_text = "Not available"

        latest = df.iloc[0]

        latest_weight = (
            f"{latest['weight']} kg"
            if pd.notna(latest["weight"])
            else "Not available"
        )

        return f"""
## 🏥 Your Fitness Summary

### 📊 Health Statistics

- 🚶 **Average Steps:** {avg_steps:.0f} steps/day
- 😴 **Average Sleep:** {avg_sleep:.1f} hours/day
- ⚖️ **Average Recorded Weight:** {weight_text}
- 📋 **Total Records:** {len(df)}

### 📅 Latest Record

- **Date:** {latest['date']}
- **Steps:** {int(latest['steps'])}
- **Sleep:** {latest['sleep']} hours
- **Weight:** {latest_weight}

---
*This report summarizes recorded data and is not a medical diagnosis.*
"""

    except Exception as e:
        return f"Unable to generate fitness summary: {e}"
