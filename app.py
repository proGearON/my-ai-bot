import streamlit as st
from groq import Groq

st.set_page_config(page_title="My AI Assistant", page_icon="🤖")
st.title("🤖 My Personal AI")

# Get Groq API key from Secrets or Sidebar
api_key = st.secrets.get("GROQ_API_KEY", "")

with st.sidebar:
    if not api_key:
        api_key = st.text_input("Enter your Groq API Key:", type="password")
    
    # Model selector with active Groq models
    selected_model = st.selectbox(
        "Choose AI Model:",
        ["openai/gpt-oss-120b", "qwen/qwen3.8-27b", "openai/gpt-oss-20b"]
    )

if not api_key:
    st.info("👈 Please paste your Groq API Key in the sidebar to start chatting.")
else:
    client = Groq(api_key=api_key)

    # Initialize chat history
    if "messages" not in st.session_state:
        st.session_state.messages = [
            {"role": "system", "content": "You are my dedicated, intelligent personal AI assistant."}
        ]

    # Show chat messages
    for msg in st.session_state.messages:
        if msg["role"] != "system":
            with st.chat_message(msg["role"]):
                st.write(msg["content"])

    # Chat input
    if prompt := st.chat_input("Ask anything..."):
        st.session_state.messages.append({"role": "user", "content": prompt})
        with st.chat_message("user"):
            st.write(prompt)

        try:
            response = client.chat.completions.create(
                model=selected_model,
                messages=st.session_state.messages,
            )
            reply = response.choices[0].message.content
            st.session_state.messages.append({"role": "assistant", "content": reply})
            with st.chat_message("assistant"):
                st.write(reply)
        except Exception as e:
            st.error(f"Error: {e}")
