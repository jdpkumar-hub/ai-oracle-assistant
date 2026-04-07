import streamlit as st
import pandas as pd

# =========================
# AI SQL ANALYZER (SIMPLE LOGIC)
# =========================
def analyze_query(query):
    suggestions = []

    if "select *" in query.lower():
        suggestions.append("❌ Avoid SELECT * → Use specific columns")

    if "where" not in query.lower():
        suggestions.append("⚠️ Add WHERE clause to limit data")

    if "join" in query.lower():
        suggestions.append("💡 Ensure indexed columns are used in JOIN")

    if not suggestions:
        suggestions.append("✅ Query looks optimized!")

    return suggestions


def analyze_page():
    st.title("🔍 Analyze SQL")
    st.success("🎉 All features are FREE during beta launch!")

    # =========================
    # FILE UPLOAD
    # =========================
    st.subheader("📂 Upload File")

    uploaded_file = st.file_uploader(
        "Upload SQL / CSV / TXT / PDF",
        type=["sql", "txt", "csv", "pdf"]
    )

    query = ""

    if uploaded_file:
        file_type = uploaded_file.name.split(".")[-1]

        if file_type == "pdf":
            import PyPDF2
            pdf_reader = PyPDF2.PdfReader(uploaded_file)
            content = ""
            for page in pdf_reader.pages:
                content += page.extract_text()

        elif file_type == "csv":
            df = pd.read_csv(uploaded_file)
            st.dataframe(df)
            content = df.to_string()

        else:
            content = uploaded_file.read().decode("utf-8")

        st.success("✅ File uploaded!")
        st.text_area("📄 File Content", content, height=200)

        query = content

    # =========================
    # MANUAL INPUT
    # =========================
    st.subheader("✍️ Enter Query")

    user_input = st.text_area("Enter SQL query")

    if user_input:
        query = user_input

    # =========================
    # ANALYZE
    # =========================
    if st.button("🚀 Analyze"):
        if query:
            st.info("🔍 Analyzing...")

            results = analyze_query(query)

            st.subheader("📊 Results")
            for r in results:
                st.write(r)

            # SAVE HISTORY
            st.session_state.history.append({
                "query": query,
                "result": results
            })

        else:
            st.warning("⚠️ Enter or upload query")