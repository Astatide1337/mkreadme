<!-- AUTOGEN:START -->

```markdown
# My Awesome Project

A custom description for my project.

## Tech Stack & Key Features

- **Tech Stack**: Python 3.13+, Typer (CLI framework), Rich (terminal styling), OpenAI (LLM integration), PathSpec (file pattern matching), python-dotenv (environment management), Jinja2 (templating), Shellingham (shell command detection)
- **Key Features**:
  - Securely store OpenRouter API keys
  - Search and browse LLM models
  - Generate professional README files from project analysis
  - Smart README updates with AUTOGEN markers
  - Force overwrite option for custom READMEs
  - Debug mode for context analysis

## Prerequisites & Installation

**Prerequisites**:
- Python 3.13 or higher
- OpenRouter API key

**Installation**:
1. Clone the repository
2. Install dependencies:
   ```bash
   pip install -e .
   ```
   or using uv:
   ```bash
   uv pip install -e .
   ```

## Usage

1. **Set API Key**:
   ```bash
   python main.py set-key YOUR_OPENROUTER_API_KEY
   ```

2. **Browse Models**:
   ```bash
   python main.py models  # Shows recommended models
   python main.py models llama  # Search for specific models
   ```

3. **Generate README**:
   ```bash
   python main.py gen --model google/gemini-flash-1.5
   ```

   Options:
   - `--model`: LLM model ID (required)
   - `--force-overwrite`: Replace entire README (existing content not preserved)
   - `--debug`: Show project analysis details

## Project File Structure

```
├── .autoreadme.yml      # Project configuration
├── .env                 # Environment variables (API key storage)
├── .gitignore           # Git ignore rules
├── .python-version      # Python version specification
├── main.py              # CLI application entry point
├── PRD.txt              # Product requirements document
├── pyproject.toml       # Project metadata and dependencies
├── templates/           # Jinja2 template directory
└── uv.lock              # UV dependency lock file
```

[![pylint](https://img.shields.io/badge/pylint-10.0-yellow.svg)](https://www.pylint.org/)
```

<!-- AUTOGEN:END -->