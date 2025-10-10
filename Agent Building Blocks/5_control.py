"""
'Control is what transforms an AI agent from being reactive to being reliable.'
"""

from openai import OpenAI
from pydantic import BaseModel
from typing import Literal


class IntentClassification(BaseModel):
    """Define the expected structure for intent classification output."""
    intent: Literal["question", "request", "complaint"]
    confidence: float
    reasoning: str


def route_based_on_intent(user_input: str) -> tuple[str, IntentClassification]:
    client = OpenAI()

    # Use the LLM to classify user input and return structured output
    response = client.responses.parse(
        model="gpt-4o",
        input=[
            {
                "role": "system",
                "content": "Classify user input into one of three categories: question, request, or complaint. Provide your reasoning and confidence level.",
            },
            {"role": "user", "content": user_input},
        ],
        text_format=IntentClassification,  # Enforce schema validation
    )

    classification = response.output_parsed
    intent = classification.intent

    # Route the logic based on detected intent
    if intent == "question":
        result = answer_question(user_input)
    elif intent == "request":
        result = process_request(user_input)
    elif intent == "complaint":
        result = handle_complaint(user_input)
    else:
        result = "I'm not sure how to help with that."

    return result, classification


def answer_question(question: str) -> str:
    # Ask the LLM to answer user questions
    client = OpenAI()
    response = client.responses.create(
        model="gpt-4o", input=f"Answer this question: {question}"
    )
    return response.output[0].content[0].text


def process_request(request: str) -> str:
    # Simulate request handling logic
    return f"Processing your request: {request}"


def handle_complaint(complaint: str) -> str:
    # Simulate complaint handling logic
    return f"I understand your concern about: {complaint}. Let me escalate this."


if __name__ == "__main__":
    # Test various inputs to see how the agent routes each one
    test_inputs = [
        "What is machine learning?",
        "Please schedule a meeting for tomorrow",
        "I'm unhappy with the service quality",
    ]

    for user_input in test_inputs:
        print(f"\nInput: {user_input}")
        result, classification = route_based_on_intent(user_input)
        print(
            f"Intent: {classification.intent} (confidence: {classification.confidence})"
        )
        print(f"Reasoning: {classification.reasoning}")
        print(f"Response: {result}")
