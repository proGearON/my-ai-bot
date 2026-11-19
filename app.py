import streamlit as st
from groq import Groq

st.set_page_config(page_title="My AI Assistant", page_icon="🤖")
st.title("🤖 My Personal AI")

# Get Groq API key from Streamlit Secrets or sidebar input
api_key = st.secrets.get("GROQ_API_KEY", "")

if not api_key:
    with st.sidebar:
        api_key = st.text_input("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", type="password")

if not api_key:
    st.info("Please enter your Groq API Key in the sidebar or in Streamlit Secrets to begin chatting.")
else:
    client = Groq(api_key=api_key)

    # Initialize chat history with your custom personality
    if "messages" not in st.session_state:
        st.session_state.messages = [
            {"role": "system", "content": "You are a helpful, smart, and friendly personal AI assistant."}
        ]

    # Display past messages (excluding system prompt)
    for msg in st.session_state.messages:
        if msg["role"] != "system":
            with st.chat_message(msg["role"]):
                st.write(msg["content"])

    # Chat input box
    if prompt := st.chat_input("Ask anything..."):
        st.session_state.messages.append({"role": "user", "content": prompt})
        with st.chat_message("user"):
            st.write(prompt)

        try:
            response = client.chat.completions.create(
                model="llama-3.3-70b-versatile",
                messages=st.session_state.messages,
            )
            reply = response.choices[0].message.content
            st.session_state.messages.append({"role": "assistant", "content": reply})
            with st.chat_message("assistant"):
                st.write(reply)
        except Exception as e:
            st.error(f"Error: {e}")
