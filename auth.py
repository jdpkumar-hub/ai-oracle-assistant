import streamlit as st
from utils import is_strong_password, hash_password, verify_password

def signup(supabase):
    st.title("📝 Sign Up")

    new_user = st.text_input("Username")
    new_pass = st.text_input("Password", type="password")

    if st.button("Create Account"):

        if not new_user or not new_pass:
            st.warning("Please fill all fields")
            return

        if not is_strong_password(new_pass):
            st.warning("Weak password")
            return

        result = supabase.table("users").select("*").eq("username", new_user).execute()

        if result.data:
            st.warning("User exists")
            return

        hashed = hash_password(new_pass)

        supabase.table("users").insert({
            "username": new_user,
            "password": hashed
        }).execute()

        st.session_state.logged_in = True
        st.session_state.username = new_user
        st.rerun()


def login(supabase):
    st.title("🔐 Login")

    username = st.text_input("Username")
    password = st.text_input("Password", type="password")

    if st.button("Login"):

        result = supabase.table("users").select("*").eq("username", username).execute()

        if result.data:
            stored_password = result.data[0]["password"]

            if verify_password(password, stored_password):
                st.session_state.logged_in = True
                st.session_state.username = username
                st.rerun()
            else:
                st.error("Wrong password")
        else:
            st.error("User not found")