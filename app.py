import streamlit as st
from auth import login, logout, get_user, supabase
import os
from openai import OpenAI

client = OpenAI(api_key=os.getenv("OPENAI_API_KEY"))

st.set_page_config(page_title="AI DBA Assistant", page_icon="🤖", layout="wide")

# -------------------------------
# STYLE
# -------------------------------
st.markdown("""
<style>
.block-container { padding-top: 1rem; }

.card {
    background-color: white;
    padding: 25px;
    border-radius: 20px;
    box-shadow: 0px 8px 24px rgba(0,0,0,0.08);
}

.feature {
    padding: 12px;
    border-radius: 12px;
    transition: 0.3s;
}
.feature:hover {
    background-color: #f5f7ff;
}
</style>
""", unsafe_allow_html=True)

# -------------------------------
# AUTH
# -------------------------------
params = st.query_params
if "code" in params:
    supabase.auth.exchange_code_for_session({"auth_code": params["code"]})
    st.query_params.clear()
    st.rerun()

user = get_user()

# -------------------------------
# LOGIN
# -------------------------------
if not user:
    col1, col2 = st.columns([1, 3])

    with col1:
        st.image("logo2.png", width=200)
        st.markdown("## AI DBA Assistant")

    with col2:
        tab1, tab2 = st.tabs(["Login", "Signup"])

        with tab1:
            login()

        with tab2:
            email = st.text_input("Email")
            password = st.text_input("Password", type="password")

            if st.button("Create"):
                supabase.auth.sign_up({"email": email, "password": password})

    st.stop()

# -------------------------------
# SIDEBAR
# -------------------------------
with st.sidebar:
    page = st.radio("", ["🏠 Dashboard", "💬 AI Chat", "📊 Reports", "⚙️ Settings"])
    st.success(user.email)
    logout()

# -------------------------------
# PAGES
# -------------------------------
if page == "🏠 Dashboard":
    st.title("Dashboard")

elif page == "💬 AI Chat":
    st.title("AI DBA Assistant")

    tab1, tab2, tab3 = st.tabs(["💬 Chat", "⚡ SQL", "📊 AWR"])

    # CHAT
    with tab1:
        q = st.text_input("Ask question")

        if q:
            res = client.chat.completions.create(
                model="gpt-4o-mini",
                messages=[{"role": "user", "content": q}]
            )
            st.write(res.choices[0].message.content)

    # SQL
    with tab2:
        sql = st.text_area("SQL")

        if st.button("Analyze SQL"):
            res = client.chat.completions.create(
                model="gpt-4o-mini",
                messages=[{"role": "user", "content": sql}]
            )
            st.write(res.choices[0].message.content)

    # ✅ AWR (FIXED POSITION)
    with tab3:
        file = st.file_uploader("Upload AWR", type=["txt"])

        if file:
            content = file.read().decode("utf-8")[:15000]

            if st.button("Analyze AWR"):
                res = client.chat.completions.create(
                    model="gpt-4o-mini",
                    messages=[{"role": "user", "content": content}]
                )
                st.write(res.choices[0].message.content)

# -------------------------------
elif page == "📊 Reports":
    st.title("Reports")

elif page == "⚙️ Settings":
    st.title("Settings")