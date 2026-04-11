import streamlit as st
from auth import login, logout

# -------------------------------
# ⚙️ PAGE CONFIG
# -------------------------------
st.set_page_config(
    page_title="AI DBA Assistant",
    page_icon="🤖",
    layout="wide"
)

# -------------------------------
# 🔐 AUTH CHECK
# -------------------------------
if not login():
    st.stop()

# -------------------------------
# 🎨 CUSTOM CSS (LOOK & FEEL)
# -------------------------------
st.markdown("""
<style>
.big-title {
    font-size: 42px;
    font-weight: bold;
}
.sub-text {
    font-size: 18px;
    color: gray;
}
.card {
    padding: 20px;
    border-radius: 12px;
    background-color: #f7f7f7;
    margin-bottom: 10px;
}
</style>
""", unsafe_allow_html=True)

# -------------------------------
# 🧭 SIDEBAR
# -------------------------------
with st.sidebar:
    st.image("https://cdn-icons-png.flaticon.com/512/4712/4712027.png", width=80)
    st.markdown("## AI DBA Assistant")
    st.caption("Smart Database Optimization Tool")

    st.divider()

    st.markdown("### 👤 User")
    st.success("Logged in")

    if st.button("🚪 Logout"):
        logout()

# -------------------------------
# 🏠 HERO SECTION
# -------------------------------
st.markdown('<div class="big-title">🚀 AI DBA Assistant</div>', unsafe_allow_html=True)
st.markdown('<div class="sub-text">Optimize, analyze, and tune your Oracle database with AI</div>', unsafe_allow_html=True)

st.divider()

# -------------------------------
# ⭐ FEATURES SECTION
# -------------------------------
col1, col2, col3 = st.columns(3)

with col1:
    st.markdown('<div class="card">⚡ <b>SQL Tuning</b><br>Identify slow queries instantly</div>', unsafe_allow_html=True)

with col2:
    st.markdown('<div class="card">📊 <b>Performance Insights</b><br>Analyze AWR & wait events</div>', unsafe_allow_html=True)

with col3:
    st.markdown('<div class="card">🤖 <b>AI Recommendations</b><br>Get smart tuning suggestions</div>', unsafe_allow_html=True)

st.divider()

# -------------------------------
# 💬 CHAT SECTION (DEMO STYLE)
# -------------------------------
st.markdown("### 💬 Ask your database question")

if "chat_history" not in st.session_state:
    st.session_state.chat_history = []

user_input = st.chat_input("Ask something like: Why is my query slow?")

if user_input:
    # Save user message
    st.session_state.chat_history.append(("user", user_input))

    # Demo AI response (for showcase)
    response = f"""
🔍 **Analysis Result**

Your query might be slow due to:
- Missing indexes
- High full table scans
- Outdated statistics

💡 **Recommendation**
- Create index on filtered columns
- Gather fresh stats
- Review execution plan
"""

    st.session_state.chat_history.append(("ai", response))

# -------------------------------
# 📜 DISPLAY CHAT
# -------------------------------
for role, msg in st.session_state.chat_history:
    if role == "user":
        st.chat_message("user").write(msg)
    else:
        st.chat_message("assistant").write(msg)