import streamlit as st
from groq import Groq
from duckduckgo_search import DDGS

st.set_page_config(page_title="My Personal AI", page_icon="⚡", layout="wide")
st.title("⚡ My Personal AI")

# Sidebar - Complete Control in Your Hands
with st.sidebar:
    st.header("⚙️ Control Panel")
    api_key = st.secrets.get("GROQ_API_KEY", "")
    if not api_key:
        api_key = st.text_input("Groq API Key:", type="password")

    selected_model = st.selectbox(
        "AI Brain (Model):",
        ["openai/gpt-oss-120b", "qwen/qwen3.8-27b", "openai/gpt-oss-20b"]
    )

    enable_web = st.checkbox("🌐 Enable Live Web Search", value=False)

    temperature = st.slider("Creativity (Temperature):", 0.0, 1.0, 0.7, 0.1)

    system_instruction = st.text_area(
        "🧠 AI Persona & Rules:",
        value="You are my dedicated personal AI assistant. You are loyal, smart, concise, and always help me succeed.",
        height=120
    )

    if st.button("🗑️ Clear Chat History"):
        st.session_state.messages = []
        st.rerun()

def search_web(query):
    try:
        with DDGS() as ddgs:
            results = list(ddgs.text(query, max_results=3))
            if results:
                return "\n".join([f"- {r['title']}: {r['body']}" for r in results])
    except Exception:
        pass
    return ""

if not api_key:
    st.info("👈 Please enter your Groq API Key in the sidebar.")
else:
    client = Groq(api_key=api_key)

    if "messages" not in st.session_state:
        st.session_state.messages = []

    # Display past messages
    for msg in st.session_state.messages:
        with st.chat_message(msg["role"]):
            st.write(msg["content"])

    # Chat Input
    if prompt := st.chat_input("What would you like me to do?"):
        st.session_state.messages.append({"role": "user", "content": prompt})
        with st.chat_message("user"):
            st.write(prompt)

        # Build context
        full_system = system_instruction
        if enable_web:
            with st.spinner("Searching the web..."):
                web_info = search_web(prompt)
                if web_info:
                    full_system += f"\n\nLive Web Information:\n{web_info}"

        api_messages = [{"role": "system", "content": full_system}]
        for m in st.session_state.messages:
            api_messages.append({"role": m["role"], "content": m["content"]})

        try:
            with st.spinner("Thinking..."):
                response = client.chat.completions.create(
                    model=selected_model,
                    messages=api_messages,
                    temperature=temperature,
                )
                reply = response.choices[0].message.content
                st.session_state.messages.append({"role": "assistant", "content": reply})
                with st.chat_message("assistant"):
                    st.write(reply)
        except Exception as e:
            st.error(f"Error: {e}")
