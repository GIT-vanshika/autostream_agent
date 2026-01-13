from typing import TypedDict


def mock_lead_capture(name: str, email: str, platform: str) -> None:
    print(f"Lead captured successfully: {name}, {email}, {platform}")


class LeadInput(TypedDict):
    name: str
    email: str
    platform: str
