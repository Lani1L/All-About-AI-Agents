"""
Feedback fuels intelligence.
"""

from openai import OpenAI 

# Ask for human approval before finalizing the AI output
def get_human_approval(content: str) -> bool:
    print(f"Generated content:\n{content}\n")
    response = input("Approve this? (y/n): ")
    return response.lower().startswith("y")


def intelligence_with_human_feedback(prompt: str) -> None:
    client = OpenAI()

    # Generate initial AI response (draft)
    response = client.responses.create(model="gpt-4o", input=prompt)
    draft_response = response.output_text

    # Require human approval before finalizing
    if get_human_approval(draft_response):
        print("✅ Final answer approved")
    else:
        print("❌ Answer not approved")


if __name__ == "__main__":
    # Example use: human reviews AI-generated poem
    intelligence_with_human_feedback("Write a short poem about technology")

