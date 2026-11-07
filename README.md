# genai-path

Phase 1: a Python terminal tool that sends a prompt to OpenAI and prints the answer, token usage, elapsed time, and finish reason.

## Setup (PowerShell)

```powershell
python -m venv .venv
.\.venv\Scripts\Activate.ps1
python -m pip install openai python-dotenv
```

Create a local `.env` file with your own API key:

```dotenv
OPENAI_API_KEY=your_api_key_here
```

The `.env` file and virtual environment are excluded from Git. API requests require available API credits.

## Usage

```powershell
python llm_chat.py "Explain a hash map in two sentences."
python llm_chat.py "Explain recursion to a 10-year-old in 3 sentences." --model gpt-4o-mini
python llm_chat.py "Explain how the internet works." --max-tokens 20
python llm_chat.py "Explain how the internet works." --max-tokens 400
python llm_chat.py "Tell me a short story." --system "You are a storyteller." --temperature 0.7
```

Options: `--model` (default `gpt-4o-mini`), `--system`, `--temperature` (0 to 2, when supported), and `--max-tokens` (default 1024).

The completion token limit includes reasoning tokens for models that use them. A small budget can produce an empty answer with finish reason `length`; increase the budget or use the default model for short-output exercises.

Answers go to standard output; usage and diagnostic messages go to standard error. A finish reason of `length` means the token limit was reached, while `stop` means the response ended normally.
