import streamlit as st
from supabase_client import supabase

# =========================
# GOOGLE LOGIN
# =========================
def google_login():
    res = supabase.auth.sign_in_with_oauth({
        "provider": "google",
        "options": {
            "redirect_to": "https://ai-oracle-assistant.streamlit.app"
        }
    })

    return res.url


# =========================
# SESSION HANDLER
# =========================
def handle_session():
    session = supabase.auth.get_session()

    if session and session.session:
        st.session_state["user"] = session.session.user
        st.session_state["logged_in"] = True
        return True

    return False


# =========================
# LOGIN UI
# =========================
def login():

    st.markdown("## 🔐 Login")

    if "logged_in" not in st.session_state:
        st.session_state["logged_in"] = False

    # Already logged in
    if handle_session():
        st.success("✅ Logged in")
        return

    # Login button
    if st.button("🔵 Continue with Google"):
        url = google_login()
        st.markdown(f"[👉 Click to Login]({url})")


# =========================
# REQUIRE LOGIN
# =========================
def require_login():
    if not st.session_state.get("logged_in"):
        login()
        st.stop()


# =========================
# LOGOUT
# =========================
def logout():
    supabase.auth.sign_out()
    st.session_state.clear()
    st.rerun()


# =========================
# USER SIDEBAR
# =========================
def show_user():
    if "user" in st.session_state:
        st.sidebar.success(f"👤 {st.session_state['user'].email}")

        if st.sidebar.button("Logout"):
            logout()