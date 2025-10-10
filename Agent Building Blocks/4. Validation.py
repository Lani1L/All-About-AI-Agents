"""
More info: https://platform.openai.com/docs/guides/structured-outputs?api-mode=responses
"""

from openai import OpenAI 
from pydantic import BaseModel


class TaskResult(BaseModel):
    # Define the expected structured output schema for the model.
    task: str
    completed: bool
    priority: int


def structured_intelligence(prompt: str) -> TaskResult:
    client = OpenAI()

    # Ask the model to extract structured data and validate it using Pydantic
    response = client.responses.parse(
        model="gpt-4o",
        input=[
            {"role": "system", "content": "Extract task information from the user input."},
            {"role": "user", "content": prompt},
        ],
        text_format=TaskResult,  # Enforce structured output format
    )
    return response.output_parsed  # Return parsed, validated result


if __name__ == "__main__":
    # Example: extract structured task info from natural language
    result = structured_intelligence(
        "I need to complete the project presentation by Friday, it's high priority"
    )
    print("Structured Output:")
    print(result.model_dump_json(indent=2))
    print(f"Extracted task: {result.task}")
