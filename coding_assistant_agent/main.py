# /// script
# requires-python = ">=3.13"
# dependencies = [
#     "anthropic",
#     "pydantic",
# ]
# ///

import os
import sys
import argparse # for CLI argument parsing
import logging
from typing import List, Dict, Any
from anthropic import Anthropic # type: ignore
from pydantic import BaseModel # type: ignore

# Configure logging
logging.basicConfig(
    level=logging.INFO,
    format="%(asctime)s - %(levelname)s - %(message)s",
    handlers=[logging.FileHandler("agent.log")]
)
# Suppress overly verbose logs from httpcore and httpx
logging.getLogger("httpcore").setLevel(logging.WARNING)
logging.getLogger("httpx").setLevel(logging.WARNING)

# Tool definition using pydantic for input validation
class Tool(BaseModel):
    name: str
    description: str
    input_schema: Dict[str, Any]

class AIAgent:
    def __init__(self, api_key: str):
        self.client = Anthropic(api_key=api_key)
        self.messages: List[Dict[str, Any]] = []
        self.tools: List[Tool] = []
        self.max_retries = 3
        self._setup_tools()
    
    # Define tools
    def _setup_tools(self):
        self.tools = [
            Tool(
                name="read_file",
                description="Reads the content of a specified path.",
                input_schema={
                    "type": "object",
                    "properties": {
                        "path": {"type": "string", "description": "The file path to read."}
                    },
                    "required": ["path"],
                },
            ),
            Tool(
                name="list_files",
                description="List all files and directories in the specified path.",
                input_schema={
                    "type": "object",
                    "properties": {
                        "path": {"type": "string", "description": "The directory path to list (defaults to current directory)"}
                    },
                    "required": [],
                },
            ),
            Tool(
                name="edit_file",
                description="Edit a file by replacing old_text with new_text. Creates the file if it doesn't exist.",
                input_schema={
                    "type": "object",
                    "properties": {
                        "path": {"type": "string", "description": "The path to the file to edit."},
                        "old_text": {"type": "string", "description": "The text to search for and replace (leave empty to create new file)"},
                        "new_text": {"type": "string", "description": "The text to replace old_text with"},

                    },
                    "required": ["path", "new_text"],
                },
            ),

        ]
    # Tool execution logic    
    def _execute_tool(self, tool_name:str, tool_input: Dict[str, Any]) -> str:
        logging.info(f"Executing tool: {tool_name} with input: {tool_input}")
        try:
            if tool_name == "read_file":
                return self._read_file(tool_input["path"])
            elif tool_name == "list_files":
                return self._list_files(tool_input.get("path", "."))
            elif tool_name == "edit_file":
                return self._edit_file(
                    tool_input["path"],
                    tool_input.get("old_text", ""),
                    tool_input["new_text"]
                )
            else:
                return f"Error: Unknown tool '{tool_name}'"
        except Exception as e:
            logging.error(f"Error executing tool '{tool_name}': {str(e)}")
            return f"Error executing tool '{tool_name}': {str(e)}"
        
    def _read_file(self, path: str) -> str:
        try:
            with open(path, 'r', encoding='utf-8') as f:
                content = f.read()
            return f"File contents of '{path}':\n{content}"
        except FileNotFoundError:
            return f"Error: File '{path}' not found."
        except Exception as e:
            return f"Error reading file '{path}': {str(e)}"

    def _list_files(self, path: str) -> str:
        try:
            if not os.path.exists(path):
                return f"Path not found: {path}"

            items = []
            for item in sorted(os.listdir(path)):
                item_path = os.path.join(path, item)
                if os.path.isdir(item_path):
                    items.append(f"[DIR]  {item}/")
                else:
                    items.append(f"[FILE] {item}")

            if not items:
                return f"Empty directory: {path}"

            return f"Contents of {path}:\n" + "\n".join(items)
        except Exception as e:
            return f"Error listing files: {str(e)}"

    def _edit_file(self, path: str, old_text: str, new_text: str) -> str:
        try:
            if os.path.exists(path) and old_text:
                with open(path, "r", encoding='utf-8') as f:
                    content = f.read()
                if old_text not in content:
                    return f"Text not found in file: {old_text}"
                content = content.replace(old_text, new_text)
                with open(path, "w", encoding='utf-8') as f:
                    f.write(content)
                return f"Successfully edited file '{path}'."
            else:

                dir_name = os.path.dirname(path)
                if dir_name:
                    os.makedirs(dir_name, exist_ok=True)

                with open(path, "w", encoding='utf-8') as f:
                    f.write(new_text)
                return f"Successfully created file '{path}'."
        except Exception as e:
            return f"Error editing file '{path}': {str(e)}"
    
    # Conversational loop    
    def chat(self, user_input: str) -> str:
        logging.info(f"User input: {user_input}")
        self.messages.append({"role": "user", "content": user_input})
        retries = 3

        tool_schema = [
            {
                "name": tool.name,
                "description": tool.description,
                "parameters": tool.input_schema
            }
            for tool in self.tools
        ]

        while True:
            try:
                response = self.client.messages.create(
                    model = "claude-3-5-haiku-20241022",
                    max_tokens=2000,
                    system="You are a helpful coding assistant operating in a terminal environment. Output only plain text without markdown formatting, as your respones appear directly in the terminal. Be concise but thorough, providing clear and practical advice with a friendly tone. Don't use any asterisk characters in your responses.",
                    messages=self.messages,
                    tools=tool_schema,
                )

                assistant_message = {"role": "assistant", "content": []}

                for content in response.content:
                    if content.type == "text":
                        assistant_message["content"].append(
                            {"type": "text", "text": content.text}
                        )
                    elif content.type == "tool_use":
                        assistant_message["content"].append(
                            {
                                "type": "tool_use",
                                "id": content.id,
                                "name": content.name,
                                "input": content.input,
                            }
                        )
                self.messages.append(assistant_message)

                tool_results = []
                for content in response.content:
                    if content.type == "tool_use":
                        result = self._execute_tool(content.name, content.input)
                        logging.info(
                            f"Tool result: {result[:500]}..."                           
                        )
                        tool_results.append(
                            {
                                "type": "tool_result",
                                "tool_use_id": content.id,
                                "content": result,
                            }
                        )
                if tool_results:
                    self.messages.append(
                        {"role": "tool", "content": tool_results}
                    )
                else:
                    return response.content[0].text if response.content else ""
            except Exception as e:
                return f"Error: {str(e)}"

