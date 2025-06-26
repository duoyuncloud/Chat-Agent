import streamlit as st
import requests
from datetime import datetime

# --- LLM 选项与介绍 ---
LLM_OPTIONS = {
    "Ollama": {
        "desc": "本地大模型，支持 llama2:latest 等，免API Key，适合本地推理和隐私场景。",
        "backend_url": "http://localhost:8000/chat"
    },
    "Claude4": {
        "desc": "Anthropic Claude 4（目前用 Claude 3 Opus 作为占位），需要API Key，适合高质量云端推理。",
        "backend_url": "http://localhost:8000/chat"
    }
}

# Sidebar with app info
with st.sidebar:
    st.header("☁️ Cloud Chat UI")
    st.markdown("""
    - Backend: FastAPI
    - Frontend: Streamlit
    - Avatars: ☁️ (You), 🐷 (Bot)
    """)
    st.markdown("---")
    st.write("Made with ❤️ for chat!")

# Set the title and description
st.title("Cloud Chat☁️——PIG knows!🐷")
st.markdown("🐷：Ask me anything! Glad to help :)")

# --- LLM 选择 ---
st.subheader("选择你的🐷")
llm = st.selectbox(
    "请选择你要聊天的🐷：",
    list(LLM_OPTIONS.keys()),
    format_func=lambda x: f"{x}"
)
st.info(LLM_OPTIONS[llm]["desc"])

api_key = ""
api_key_valid = True
api_key_error = ""
if llm == "Claude4":
    api_key = st.text_input("请输入 Claude API Key（sk-ant-...）", type="password")
    if not api_key:
        api_key_valid = False
        api_key_error = "Claude API Key 不能为空。"
    elif not api_key.startswith("sk-ant-"):
        api_key_valid = False
        api_key_error = "Claude API Key 必须以 sk-ant- 开头。"
    if not api_key_valid:
        st.warning(api_key_error)

st.markdown("---")

# Add a button to clear the chat
if st.button("清空对话", use_container_width=True):
    st.session_state.messages = []

# Initialize the chat history in the session state if it doesn't exist yet
if "messages" not in st.session_state:
    st.session_state.messages = []

# Helper for colored chat bubbles
USER_BUBBLE = "background-color:#e0f7fa; border-radius:10px; padding:8px; margin:4px 0;"
BOT_BUBBLE = "background-color:#f3e5f5; border-radius:10px; padding:8px; margin:4px 0;"

# Display the chat history using chat bubbles and timestamps
for msg in st.session_state.messages:
    with st.chat_message(msg["role"]):
        avatar = "☁️" if msg["role"] == "user" else "🐷"
        bubble_style = USER_BUBBLE if msg["role"] == "user" else BOT_BUBBLE
        timestamp = msg.get("timestamp", "")
        st.markdown(f"<div style='{bubble_style}'>{avatar} <b>{msg['content']}</b> <span style='float:right;font-size:10px;color:#888;'>{timestamp}</span></div>", unsafe_allow_html=True)

# Input box for user message
user_input = st.text_input("请输入你的问题...", key="input", disabled=st.session_state.get("loading", False))

# Send button
send_disabled = st.session_state.get("loading", False) or not user_input.strip()
if llm == "Claude4" and not api_key_valid:
    send_disabled = True

send_clicked = st.button("发送", disabled=send_disabled, use_container_width=True)

# Handle sending message
if send_clicked and user_input.strip():
    st.session_state["loading"] = True
    now = datetime.now().strftime("%H:%M:%S")
    st.session_state.messages.append({"role": "user", "content": user_input, "timestamp": now})
    with st.spinner("Pig is thinking..."):
        try:
            if llm == "Ollama":
                payload = {"message": user_input}
                response = requests.post(LLM_OPTIONS[llm]["backend_url"], json=payload)
            else:
                payload = {"message": user_input, "api_key": api_key, "model": "claude-3-opus-20240229"}
                response = requests.post(LLM_OPTIONS[llm]["backend_url"], json=payload)
            response.raise_for_status()
            reply = response.json()["response"]
            now = datetime.now().strftime("%H:%M:%S")
            st.session_state.messages.append({"role": "assistant", "content": reply, "timestamp": now})
        except Exception as err:
            now = datetime.now().strftime("%H:%M:%S")
            err_msg = str(err)
            # Claude API 错误友好提示
            if hasattr(err, 'response') and err.response is not None:
                try:
                    err_json = err.response.json()
                    err_msg = err_json.get("error", {}).get("message") or err_json.get("error", str(err.response.text))
                except Exception:
                    err_msg = err.response.text
            st.session_state.messages.append({"role": "assistant", "content": f"❌ Error: {err_msg}", "timestamp": now})
    st.session_state["loading"] = False
    st.rerun()  # Refresh to clear input and show new message

# Add a placeholder at the end to auto-scroll
st.empty() 