AGENTX
AgentX is a small Python learning project for experimenting with OpenAI-powered terminal agents and simple game development. It currently contains:

- a basic chatbot example using the OpenAI Chat Completions API
- a tool-calling mini agent that can inspect files, write files, and run terminal commands
- a Snake game built with Python and Pygame

## Requirements

- Python 3.13 or newer
- An OpenAI API key for the agent examples
- Pygame for the Snake game

Project dependencies are listed in `pyproject.toml`:

```toml
openai>=3.10.0
pygame>=2.5.0
python-dotenv>=1.2.3
```

## Setup

Create and activate a virtual environment:

```powershell
python -m venv .venv
.\.venv\Scripts\activate
```

Install dependencies:

```powershell
python -m pip install openai python-dotenv pygame
```

Create a `.env` file in the project root:

```env
OPENAI_API_KEY=your_api_key_here
```

Keep `.env` private. Do not commit or share real API keys.

## Main Files

### `agent.py`

The main terminal agent. It uses OpenAI function tools so the model can:

- `list_files`: list files and folders
- `read_files`: read one or more text files
- `write_files`: create or overwrite files
- `run_command`: run shell commands after user approval

Run it from the project root:

```powershell
python agent.py
```

Type a request at the prompt, for example:

```text
List the files in this project
```

Type `exit` or `quit` to stop.

### `step1.py`

A simple chatbot loop. It sends user messages to the OpenAI API and prints the assistant response.

Run it with:

```powershell
python step1.py
```

### `step2.py`

A smaller function-calling example. It defines a single `read_file` tool and asks the model to summarize the contents of some note files.

Run it with:

```powershell
python step2.py
```

### `snake-game/main.py`

A simple Snake game built with Pygame. The snake moves on a grid, eats food, grows, tracks score, and supports restart after game over.

Run it with:

```powershell
python snake-game\main.py
```

Controls:

- Arrow keys or WASD: move
- R: restart after game over
- Q or Escape: quit after game over

## Project Structure

```text
.
+-- agent.py
+-- step1.py
+-- step2.py
+-- notes.txt
+-- pyproject.toml
+-- uv.lock
+-- src/
|   +-- agenticai/
|       +-- __init__.py
+-- snake-game/
    +-- main.py
    +-- README.md
    +-- requirements.txt
```

## Troubleshooting

### `ModuleNotFoundError: No module named 'openai'`

Install dependencies into the same Python environment used to run the script:

```powershell
python -m pip install openai python-dotenv
```

### `ModuleNotFoundError: No module named 'pygame'`

Install Pygame into the active environment:

```powershell
python -m pip install pygame
```

### OpenAI API connection errors

Check your internet connection, VPN, proxy, antivirus, or firewall settings. Also confirm your `.env` file contains a valid `OPENAI_API_KEY`.

### `reasoning_effort` tool errors

For `gpt-5.6-luna` with function tools in Chat Completions, the request must use:

```python
reasoning_effort="none"
```

This is already set in the tool-calling examples.

## Notes

This project is mainly educational. The terminal agent can write files and run shell commands, so review command prompts carefully before approving command execution.
