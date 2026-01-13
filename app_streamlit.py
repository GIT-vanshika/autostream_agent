import streamlit as st

from agent.streamlit_agent import agent_turn

st.set_page_config(page_title="AutoStream Assistant", page_icon="🎬")

st.title("🎬 AutoStream Support Agent")

if "agent_state" not in st.session_state:
    st.session_state.agent_state = {
        "internal_state": {},  
        "messages": [],       
        "last_reply": "",
    }

for msg in st.session_state.agent_state["messages"]:
    role = msg["role"]
    with st.chat_message("user" if role == "user" else "assistant"):
        st.markdown(msg["content"])

user_input = st.chat_input(
    "Ask about AutoStream pricing, features, or say you want to buy..."
)

if user_input:
    with st.chat_message("user"):
        st.markdown(user_input)

    new_state = agent_turn(user_input, st.session_state.agent_state)
    st.session_state.agent_state = new_state

    assistant_reply = new_state["last_reply"]
    with st.chat_message("assistant"):
        st.markdown(assistant_reply)
