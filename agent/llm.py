from google import genai
from config import GOOGLE_API_KEY

client = genai.Client(api_key=GOOGLE_API_KEY)

MODEL_NAME = "models/gemini-2.5-flash" 


def ask_llm(user_message: str, context: str | None = None) -> str:
    if context:
        system_prompt = (
            "You are AutoStream's product assistant. "
            "Use the following knowledge base to answer questions about pricing, "
            "plans, policies, and supported platforms.\n\n"
            f"{context}\n\n"
        )
    else:
        system_prompt = (
            "You are AutoStream's product assistant. Answer briefly and clearly.\n\n"
        )

    prompt = system_prompt + f"User: {user_message}\nAssistant:"

    result = client.models.generate_content(
        model=MODEL_NAME,
        contents=prompt,
    )
    return result.text.strip()
