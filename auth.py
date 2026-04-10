import streamlit as st

# ============================
# 🔐 LOGIN PAGE
# ============================
def login(supabase):

    st.title("🔐 Login")

    # ----------------------------
    # 🔵 GOOGLE LOGIN BUTTON
    # ----------------------------
    st.markdown("### Continue with Google")

    st.markdown(
        """
        <a href="https://ai-auth-frontend-nine.vercel.app" target="_self">
            <button style="
                width: 100%;
                padding: 12px;
                background-color: white;
                border: 1px solid #ddd;
                border-radius: 8px;
                font-size: 16px;
                cursor: pointer;">
                🔵 Continue with Google
            </button>
        </a>
        """,
        unsafe_allow_html=True
    )

    st.markdown("---")

    # ----------------------------
    # 📧 EMAIL LOGIN
    # ----------------------------
    st.markdown("### Or login with Email")

    email = st.text_input("Email", key="login_email")
    password = st.text_input("Password", type="password", key="login_password")

    if st.button("Login"):
        try:
            result = supabase.table("users").select("*").eq("email", email).execute()

            if result.data:
                stored_password = result.data[0]["password"]

                if verify_password(password, stored_password):
                    st.session_state.logged_in = True
                    st.session_state.username = email
                    st.success("Login successful ✅")
                    st.rerun()
                else:
                    st.error("Wrong password ❌")
            else:
                st.error("User not found ❌")

        except Exception as e:
            st.error(f"Error: {e}")


# ============================
# 🔑 PASSWORD VERIFY FUNCTION
# ============================
def verify_password(input_password, stored_password):
    # Simple compare (you can upgrade to hashing later)
    return input_password == stored_password