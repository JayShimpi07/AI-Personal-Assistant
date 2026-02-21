import streamlit as st
import requests

# ==============================
# PAGE CONFIG (MUST BE FIRST)
# ==============================
st.set_page_config(
    page_title="Personal AI Assistant",
    page_icon="✨",
    layout="wide"
)

# ==============================
# LOAD CSS
# ==============================
with open("style.css", encoding="utf-8") as f:
    st.markdown(f"<style>{f.read()}</style>", unsafe_allow_html=True)

st.markdown(
    """
    <style>
    footer {visibility: hidden;}
    </style>
    """,
    unsafe_allow_html=True
)
# ==============================
# HEADER
# ==============================
st.markdown("""
<div class="header">
    <h1>✨ Personal AI Assistant</h1>
    <p>Your intelligent workspace companion powered by automation.</p>
</div>
""", unsafe_allow_html=True)

# ==============================
# FEATURES GRID
# ==============================
st.markdown("""
<div class="feature-grid">

<div class="feature-card">🧠 Answer intelligent questions</div>
<div class="feature-card">📅 Manage calendar events</div>
<div class="feature-card">📧 Read & send emails</div>
<div class="feature-card">✅ Manage tasks</div>
<div class="feature-card">📝 Create notes</div>
<div class="feature-card">💰 Track expenses</div>

</div>
""", unsafe_allow_html=True)

st.divider()

# ==============================
# CHAT HISTORY INIT
# ==============================
if "messages" not in st.session_state:
    st.session_state.messages = []

st.subheader("💬 Chat")

# ==============================
# DISPLAY CHAT HISTORY
# ==============================
for message in st.session_state.messages:
    role = message.get("role", "assistant")
    content = message.get("content", "")

    with st.chat_message(role):
        st.markdown(content)

# ==============================
# CHAT INPUT
# ==============================
user_message = st.chat_input("Ask your assistant anything...")

# ==============================
# SAFE RESPONSE PARSER
# ==============================
def extract_ai_response(resp):
    try:
        data = resp.json()

        if isinstance(data, dict):
            return data.get("output") or data.get("response") or str(data)

        if isinstance(data, list) and len(data) > 0:
            item = data[0]
            if isinstance(item, dict):
                return item.get("output") or item.get("response") or str(item)

        return str(data)

    except Exception:
        return "⚠️ Failed to read assistant response."

# ==============================
# SEND MESSAGE
# ==============================
if user_message:

    # show user message
    with st.chat_message("user"):
        st.markdown(user_message)

    st.session_state.messages.append(
        {"role": "user", "content": user_message}
    )

    # assistant response
    with st.chat_message("assistant"):
        with st.spinner("Assistant is thinking..."):

            try:
                response = requests.post(
                    "https://jayshimpi07.app.n8n.cloud/webhook/6e55ccdc-3ac9-43e1-9900-eefca464488e",
                    json={"message": user_message},
                    timeout=60
                )

                ai_response = extract_ai_response(response)

            except requests.exceptions.RequestException:
                ai_response = "❌ Unable to connect to assistant backend."

        st.markdown(ai_response)

    st.session_state.messages.append(
        {"role": "assistant", "content": ai_response}
    )