from typing import List, Literal, Optional, TypedDict

IntentType = Literal["greeting", "product_query", "high_intent", "unknown"]


class Message(TypedDict):
    role: Literal["user", "assistant"]
    content: str


class AgentState(TypedDict, total=False):
    messages: List[Message]

    intent: IntentType

    retrieved_context: str

    user_name: Optional[str]
    user_email: Optional[str]
    user_platform: Optional[str]
    lead_captured: bool
