import json
import os
import subprocess
import sys
from pathlib import Path

PROJECT_DIR = Path(__file__).resolve().parent
VENV_PYTHON = PROJECT_DIR / ".venv" / "Scripts" / "python.exe"

if VENV_PYTHON.exists() and Path(sys.executable).resolve() != VENV_PYTHON.resolve():
    os.execv(str(VENV_PYTHON), [str(VENV_PYTHON), *sys.argv])

from openai import APIConnectionError, AuthenticationError, OpenAI, OpenAIError
from dotenv import load_dotenv
load_dotenv()

client =OpenAI()
MODEL = "gpt-5.6-luna"
WORKING_DIR = Path.cwd()

SYSTEM_PROMPT = """You are a coding agent running in the user's terminal.
You can list files, read files, write files, and run shell commands.
Use your tools to complete the user's task, then briefly summarize what you did.
The working directory is the folder the user launched you from."""


def resolve_path(path):
    target = (WORKING_DIR / path).resolve()
    try:
        target.relative_to(WORKING_DIR)
    except ValueError:
        raise ValueError("Path must stay inside the working directory.")
    return target


def list_files(path="."):
    entries = []
    target = resolve_path(path)
    for entry in target.iterdir():
        entries.append(str(entry.relative_to(WORKING_DIR)) + ("/" if entry.is_dir() else ""))
    return "\n".join(sorted(entries)) or "(empty directory)"


def read_files(paths):
    results = {}
    for path in paths:
        target = resolve_path(path)
        if not target.exists():
            results[path] = "File not found."
        elif not target.is_file():
            results[path] = "Path is not a file."
        else:
            results[path] = target.read_text(encoding="utf-8")
    return json.dumps(results, indent=2)


def write_files(files):
    results = {}
    for file_info in files:
        path = file_info["path"]
        content = file_info["content"]
        target = resolve_path(path)
        target.parent.mkdir(parents=True, exist_ok=True)
        target.write_text(content, encoding="utf-8")
        results[path] = f"Saved {path} ({len(content)} characters)"
    return json.dumps(results, indent=2)


def run_command(command):
    try:
        answer = input(f"  Run '{command}'? [y/N] ")
    except (EOFError, KeyboardInterrupt):
        return "Could not ask for approval because stdin is closed."

    if answer.strip().lower() != "y":
        return "The user declined to run this command."

    result = subprocess.run(
        command, shell=True, capture_output=True, text=True, timeout=120
    )
    output = (result.stdout + result.stderr).strip()
    return output or f"(no output, exit code {result.returncode})"


TOOLS = {
    "list_files": list_files,
    "read_files": read_files,
    "write_files": write_files,
    "run_command": run_command,
}

TOOL_SCHEMAS = [
    {
        "type": "function",
        "function": {
            "name": "list_files",
            "description": "List the files in a directory. Folders end with /.",
            "parameters": {
                "type": "object",
                "properties": {
                    "path": {"type": "string", "description": "Directory to list, e.g. '.'"},
                },
                "required": ["path"],
            },
        },
    },
    {
        "type": "function",
        "function": {
            "name": "read_files",
            "description": "Read one or more text files and return their contents.",
            "parameters": {
                "type": "object",
                "properties": {
                    "paths": {
                        "type": "array",
                        "items": {"type": "string"},
                        "description": "Paths of the files to read",
                    },
                },
                "required": ["paths"],
            },
        },
    },
    {
        "type": "function",
        "function": {
            "name": "write_files",
            "description": "Create or overwrite one or more text files with the given content.",
            "parameters": {
                "type": "object",
                "properties": {
                    "files": {
                        "type": "array",
                        "items": {
                            "type": "object",
                            "properties": {
                                "path": {"type": "string", "description": "Path of the file to write"},
                                "content": {"type": "string", "description": "Full contents of the file"},
                            },
                            "required": ["path", "content"],
                        },
                    },
                },
                "required": ["files"],
            },
        },
    },
    {
        "type": "function",
        "function": {
            "name": "run_command",
            "description": "Run a shell command and return its output. The user approves it first.",
            "parameters": {
                "type": "object",
                "properties": {
                    "command": {"type": "string", "description": "The shell command to run"},
                },
                "required": ["command"],
            },
        },
    },
]


def run_tool(tool_call):
    name = tool_call.function.name
    args = json.loads(tool_call.function.arguments)
    print(f"  tool: {name}({args})")
    try:
        return str(TOOLS[name](**args))
    except Exception as error:
        return f"Error: {error}"



def run_agent(messages):
    while True:
        try:
            response = client.chat.completions.create(
                model=MODEL,
                messages=messages,
                tools=TOOL_SCHEMAS,
                reasoning_effort="none",
            )
        except AuthenticationError:
            return (
                "OpenAI authentication failed. Check that OPENAI_API_KEY is set correctly "
                "in your .env file or terminal environment."
            )
        except APIConnectionError:
            return (
                "Could not connect to the OpenAI API. Check your internet connection, VPN, "
                "proxy, antivirus, or Windows firewall settings, then try again."
            )
        except OpenAIError as error:
            return f"OpenAI API error: {error}"

        message = response.choices[0].message
        messages.append(message)

        # No tool calls means the model is done and answered in plain text
        if not message.tool_calls:
            return message.content

        for tool_call in message.tool_calls:
            result = run_tool(tool_call)
            messages.append({
                "role": "tool",
                "tool_call_id": tool_call.id,
                "content": result,
            })
       
            
def main():
    messages = [{"role": "system", "content": SYSTEM_PROMPT}]
    print("Mini agent ready. Type 'exit' to quit.")
    while True:
        try:
            user_input = input("\nYou: ")
        except (EOFError, KeyboardInterrupt):
            print()
            break

        if user_input.strip().lower() in ("exit", "quit"):
            break

        messages.append({"role": "user", "content": user_input})
        reply = run_agent(messages)
        print(f"\nAgent: {reply}")


if __name__ == "__main__":
    main()
