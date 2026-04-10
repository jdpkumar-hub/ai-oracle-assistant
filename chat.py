import streamlit as st
from openai import OpenAI

# DEBUG check
if "OPENAI_API_KEY" not in st.secrets:
    st.error("❌ OpenAI API Key missing")
    st.stop()

client = OpenAI(api_key=st.secrets["OPENAI_API_KEY"])

st.title("🤖 AI DBA Assistant")

if "messages" not in st.session_state:
    st.session_state.messages = []

# Show history
for msg in st.session_state.messages:
    with st.chat_message(msg["role"]):
        st.write(msg["content"])

prompt = st.chat_input("Ask database question...")

if prompt:
    st.session_state.messages.append({"role": "user", "content": prompt})

    with st.chat_message("user"):
        st.write(prompt)

    try:
        with st.chat_message("assistant"):
            with st.spinner("Thinking..."):

                response = client.chat.completions.create(
                    model="gpt-4o-mini",
                    messages=[
                        {
                            "role": "system",
                            "content": "You are an Oracle DBA expert."
                        }
                    ] + st.session_state.messages
                )

                reply = response.choices[0].message.content
                st.write(reply)

        st.session_state.messages.append({"role": "assistant", "content": reply})

    except Exception as e:
        st.error(f"❌ Error: {str(e)}")