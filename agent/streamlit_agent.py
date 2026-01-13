# agent/streamlit_agent.py
from typing import Dict, Any

from agent.state import AgentState
from agent.intent import classify_intent
from agent.llm import ask_llm
from rag.retriever import AutoStreamRetriever
from tools.lead_capture import mock_lead_capture

retriever = AutoStreamRetriever()


def ensure_state_defaults(state: AgentState) -> AgentState:
    state.setdefault("messages", [])
    state.setdefault("retrieved_context", "")
    state.setdefault("lead_captured", False)
    state.setdefault("user_name", None)
    state.setdefault("user_email", None)
    state.setdefault("user_platform", None)
    return state


def need_more_lead_info(state: AgentState) -> str | None:
    if not state.get("user_name"):
        return "May I know your name? Please say: 'my name is ...'"
    if not state.get("user_email"):
        return "Please share your email so the team can contact you."
    if not state.get("user_platform"):
        return "Which platform do you mainly create content for? (YouTube, TikTok, Instagram, Twitch)"
    return None


def maybe_capture_lead(state: AgentState) -> bool:
    if (
        not state.get("lead_captured")
        and state.get("user_name")
        and state.get("user_email")
        and state.get("user_platform")
    ):
        mock_lead_capture(
            state["user_name"], state["user_email"], state["user_platform"]
        )
        state["lead_captured"] = True
        return True
    return False


def agent_turn(user_text: str, ui_state: Dict[str, Any]) -> Dict[str, Any]:
    """
    Single turn of your agent for Streamlit UI.

    ui_state: free-form dict stored in st.session_state["agent_state"].
    It contains:
      - "internal_state": your AgentState
      - "messages": list of {role, content}
      - "last_reply": last assistant message
    """

    internal_state: AgentState = ui_state.get("internal_state", {}) 
    ensure_state_defaults(internal_state)

    internal_state["messages"].append({"role": "user", "content": user_text})

    if "@" in user_text and "." in user_text and " " not in user_text:
        internal_state["user_email"] = user_text
    elif user_text.lower() in {"youtube", "tiktok", "instagram", "twitch"}:
        internal_state["user_platform"] = user_text
    elif "my name is" in user_text.lower():
        internal_state["user_name"] = user_text.split("is", 1)[1].strip()

    intent = classify_intent(user_text)
    internal_state["intent"] = intent

    in_lead_flow = (
        intent == "high_intent"
        or not internal_state.get("lead_captured")
        and (
            internal_state.get("user_name")
            or internal_state.get("user_email")
            or internal_state.get("user_platform")
        )
    )

    if in_lead_flow:
        missing_question = need_more_lead_info(internal_state)
        if missing_question:
            reply = missing_question
        else:
            just_captured = maybe_capture_lead(internal_state)
            if just_captured:
                reply = (
                    "Thanks! You’re all set. The team will reach out shortly about AutoStream."
                )
            else:
                reply = "Thanks, noted."
    else:
        context = ""
        if intent == "product_query":
            docs = retriever.get_relevant_docs(user_text)
            context = "\n\n---\n\n".join(docs)
            internal_state["retrieved_context"] = context

        reply = ask_llm(user_text, context=context or None)

    ui_state.setdefault("messages", [])
    ui_state["messages"].append({"role": "user", "content": user_text})
    ui_state["messages"].append({"role": "assistant", "content": reply})
    ui_state["last_reply"] = reply
    ui_state["internal_state"] = internal_state

    return ui_state
