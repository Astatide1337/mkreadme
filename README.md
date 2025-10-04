<!-- AUTOGEN:START -->

```markdown
# mkaireadme

## Description
mkaireadme is an AI-powered CLI tool that generates professional README.md files for software projects. It analyzes your project structure, key files, and configuration to create tailored documentation using advanced language models via OpenRouter. The tool supports smart updates, preserving custom content while regenerating AI-generated sections.

## Tech Stack
- **Python 3.9+**  
- **Typer** - CLI framework
- **Rich** - Enhanced terminal output
- **OpenAI** - API client for OpenRouter
- **python-dotenv** - Environment variable management
- **pathspec** - Gitignore pattern matching
- **PyYAML** - Configuration file handling

## Installation
Install via pip:
```bash
pip install mkaireadme
```

Or from source:
```bash
git clone https://github.com/gemini-cli/mkaireadme.git
cd mkaireadme
pip install .
```

## Usage
### Setup
1. Initialize configuration:
```bash
mkaireadme init
```
   Creates `.mkaireadme.yml` for AI guidance.

2. Set API key:
```bash
mkaireadme set-key YOUR_OPENROUTER_API_KEY
```

### Commands
- **Generate README**:
  ```bash
  mkaireadme gen --model google/gemini-flash-1.5
  ```
  Options:
  - `--model`: Specify AI model (use `mkaireadme models` to see options)
  - `--force-overwrite`: Override existing README without markers
  - `--debug`: Enable verbose output

- **List Models**:
  ```bash
  mkaireadme models  # Show recommended models
  mkaireadme models llama  # Search for models
  ```

### Generated README Behavior
- Creates `README.md` with auto-generated content wrapped in `` and `` markers
- Preserves custom content outside markers during updates
- Analyzes project structure, key files (Python, JS, TOML, etc.), and `.gitignore` patterns
- Leverages `.mkaireadme.yml` for project-specific guidance and exclusions

### Example Workflow
```bash
# 1. Setup
mkaireadme init
mkaireadme set-key sk-or-xxxxxx

# 2. Explore models
mkaireadme models

# 3. Generate README
mkaireadme gen --model openai/gpt-4o-mini

# 4. Edit generated sections in README.md
# 5. Update README later (preserves custom edits)
mkaireadme gen --model google/gemini-flash-1.5
```

## Configuration
Edit `.mkaireadme.yml` to:
- Define project goals
- Provide custom instructions
- Specify file/directory exclusions
```yaml
project_goals: "Build scalable REST APIs"
custom_instructions: "Emphasize security features"
exclude:
  - tests/
  - *.log
```

<!-- AUTOGEN:END -->