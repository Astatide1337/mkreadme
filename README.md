<!-- AUTOGEN:START -->

```markdown
# mkaireadme

[![License: MIT](https://img.shields.io/badge/License-MIT-yellow.svg)](https://opensource.org/licenses/MIT)  
[![Python](https://img.shields.io/badge/Python-3.9+-blue.svg)](https://www.python.org/downloads/)  
[![Typer](https://img.shields.io/badge/Typer-0.12.0-green.svg)](https://typer.tiangolo.com/)  
[![Rich](https://img.shields.io/badge/Rich-13.7.0-purple.svg)](https://github.com/Textualize/rich)

An AI-powered CLI tool to generate professional README.md files using OpenRouter's language models.

## Features
- 🤖 AI-driven README generation from project analysis
- ⚙️ Configurable via `.mkaireadme.yml` for custom instructions
- 🔄 Smart updates with `AUTOGEN` markers for existing READMEs
- 🔒 Secure API key management with `.env` integration
- 🚫 Exclusion patterns for sensitive files (respects `.gitignore`)
- 📊 Rich terminal output with status indicators and error handling
- 🔍 Model discovery and listing

## Tech Stack
- **Language**: Python 3.9+
- **CLI Framework**: Typer
- **Terminal UI**: Rich
- **AI Provider**: OpenRouter
- **Configuration**: YAML
- **Environment Management**: python-dotenv
- **File Pattern Matching**: pathspec

## Installation
```bash
pip install mkaireadme
```

## Quick Start
1. **Set API Key**:
   ```bash
   mkaireadme set-key YOUR_OPENROUTER_API_KEY
   ```

2. **Initialize Configuration** (optional):
   ```bash
   mkaireadme init
   ```

3. **Generate README**:
   ```bash
   mkaireadme gen --model google/gemini-flash-1.5
   ```

## Commands

### `init`
Create a `.mkaireadme.yml` configuration file to guide AI generation:
```bash
mkaireadme init
```

### `set-key`
Securely store your OpenRouter API key:
```bash
mkaireadme set-key YOUR_API_KEY
```

### `models`
List recommended models or search by keyword:
```bash
# Show recommended models
mkaireadme models

# Search for specific models
mkaireadme models claude
mkaireadme models llama
```

### `gen`
Generate or update a README.md file:
```bash
# Basic generation
mkaireadme gen --model google/gemini-flash-1.5

# Force overwrite existing README
mkaireadme gen --model google/gemini-flash-1.5 --force-overwrite

# Enable debug output
mkaireadme gen --model google/gemini-flash-1.5 --debug
```

## Configuration
Create `.mkaireadme.yml` to customize AI behavior:
```yaml
# Project goals for better descriptions
project_goals: "A scalable microservice for real-time analytics"

# Custom instructions
custom_instructions: "Focus on security features and deployment"

# Files/directories to exclude
exclude:
  - "*.test"
  - "temp/"
```

## Smart Update Behavior
The tool preserves existing content using special markers:
```markdown

Generated AI content here


Your custom content here
```

## Error Handling
- **Missing API Key**: Clear prompt to run `set-key`
- **Authentication Errors**: Validates API credentials
- **Rate Limiting**: Automatic retries with backoff
- **Safety Filters**: Guides users to alternative models
- **File Permissions**: Handles read/write errors gracefully

## Contributing
1. Fork the repository
2. Create a feature branch
3. Commit your changes
4. Submit a pull request

## License
This project is licensed under the MIT License - see the [LICENSE](LICENSE) file for details.

## Acknowledgments
- [OpenRouter](https://openrouter.ai/) for AI model access
- [Typer](https://typer.tiangolo.com/) for CLI framework
- [Rich](https://github.com/Textualize/rich) for terminal enhancements
- [PathSpec](https://github.com/cpburnz/python-pathspec) for pattern matching
```

<!-- AUTOGEN:END -->

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