import streamlit as st
from openai import OpenAI

# Initialize OpenAI client
client = OpenAI(api_key=st.secrets["OPENAI_API_KEY"])

def chat_ui():
    st.title("🤖 AI DBA Assistant")

    # Initialize chat history
    if "messages" not in st.session_state:
        st.session_state.messages = []

    # User input
    user_input = st.chat_input("Ask database question...")

    if user_input:
        # Save user message
        st.session_state.messages.append({"role": "user", "content": user_input})

        # Call OpenAI
        response = client.chat.completions.create(
    model="gpt-4o-mini",
    messages=[
        {
            "role": "system",
            "content": "You are an expert Oracle DBA assistant. Help with performance tuning, SQL optimization, indexing, waits, and troubleshooting."
        }
    ] + st.session_state.messages,
    temperature=0.3
)

        ai_reply = response.choices[0].message.content

        # Save AI response
        st.session_state.messages.append({"role": "assistant", "content": ai_reply})

    # Display chat
    for msg in st.session_state.messages:
        st.chat_message(msg["role"]).write(msg["content"])