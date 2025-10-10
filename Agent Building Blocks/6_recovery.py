"""
An intelligent agent isn’t the one that never fails, but the one that knows how to recover gracefully.
"""

from typing import Optional 
from openai import OpenAI
from pydantic import BaseModel


class UserInfo(BaseModel):
    """Define structured schema for extracting user information."""
    name: str
    email: str
    age: Optional[int] = None  # Optional field (may not always be provided)


def resilient_intelligence(prompt: str) -> str:
    client = OpenAI()

    # Ask the LLM to extract structured user data and validate with Pydantic
    response = client.responses.parse(
        model="gpt-4o",
        input=[
            {"role": "system", "content": "Extract user information from the text."},
            {"role": "user", "content": prompt},
        ],
        text_format=UserInfo,  # Expected schema for the output
        temperature=0.0,  # Keep deterministic output
    )

    user_data = response.output_parsed.model_dump()

    try:
        # Attempt to use age field; handle cases where it's missing or invalid
        age = user_data["age"]
        if age is None:
            raise ValueError("Age is None")
        age_info = f"User is {age} years old"
        return age_info

    except (KeyError, TypeError, ValueError):
        print("❌ Age not available, using fallback info...")

        # Fallback path using only guaranteed fields
        return f"User {user_data['name']} has email {user_data['email']}"


if __name__ == "__main__":
    # Example: missing age triggers recovery logic
    result = resilient_intelligence(
        "My name is John Smith and my email is john@example.com"
    )
    print("Recovery Output:")
    print(result)

