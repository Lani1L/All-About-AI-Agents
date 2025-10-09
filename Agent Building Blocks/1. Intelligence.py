"""
You can find the OpenAI documentation below:
https://platform.openai.com/docs/quickstart?desktop-os=windows&language=python

"""

from openai import OpenAI  

# Define a function that sends a prompt to the GPT-4o model and returns the response
def basic_intelligence(prompt: str) -> str:
    client = OpenAI()
    response = client.responses.create(model="gpt-4o", input=prompt)
    return response.output_text


if __name__ == "__main__":
    result = basic_intelligence(prompt="What is Agentic AI?")
    print("Basic Intelligence Output:")
    print(result)
