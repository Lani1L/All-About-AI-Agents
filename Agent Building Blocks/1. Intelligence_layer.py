"""
'An AI agent’s true intelligence isn’t measured by what it knows, but by how well it learns, adapts, and acts with purpose.'

You can find the OpenAI documentation below:
https://platform.openai.com/docs/quickstart?desktop-os=windows&language=python

"""

from openai import OpenAI  

# Sends a prompt to the GPT-4o model and returns the generated response
def basic_intelligence(prompt: str) -> str:
    client = OpenAI()  # Initialize OpenAI client
    response = client.responses.create(model="gpt-4o", input=prompt)  # Call the model
    return response.output_text  # Extract and return model output


if __name__ == "__main__":
    # Example usage of the function
    result = basic_intelligence(prompt="What is Agentic AI?")
    print("Basic Intelligence Output:")
    print(result)
