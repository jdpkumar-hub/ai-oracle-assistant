import streamlit as st

def login():
    st.subheader("🔐 Login")

    email = st.text_input("Email")
    password = st.text_input("Password", type="password")

    if st.button("Login"):
        if email and password:
            st.session_state.logged_in = True
            st.session_state.email = email

            st.success("✅ Login successful")
            st.rerun()
        else:
            st.error("❌ Enter email & password")


def signup():
    st.subheader("📝 Signup")

    email = st.text_input("Email")
    password = st.text_input("Password", type="password")

    if st.button("Create Account"):
        if email and password:
            st.success("✅ Account created. Please login.")
        else:
            st.error("❌ Fill all fields")