import streamlit as st
from auth import login, signup, reset_password, logout, get_user, supabase
import os
from openai import OpenAI
import pandas as pd
from reportlab.platypus import SimpleDocTemplate, Paragraph, Spacer
from reportlab.lib.styles import getSampleStyleSheet
from io import BytesIO
import oracledb
import time

# -------------------------------
# CONFIG
# -------------------------------
st.set_page_config(page_title="AI DBA Assistant", page_icon="🤖", layout="wide")

# -------------------------------
# OPENAI
# -------------------------------
client = OpenAI(api_key=os.getenv("OPENAI_API_KEY"))

# -------------------------------
# ORACLE CONNECTION
# -------------------------------
@st.cache_resource
def get_connection():
    return oracledb.connect(
        user=st.secrets["ORACLE_USER"],
        password=st.secrets["ORACLE_PASSWORD"],
        dsn=st.secrets["ORACLE_DSN"]
    )

# -------------------------------
# SESSION INIT
# -------------------------------
if "user" not in st.session_state:
    st.session_state.user = None

# -------------------------------
# PDF GENERATOR
# -------------------------------
def create_pdf(text):
    buffer = BytesIO()
    doc = SimpleDocTemplate(buffer)
    styles = getSampleStyleSheet()
    story = []

    for line in text.split("\n"):
        if line.strip():
            story.append(Paragraph(line, styles["Normal"]))
            story.append(Spacer(1, 8))

    doc.build(story)
    buffer.seek(0)
    return buffer

# -------------------------------
# OAUTH HANDLER
# -------------------------------
params = st.query_params

if "code" in params:
    try:
        supabase.auth.exchange_code_for_session({
            "auth_code": params["code"]
        })
        st.query_params.clear()
        user = get_user()
        if user:
            st.session_state.user = user
            st.rerun()
    except Exception as e:
        st.error(f"Login failed: {e}")

# -------------------------------
# LOGIN PAGE
# -------------------------------
user = get_user()
if user:
    st.session_state.user = user

user = st.session_state.user

if not user:
    tab1, tab2, tab3 = st.tabs(["🔐 Login", "🆕 Signup", "🔑 Reset"])

    with tab1:
        login()
    with tab2:
        signup()
    with tab3:
        reset_password()

    st.stop()

# -------------------------------
# SIDEBAR
# -------------------------------
with st.sidebar:
    st.title("AI DBA Assistant")
    page = st.radio("", [
        "🏠 Dashboard",
        "💬 AI Chat",
        "📊 Performance Diagnostics",
        "📡 Live Monitoring",
        "📜 History",
        "⚙️ Settings"
    ])
    st.success(user.email)
    logout()

# ===============================
# DASHBOARD
# ===============================
if page == "🏠 Dashboard":
    st.title("📊 Dashboard")

# ===============================
# AI CHAT
# ===============================
elif page == "💬 AI Chat":
    st.title("💬 AI DBA Assistant")

    question = st.text_input("Ask anything...")

    if question:
        response = client.chat.completions.create(
            model="gpt-4o-mini",
            messages=[{"role": "user", "content": question}]
        )
        answer = response.choices[0].message.content
        st.write(answer)

        pdf = create_pdf(answer)
        st.download_button("Download PDF", pdf, "report.pdf")

# ===============================
# PERFORMANCE DIAGNOSTICS
# ===============================
elif page == "📊 Performance Diagnostics":
    st.title("📊 AI Performance Diagnostics")

    file = st.file_uploader("Upload AWR Report", type=["txt"])

    if file:
        content = file.read().decode("utf-8")

        if st.button("Analyze"):
            with st.spinner("Analyzing..."):
                response = client.chat.completions.create(
                    model="gpt-4o-mini",
                    messages=[{
                        "role": "user",
                        "content": f"Analyze this AWR report:\n{content[:15000]}"
                    }]
                )
                st.write(response.choices[0].message.content)

# ===============================
# LIVE MONITORING
# ===============================
elif page == "📡 Live Monitoring":

    st.title("📡 Real-Time Oracle Monitoring")

    # Refresh control
    refresh_rate = st.slider("Refresh Interval (sec)", 2, 10, 5)
    auto_refresh = st.checkbox("Enable Auto Refresh", value=True)

    try:
        conn = get_connection()
        cursor = conn.cursor()

        # CPU
        cursor.execute("""
            SELECT value 
            FROM v$sysmetric 
            WHERE metric_name = 'CPU Usage Per Sec'
            AND rownum = 1
        """)
        cpu = cursor.fetchone()[0]

        # Sessions
        cursor.execute("""
            SELECT COUNT(*) 
            FROM v$session 
            WHERE status = 'ACTIVE'
        """)
        sessions = cursor.fetchone()[0]

        # Wait events
        cursor.execute("""
            SELECT event, total_waits 
            FROM v$system_event
            ORDER BY total_waits DESC FETCH FIRST 5 ROWS ONLY
        """)
        waits = cursor.fetchall()

        # Top SQL
        cursor.execute("""
            SELECT sql_id, elapsed_time/1000000 seconds
            FROM v$sql
            ORDER BY elapsed_time DESC FETCH FIRST 5 ROWS ONLY
        """)
        top_sql = cursor.fetchall()

        col1, col2 = st.columns(2)
        col1.metric("CPU Usage", f"{round(cpu,2)}%")
        col2.metric("Active Sessions", sessions)

        st.divider()

        st.subheader("Top Wait Events")
        for event, count in waits:
            st.write(f"{event} → {count}")

        st.subheader("Top SQL by Time")
        for sql_id, sec in top_sql:
            st.write(f"{sql_id} → {round(sec,2)} sec")

    except Exception as e:
        st.error(f"Database Error: {e}")

    # Auto refresh
    if auto_refresh:
        time.sleep(refresh_rate)
        st.rerun()

# ===============================
# HISTORY
# ===============================
elif page == "📜 History":
    st.title("📜 History")

# ===============================
# SETTINGS
# ===============================
elif page == "⚙️ Settings":
    st.title("⚙️ Settings")

# -------------------------------
# FOOTER
# -------------------------------
st.markdown("---")
st.caption("© AI DBA Assistant 🚀")