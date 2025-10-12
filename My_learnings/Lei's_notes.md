**1.** In AI engineering, there are two main ways to build an AI agent:

a. Using frameworks such as LangChain, LlamaIndex, CrewAI, or AutoGen, and
b. Building one from scratch using pure Python or Java code combined with an LLM API.

Each approach has its own advantages and disadvantages. Frameworks offer speed and convenience, while custom implementations provide flexibility and control. Below are some of the key pros and cons of both methods: 

| Criteria                 | With Framework   | Without Framework (Pure Python) |
| ------------------------ | ---------------- | ------------------------------- |
| **Speed of Development** | 🚀 Fast          | 🐢 Slower                       |
| **Flexibility/Control**  | ⚙️ Limited       | 🧩 Full control                 |
| **Performance**          | Moderate         | High                            |
| **Learning Curve**       | Steep            | Moderate                        |
| **Maintenance**          | Easier initially | Harder long-term                |
| **Dependencies**         | Many             | Minimal                         |
| **Debugging**            | Complex          | Simple                          |
| **Scalability**          | High             | Manual effort                   |

**2.** There's a new tool called **UV**. It aims to serve as a drop-in replacement (or even unification) for many existing Python tools: pip, virtualenv, pipx, pip-tools, pyenv, poetry, etc.

**It can manage:**
Dependencies (installing, resolving, locking) 
Virtual environments and isolation of tool installs 
Project operations (running scripts, syncing environments, possibly building/publishing) 
Tool execution: it can run and install CLI tools in isolated environments (via uv tool run or the alias uvx)

**Current Limitations & Considerations**

While UV supports major workflows, it may not yet match every legacy or obscure feature of pip or other tooling. 
Because it's newer, community adoption, documentation, and ecosystem support are still growing.
Migration from existing tooling (poetry, pipenv, etc.) may require adjustments in project layout or configurations.
Tooling around publishing or certain edge cases might still rely on external tools (e.g. using twine).

**UV Docs**
https://docs.astral.sh/uv/getting-started/installation/
https://docs.astral.sh/uv/
