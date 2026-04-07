import streamlit as st
import random

# =========================
# OTP GENERATOR
# =========================
def generate_otp():
    return str(random.randint(100000, 999999))


# =========================
# LOGIN
# =========================
def login():
    st.title("🔐 Login")

    email = st.text_input("Email")
    password = st.text_input("Password", type="password")

    if st.button("Login"):
        if email and password:
            st.session_state.logged_in = True
            st.session_state.email = email
            st.success("✅ Login successful")
            st.rerun()
        else:
            st.error("Enter credentials")


# =========================
# SIGNUP + OTP
# =========================
def signup():
    st.title("📝 Signup")

    email = st.text_input("Email")
    password = st.text_input("Password", type="password")

    if st.button("Send OTP"):
        if email:
            otp = generate_otp()
            st.session_state.otp = otp
            st.session_state.temp_email = email
            st.session_state.temp_pass = password
            st.session_state.show_otp = True

            # 👉 Simulated email (console)
            st.success(f"OTP sent: {otp}")

# =========================
# VERIFY OTP
# =========================
def verify_otp():
    st.title("🔐 Verify OTP")

    user_otp = st.text_input("Enter OTP")

    if st.button("Verify"):
        if user_otp == st.session_state.get("otp"):
            st.success("✅ Account created!")

            st.session_state.logged_in = True
            st.session_state.email = st.session_state.temp_email
            st.session_state.show_otp = False

            st.rerun()
        else:
            st.error("❌ Invalid OTP")


# =========================
# RESET PASSWORD REQUEST
# =========================
def reset_password_request():
    st.title("🔁 Reset Password")

    email = st.text_input("Email")

    if st.button("Send Reset OTP"):
        otp = generate_otp()
        st.session_state.reset_otp_val = otp
        st.session_state.reset_email = email
        st.session_state.reset_otp = True

        st.success(f"Reset OTP: {otp}")


# =========================
# RESET PASSWORD CONFIRM
# =========================
def reset_password_confirm():
    st.title("🔁 Enter OTP & New Password")

    otp = st.text_input("OTP")
    new_pass = st.text_input("New Password", type="password")

    if st.button("Reset Password"):
        if otp == st.session_state.get("reset_otp_val"):
            st.success("✅ Password reset successful")

            st.session_state.reset_otp = False
        else:
            st.error("❌ Invalid OTP")