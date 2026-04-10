import streamlit as st
import pandas as pd

def dashboard():
    st.title("📊 AI DBA Dashboard")

    st.subheader("Database Overview")

    # Dummy data (replace with real DB later)
    data = {
        "Metric": ["CPU Usage", "Memory Usage", "Active Sessions"],
        "Value": [65, 72, 120]
    }

    df = pd.DataFrame(data)

    st.table(df)

    st.subheader("Performance Chart")
    st.line_chart(df.set_index("Metric"))