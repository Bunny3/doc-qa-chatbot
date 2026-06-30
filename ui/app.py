# ui/app.py
import streamlit as st
import requests

API_URL = "http://127.0.0.1:8000"

st.set_page_config(page_title="Doc QA Chatbot", page_icon="📄")
st.title("📄 Document Q&A Chatbot")
st.caption("RAG-powered chatbot — ask questions about your uploaded PDF")

# Initialize chat history in session state
if "messages" not in st.session_state:
    st.session_state.messages = []

# --- Sidebar: PDF status + health check ---
with st.sidebar:
    st.header("📊 Status")
    try:
        health = requests.get(f"{API_URL}/health", timeout=5).json()
        st.success(f"✅ API connected")
        st.metric("Chunks in store", health["chunks_in_store"])
    except requests.exceptions.RequestException:
        st.error("❌ API not reachable. Is the FastAPI server running?")

    st.divider()
    st.caption("This demo uses a pre-ingested sample.pdf (the 'Attention Is All You Need' paper)")

# --- Display chat history ---
for msg in st.session_state.messages:
    with st.chat_message(msg["role"]):
        st.markdown(msg["content"])
        if msg["role"] == "assistant" and msg.get("sources"):
            with st.expander("📎 Sources"):
                for s in msg["sources"]:
                    st.caption(f"- {s['source']}, page {s['page']}")

# --- Chat input ---
if question := st.chat_input("Ask a question about the document..."):
    # Show user message
    st.session_state.messages.append({"role": "user", "content": question})
    with st.chat_message("user"):
        st.markdown(question)

    # Call the API
    with st.chat_message("assistant"):
        with st.spinner("Thinking..."):
            try:
                response = requests.post(
                    f"{API_URL}/chat",
                    json={"question": question, "top_k": 3},
                    timeout=30,
                )
                response.raise_for_status()
                result = response.json()

                st.markdown(result["answer"])
                if result["sources"]:
                    with st.expander("📎 Sources"):
                        for s in result["sources"]:
                            st.caption(f"- {s['source']}, page {s['page']}")

                st.session_state.messages.append({
                    "role": "assistant",
                    "content": result["answer"],
                    "sources": result["sources"],
                })
            except requests.exceptions.RequestException as e:
                error_msg = f"⚠️ Error reaching the API: {e}"
                st.error(error_msg)
                st.session_state.messages.append({"role": "assistant", "content": error_msg})