# Command-line interface
def main():
    parser = argparse.ArgumentParser(
        description="AI Code Assistant - A convesational AI agent for file operations."
    )
    parser.add_argument(
        "--api-key",
        help="Anthropic API key (or set ANTHROPIC_API_KEY env variable)"
    )
    args = parser.parse_args()

    api_key = args.api_key or os.environ.get("ANTHROPIC_API_KEY")
    if not api_key:
        print(
            "Error: Please provide an API key via --api-key or ANTHROPIC_API_KEY environment variable."
        )
        sys.exit(1)

    agent = AIAgent(api_key)

    print(" AI Code Assistant")
    print("==================")
    print("A conversational AI agent that can read, list, and edit files.")
    print("Type 'exit' or 'quit' to end the session.\n")
    print()

    while True:
        try:
            user_input = input("You: ").strip()
            if user_input.lower() in ["exit", "quit"]:
                print("Exiting. Goodbye!")
                break
            if not user_input:
                continue

            print("\nAssistant: ", end="", flush=True)
            response = agent.chat(user_input)
            print(response)
            print()

        except (KeyboardInterrupt, EOFError):
            print("\nExiting. Goodbye!")
            break
        
        except Exception as e:
            print(f"Error: {str(e)}")
            print()

if __name__ == "__main__":
        main()


