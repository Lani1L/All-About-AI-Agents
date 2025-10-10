"""
'An agent without memory is like a human with amnesia. you have to repeat all over again'

More info: https://platform.openai.com/docs/guides/conversation-state?api-mode=responses
"""

from openai import OpenAI

client = OpenAI()  # Initialize OpenAI client


def ask_joke_without_memory():
    # Ask the model for a programming joke (no memory)
    response = client.responses.create(
        model="gpt-4o-mini",
        input=[
            {"role": "user", "content": "Tell me a joke about programming"},
        ],
    )
    return response.output_text


def ask_followup_without_memory():
    # Ask a follow-up question without context (the model won’t remember)
    response = client.responses.create(
        model="gpt-4o-mini",
        input=[
            {"role": "user", "content": "What was my previous question?"},
        ],
    )
    return response.output_text


def ask_followup_with_memory(joke_response: str):
    # Recreate conversation history so the model has context
    response = client.responses.create(
        model="gpt-4o-mini",
        input=[
            {"role": "user", "content": "Tell me a joke about programming"},
            {"role": "assistant", "content": joke_response},
            {"role": "user", "content": "What was my previous question?"},
        ],
    )
    return response.output_text


if __name__ == "__main__":
    # Step 1: Ask for a joke
    joke_response = ask_joke_without_memory()
    print(joke_response, "\n")

    # Step 2: Ask follow-up without memory (AI forgets)
    confused_response = ask_followup_without_memory()
    print(confused_response, "\n")

    # Step 3: Ask follow-up with memory (AI recalls context)
    memory_response = ask_followup_with_memory(joke_response)
    print(memory_response)

