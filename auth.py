import streamlit as st
from supabase_client import supabase

# ================================
# 🔐 GOOGLE LOGIN FUNCTION
# ================================
def google_login():
    try:
        res = supabase.auth.sign_in_with_oauth({
            "provider": "google",
            "options": {
                "redirect_to": "https://ai-oracle-assistant.streamlit.app"
            }
        })

        # 🧪 DEBUG (IMPORTANT)
        st.write("🔍 OAuth Response:", res)

        # ✅ Handle all cases
        if hasattr(res, "url"):
            return res.url

        elif isinstance(res, dict) and "url" in res:
            return res["url"]

        else:
            st.error("❌ OAuth URL not found in response")
            return None

    except Exception as e:
        st.error(f"❌ Google Login Error: {e}")
        return None


# ================================
# 🔐 HANDLE LOGIN SESSION
# ================================
def handle_session():
    try:
        session = supabase.auth.get_session()

        if session and session.session:
            user = session.session.user

            st.session_state["user"] = user
            st.session_state["logged_in"] = True

            return True

        return False

    except Exception as e:
        st.error(f"Session Error: {e}")
        return False


# ================================
# 🔐 LOGOUT
# ================================
def logout():
    try:
        supabase.auth.sign_out()
        st.session_state.clear()
        st.rerun()
    except Exception as e:
        st.error(f"Logout Error: {e}")


# ================================
# 🎯 MAIN LOGIN UI (PRO UX)
# ================================
def login():

    st.markdown("## 🔐 Login")
    st.write("### Continue with Google")

    # 🧠 PRO UX TIP: Keep state
    if "logged_in" not in st.session_state:
        st.session_state["logged_in"] = False

    # ======================
    # 🔁 HANDLE RETURN LOGIN
    # ======================
    if handle_session():
        st.success("✅ You are logged in")
        return

    # ======================
    # 🔘 LOGIN BUTTON
    # ======================
    if st.button("🔵 Continue with Google"):

        with st.spinner("Redirecting to Google..."):
            url = google_login()

        if url:
            st.success("✅ Login URL generated")

            # 🧪 SHOW DEBUG URL
            st.write("🔗 OAuth URL:", url)

            # 🔥 PRO UX: Clickable link
            st.markdown(f"""
            ### 👉 Click below if auto redirect doesn't happen:
            [🚀 Continue to Google Login]({url})
            """, unsafe_allow_html=True)

        else:
            st.error("❌ Failed to generate login URL")

    # ======================
    # ℹ️ HELP MESSAGE
    # ======================
    st.info("Login using Google to access AI DBA Assistant")


# ================================
# 🔐 REQUIRE LOGIN (FOR OTHER PAGES)
# ================================
def require_login():
    if "logged_in" not in st.session_state or not st.session_state["logged_in"]:
        login()
        st.stop()


# ================================
# 👤 SHOW USER INFO (SIDEBAR)
# ================================
def show_user():
    if "user" in st.session_state:
        user = st.session_state["user"]

        st.sidebar.success(f"👤 {user.email}")

        if st.sidebar.button("Logout"):
            logout()