import streamlit as st

def handle_auth():
    params = st.query_params

    if "access_token" in params:
        st.session_state["logged_in"] = True
        st.session_state["access_token"] = params["access_token"]

        # Clean URL (PRO UX)
        st.query_params.clear()

        st.success("✅ Login successful")
        st.rerun()


def login():
    handle_auth()

    if st.session_state.get("logged_in"):
        return True

    st.title("🔐 Login")

    # Redirect to your Vercel app
    login_url = "https://ai-auth-frontend-nine.vercel.app"

    st.markdown(f"""
        <a href="{login_url}">
            <button style="
                padding:10px 20px;
                border-radius:8px;
                cursor:pointer;
            ">
                🔵 Continue with Google
            </button>
        </a>
    """, unsafe_allow_html=True)

    return False


def logout():
    st.session_state.clear()
    st.rerun()