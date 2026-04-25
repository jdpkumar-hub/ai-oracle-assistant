import streamlit as st
from auth import login, signup, reset_password, logout, get_user, supabase
from openai import OpenAI
import pandas as pd
from reportlab.platypus import SimpleDocTemplate, Paragraph, Spacer
from reportlab.lib.styles import getSampleStyleSheet
from io import BytesIO
from datetime import datetime

# ===============================
# 🔐 OAUTH CALLBACK FIX
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
You are a Senior Oracle DBA.

Provide:
- Root cause
- SQL fixes
- Performance tuning
- Best practices
"""

# ===============================
# PAGE CONFIG
# ===============================
st.set_page_config(layout="wide")

# ===============================
# STYLE
# ===============================
st.markdown("""
<style>
.card {
    background: white;
    padding: 25px;
    border-radius: 20px;
    box-shadow: 0 10px 25px rgba(0,0,0,0.1);
}
</style>
""", unsafe_allow_html=True)

# ===============================
# GET USER
# ===============================
user = get_user()
if user:
    st.session_state.user = user

user = st.session_state.user

# ===============================
# LOGIN UI (LEFT + RIGHT)
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
        st.markdown('<div class="card">', unsafe_allow_html=True)

        tab1, tab2, tab3 = st.tabs(["Login", "Signup", "Reset"])

        with tab1:
            login()
        with tab2:
            signup()
        with tab3:
            reset_password()

        st.markdown('</div>', unsafe_allow_html=True)

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
        st.line_chart(df)

# ===============================
# AI CHAT
# ===============================
elif page == "AI Chat":

    st.title("🤖 AI DBA Assistant")

    mode = st.selectbox("Mode", ["Chat", "SQL Analyzer", "AWR Analyzer"])

    def run_ai(prompt_text):
        if st.session_state.usage >= 20:
            st.warning("Limit reached")
            st.stop()

        st.session_state.usage += 1

        response = client.chat.completions.create(
            model="gpt-4o-mini",
            messages=[
                {"role": "system", "content": SYSTEM_PROMPT},
                {"role": "user", "content": prompt_text}
            ]
        )

        return response.choices[0].message.content

    if mode == "Chat":
        q = st.text_input("Ask DBA question")

        if q:
            ans = run_ai(q)
            st.write(ans)

    elif mode == "SQL Analyzer":
        sql = st.text_area("Paste SQL")

        if st.button("Analyze"):
            ans = run_ai(f"Analyze SQL:\n{sql}")
            st.write(ans)

    elif mode == "AWR Analyzer":
        file = st.file_uploader("Upload AWR", type=["txt"])

        if file:
            content = file.read().decode()[:15000]

            if st.button("Analyze AWR"):
                ans = run_ai(content)
                st.write(ans)

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
st.caption("🚀 AI DBA Assistant")