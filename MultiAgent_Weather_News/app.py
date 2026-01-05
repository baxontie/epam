import streamlit as st
from agents.orchestrator import Orchestrator

st.set_page_config(page_title="Multi-Agent Weather & News Assistant")

st.title("Multi-Agent Weather & News Assistant")

orchestrator = Orchestrator()

if "messages" not in st.session_state:
    st.session_state.messages = []

for msg in st.session_state.messages:
    with st.chat_message(msg["role"]):
        st.markdown(msg["content"])

user_input = st.chat_input("Ask about weather, news, or both...")

if user_input:
    st.session_state.messages.append({
        "role": "user",
        "content": user_input
    })

    with st.chat_message("user"):
        st.markdown(user_input)

    with st.chat_message("assistant"):
        response = orchestrator.handle(user_input)
        st.markdown(response)

    st.session_state.messages.append({
        "role": "assistant",
        "content": response
    })
