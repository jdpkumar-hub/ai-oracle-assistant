import streamlit as st
from utils import is_strong_password, hash_password, verify_password

# =========================
# 📝 SIGNUP
# =========================
def signup(supabase):
    st.title("📝 Sign Up")

    email = st.text_input("Email", key="signup_email")
    password = st.text_input("Password", type="password", key="signup_password")

    if st.button("Create Account", key="signup_btn"):

        # ✅ Empty check
        if not email or not password:
            st.warning("Please fill all fields")
            return

        # 🔐 Password validation
        if not is_strong_password(password):
            st.warning("Password must contain:\n- 6+ chars\n- 1 uppercase\n- 1 number")
            return

        try:
            # 🔍 Check if user exists
            result = supabase.table("users").select("*").eq("email", email).execute()

            if result.data:
                st.warning("⚠️ Email already registered")
                return

            # 🔒 Hash password
            hashed = hash_password(password)

            # 💾 Insert user
            supabase.table("users").insert({
                "email": email,
                "password": hashed
            }).execute()

            # ✅ Auto login
            st.session_state.logged_in = True
            st.session_state.username = email

            st.success("Account created & logged in ✅")
            st.rerun()

        except Exception as e:
            st.error("Signup failed ❌")
            st.write(e)


# =========================
# 🔐 LOGIN
# =========================
def login(supabase):
    st.title("🔐 Login")

    email = st.text_input("Email", key="login_email")
    password = st.text_input("Password", type="password", key="login_password")

    if st.button("Login", key="login_btn"):

        # ✅ Empty check
        if not email or not password:
            st.warning("Please enter email and password")
            return

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
            st.error("Login failed ❌")
            st.write(e)