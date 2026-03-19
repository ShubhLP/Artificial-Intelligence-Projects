# TaskRunnerAI

**TaskRunnerAI** is an AI-powered agent that can interact with files, execute Python scripts, and assist in automating tasks. It is designed to reason over multiple steps, call functions safely, and provide useful outputs in response to user prompts.

---

## Features

- Read and list files in directories
- Retrieve the contents of text files
- Write content to new files without overwriting existing ones
- Execute Python scripts and report results
- Keep conversation history and track function calls for iterative reasoning
- Verbose mode for detailed logging and debugging

---

## Getting Started

### Prerequisites

- Python 3.10+
- An API key for Gemini or your AI provider stored in a `.env` file:

```env
GEMINI_API_KEY=your_api_key_here
```

## Example Usage

python main.py "Explain how the calculator renders the result to the console." --verbose
python main.py "get the contents of lorem.txt" --verbose
python main.py 'create a new README.md file with content "# calculator"'
python main.py "run tests.py"
python main.py "what files are in the root?"

## Recommended: use a virtual environment:
python -m venv .venv
source .venv/bin/activate  # macOS/Linux
.venv\Scripts\activate     # Windows
pip install -r requirements.txt
