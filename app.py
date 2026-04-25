import streamlit as st
from auth import login, signup, reset_password, logout, get_user, supabase
from openai import OpenAI
import pandas as pd
from datetime import datetime

# ===============================
# 🔐 OAUTH CALLBACK
# ===============================
params = st.query_params
if "code" in params:
    try:
        supabase.auth.exchange_code_for_session({
            "auth_code": params["code"]
        })
        st.query_params.clear()
        st.rerun()
    except Exception as e:
        st.error(f"Login failed: {e}")

# ===============================
# SESSION INIT
# ===============================
if "user" not in st.session_state:
    st.session_state.user = None

if "messages" not in st.session_state:
    st.session_state.messages = []

if "usage" not in st.session_state:
    st.session_state.usage = 0

# ===============================
# OPENAI
# ===============================
if "OPENAI_API_KEY" not in st.secrets:
    st.error("Missing OPENAI_API_KEY")
    st.stop()

client = OpenAI(api_key=st.secrets["OPENAI_API_KEY"])

# ===============================
# SYSTEM PROMPT
# ===============================
SYSTEM_PROMPT = """
You are a Senior Oracle DBA with 20+ years experience.

Always provide:
- Root Cause
- Diagnostic Queries
- Fix Steps
- Risks
- Best Practices
"""

# ===============================
# PAGE CONFIG
# ===============================
st.set_page_config(page_title="AI DBA Assistant", layout="wide")

# ===============================
# USER SESSION
# ===============================
user = get_user()
if user:
    st.session_state.user = user

user = st.session_state.user

# ===============================
# LOGIN UI
# ===============================
if not user:
    col1, col2 = st.columns([1, 2])

    with col1:
        st.image("image/logo2.png", width=220)
        st.markdown("## AI DBA Assistant")
        st.caption("🚀 Smart Oracle Optimization")

        st.markdown("""
        ⚡ SQL Tuning  
        📊 AWR Analysis  
        🤖 AI Insights  
        🚀 Performance Fixes  
        """)

    with col2:
        tab1, tab2, tab3 = st.tabs(["Login", "Signup", "Reset"])
        with tab1: login()
        with tab2: signup()
        with tab3: reset_password()

    st.stop()

# ===============================
# SIDEBAR
# ===============================
with st.sidebar:
    st.image("image/logo2.png", width=200)
    page = st.radio("", ["Dashboard", "AI Chat", "History"])
    st.success(user.email)
    logout()

# ===============================
# DASHBOARD
# ===============================
if page == "Dashboard":
    st.title("📊 Dashboard")

    data = supabase.table("query_history")\
        .select("*")\
        .eq("user_email", user.email)\
        .execute()

    df = pd.DataFrame(data.data)

    if not df.empty:
        st.metric("Total Queries", len(df))
        df["created_at"] = pd.to_datetime(df["created_at"])
        st.line_chart(df.groupby(df["created_at"].dt.date).size())

# ===============================
# AI CHAT (FULL FEATURE)
# ===============================
elif page == "AI Chat":

    st.title("🤖 AI DBA Assistant")

    tab1, tab2, tab3 = st.tabs(["💬 Chat", "⚡ SQL Analyzer", "📊 AWR Analyzer"])

    # ================= CHAT =================
    with tab1:

        # Quick buttons
        col1, col2, col3, col4 = st.columns(4)

        if col1.button("🐢 Slow Query"):
            st.session_state.messages.append({"role": "user", "content": "Why is my Oracle query slow?"})

        if col2.button("🔥 High CPU"):
            st.session_state.messages.append({"role": "user", "content": "Oracle high CPU troubleshooting steps"})

        if col3.button("💾 Tablespace Full"):
            st.session_state.messages.append({"role": "user", "content": "Tablespace full issue fix"})

        if col4.button("🔒 Lock Issue"):
            st.session_state.messages.append({"role": "user", "content": "Oracle locking issue troubleshooting"})

        st.divider()

        # Show chat history
        for msg in st.session_state.messages:
            with st.chat_message(msg["role"]):
                st.markdown(msg["content"])

        # Input box
        user_input = st.chat_input("Ask your DBA question...")

        if user_input:
            st.session_state.messages.append({"role": "user", "content": user_input})

            with st.chat_message("user"):
                st.markdown(user_input)

            # Usage limit
            if st.session_state.usage >= 20:
                st.warning("🚫 Free limit reached")
                st.stop()

            st.session_state.usage += 1

            # AI response
            with st.chat_message("assistant"):
                with st.spinner("Analyzing..."):
                    response = client.chat.completions.create(
                        model="gpt-4o-mini",
                        messages=[
                            {"role": "system", "content": SYSTEM_PROMPT},
                            *st.session_state.messages
                        ]
                    )

                    answer = response.choices[0].message.content
                    st.markdown(answer)

            st.session_state.messages.append({"role": "assistant", "content": answer})

    # ================= SQL ANALYZER =================
    with tab2:

        st.subheader("⚡ SQL Performance Analyzer")

        sql = st.text_area("Paste your SQL query")

        if st.button("🚀 Analyze SQL"):
            if sql:
                if st.session_state.usage >= 20:
                    st.warning("🚫 Free limit reached")
                    st.stop()

                st.session_state.usage += 1

                with st.spinner("Analyzing SQL..."):
                    response = client.chat.completions.create(
                        model="gpt-4o-mini",
                        messages=[
                            {"role": "system", "content": SYSTEM_PROMPT},
                            {"role": "user", "content": f"""
Analyze this Oracle SQL:

{sql}

Provide:
- Issues
- Execution Plan Advice
- Index Suggestions
- Optimized Query
"""}
                        ]
                    )

                    st.success("Analysis Complete")
                    st.write(response.choices[0].message.content)

    # ================= AWR ANALYZER =================
    with tab3:

        st.subheader("📊 AWR Report Analyzer")

        file = st.file_uploader("Upload AWR report (.txt)", type=["txt"])

        if file:
            content = file.read().decode()[:15000]

            if st.button("🚀 Analyze AWR"):
                if st.session_state.usage >= 20:
                    st.warning("🚫 Free limit reached")
                    st.stop()

                st.session_state.usage += 1

                with st.spinner("Analyzing AWR..."):
                    response = client.chat.completions.create(
                        model="gpt-4o-mini",
                        messages=[
                            {"role": "system", "content": SYSTEM_PROMPT},
                            {"role": "user", "content": f"""
Analyze this Oracle AWR report:

{content}

Provide:
- Top Bottlenecks
- Wait Events
- CPU vs IO Issues
- Recommendations
"""}
                        ]
                    )

                    st.success("AWR Analysis Complete")
                    st.write(response.choices[0].message.content)

# ===============================
# HISTORY
# ===============================
elif page == "History":
    st.title("📜 History")

    data = supabase.table("query_history")\
        .select("*")\
        .eq("user_email", user.email)\
        .execute()

    df = pd.DataFrame(data.data)

    if not df.empty:
        st.dataframe(df)

# ===============================
# FOOTER
# ===============================
st.markdown("---")
st.caption("🚀 AI DBA Assistant | ChatGPT + Analyzer Mode")