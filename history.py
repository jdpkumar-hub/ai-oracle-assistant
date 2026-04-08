import streamlit as st

def history_page():
    st.header("💬 History")

    for role, msg in st.session_state.history:
        st.write(role, ":", msg)