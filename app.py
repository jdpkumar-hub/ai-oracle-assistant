import streamlit as st
from openai import OpenAI
import oracledb

# 🔑 Add your API key here
client = OpenAI(api_key=st.secrets["OPENAI_API_KEY"])


# 🧠 Initialize history
if "history" not in st.session_state:
    st.session_state.history = []

# ⚙️ Oracle DB Connection
def get_connection():
    return oracledb.connect(
        user="system",
        password="Pa33word#1234!",
        dsn="JDPKUMAR:1521/FREE"
    )

# 🎨 Page config
st.set_page_config(page_title="AI DBA Assistant", layout="wide")

# 🚀 Title
st.title("🚀 AI Oracle Performance Assistant")

# 📌 Layout
col1, col2 = st.columns(2)

with col1:
    task = st.selectbox(
        "Select Task",
        ["Query Optimization", "Error Debugging", "Explain SQL", "Performance Issue"]
    )

with col2:
    st.markdown("### 💡 Tips")
    st.write("Paste SQL or describe your issue clearly")

# 📝 User input
user_input = st.text_area("Enter your query or issue:")

# ▶️ Run SQL on Database
if st.button("Run SQL on DB"):
    if user_input:
        try:
            conn = get_connection()
            cursor = conn.cursor()

            cursor.execute(user_input)
            rows = cursor.fetchall()

            st.subheader("📊 Query Results")
            for row in rows:
                st.write(row)

            cursor.close()
            conn.close()

        except Exception as e:
            st.error("❌ DB Error")
            st.write(str(e))
    else:
        st.warning("Please enter SQL query")

# 🤖 Analyze with AI
if st.button("Analyze"):
    if user_input:

        if task == "Query Optimization":
            prompt = f"""
            You are an expert Oracle DBA.

            Optimize this SQL query for performance.
            Provide:
            1. Optimized query
            2. Explanation
            3. Index suggestions

            SQL:
            {user_input}
            """
        else:
            prompt = f"""
            You are an expert Oracle DBA.

            Task: {task}
            User Input: {user_input}

            Provide clear and practical solution.
            """

        try:
            with st.spinner("Analyzing..."):
                response = client.chat.completions.create(
                    model="gpt-4.1-mini",
                    messages=[{"role": "user", "content": prompt}]
                )

                ai_reply = response.choices[0].message.content

                # 💾 Save history
                st.session_state.history.append(("User", user_input))
                st.session_state.history.append(("AI", ai_reply))

        except Exception as e:
            st.error("⚠️ API Error")
            st.write(str(e))
    else:
        st.warning("Please enter input")

# 🧹 Clear history
if st.button("Clear History"):
    st.session_state.history = []

# 📜 Show history
st.subheader("💬 Conversation History")

for role, msg in st.session_state.history:
    if role == "User":
        st.markdown(f"**🧑‍💻 You:** {msg}")
    else:
        st.markdown(f"**🤖 AI:** {msg}")