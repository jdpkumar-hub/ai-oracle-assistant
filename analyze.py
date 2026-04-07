import streamlit as st
import pandas as pd
import PyPDF2

def analyze_query(query):
    results = []

    if "select *" in query.lower():
        results.append("❌ Avoid SELECT *")

    if "where" not in query.lower():
        results.append("⚠️ Add WHERE clause")

    if not results:
        results.append("✅ Query optimized")

    return results


def analyze_page():
    st.title("🔍 Analyze SQL")

    # FILE UPLOAD
    file = st.file_uploader("Upload SQL/CSV/PDF", type=["sql", "txt", "csv", "pdf"])

    query = ""

    if file:
        if file.name.endswith("pdf"):
            reader = PyPDF2.PdfReader