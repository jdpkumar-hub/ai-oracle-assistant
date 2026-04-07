import streamlit as st

def history_page():
    st.title("📜 Query History")

    history = st.session_state.get("history", [])

    if not history:
        st.info("No history yet")
        return

    for i, item in enumerate(reversed(history), 1):
        with st.expander(f"Query {i}"):
            st.code(item["query"], language="sql")

            st.subheader("Results")
            for r in item["result"]:
                st.write(r)