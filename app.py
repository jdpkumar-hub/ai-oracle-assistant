import streamlit as st
from auth import login, signup
from analyze import analyze_page

# =========================
# SESSION INIT
# =========================
if "logged_in" not in st.session_state:
    st.session_state.logged_in = False

# =========================
# SIDEBAR
# =========================
st.sidebar.title("🤖 AI Oracle DBA Assistant")

# =========================
# NOT LOGGED IN
# =========================
if not st.session_state.logged_in:

    menu = st.sidebar.selectbox("Select", ["Login", "Signup"])

    if menu == "Login":
        login()
    else:
        signup()

# =========================
# LOGGED IN
# =========================
else:
    st.sidebar.success(f"👤 {st.session_state.email}")

    # 🚀 Upgrade Button (NO STRIPE)
    if st.sidebar.button("🚀 Upgrade to Pro"):
        st.warning("🚀 Premium features coming soon!")
        st.info("🎁 For now, ALL features are FREE!")

    menu = st.sidebar.radio("Menu", ["Analyze", "History"])

    if menu == "Analyze":
        analyze_page()

    elif menu == "History":
        st.title("📜 History")
        st.info("Coming soon...")

    if st.sidebar.button("Logout"):
        st.session_state.logged_in = False
        st.rerun()