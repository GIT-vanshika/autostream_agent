# app.py
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
    """Return True if lead was captured this turn."""
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


def main():
    state: AgentState = {}
    ensure_state_defaults(state)

    print("AutoStream assistant. Type 'exit' to quit.\n")

    while True:
        user_text = input("You: ").strip()
        if user_text.lower() in {"exit", "quit"}:
            break

        state["messages"].append({"role": "user", "content": user_text})

        
        if "@" in user_text and "." in user_text and " " not in user_text:
            state["user_email"] = user_text

        elif user_text.lower() in {"youtube", "tiktok", "instagram", "twitch"}:
            state["user_platform"] = user_text

        elif "my name is" in user_text.lower():
            state["user_name"] = user_text.split("is", 1)[1].strip()

        intent = classify_intent(user_text)
        state["intent"] = intent

        in_lead_flow = (
            intent == "high_intent"
            or not state.get("lead_captured")
            and (
                state.get("user_name")
                or state.get("user_email")
                or state.get("user_platform")
            )
        )

        if in_lead_flow:
            missing_question = need_more_lead_info(state)
            if missing_question:
                print("Agent:", missing_question)
            else:
                just_captured = maybe_capture_lead(state)
                if just_captured:
                    print(
                        "Agent: Thanks! You’re all set. The team will reach out shortly about AutoStream."
                    )
            continue

        context = ""
        if intent == "product_query":
            docs = retriever.get_relevant_docs(user_text)
            context = "\n\n---\n\n".join(docs)
            state["retrieved_context"] = context

        answer = ask_llm(user_text, context=context or None)
        state["messages"].append({"role": "assistant", "content": answer})
        print("Agent:", answer)


if __name__ == "__main__":
    main()
