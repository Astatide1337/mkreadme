<!-- AUTOGEN:START -->
# mkaireadme

An AI-powered CLI to generate professional README.md files.

## Description

mkaireadme is a cross-platform Python CLI tool that leverages artificial intelligence to create and maintain high-quality README.md files. By analyzing your project structure and source code, it generates comprehensive documentation with sections for project goals, tech stack, installation, usage, and more. The tool integrates with OpenRouter's API to access state-of-the-art language models, ensuring professional-grade documentation for any project.

## Features

- **AI-Powered Generation**: Uses advanced language models (OpenRouter) to analyze project context and generate tailored READMEs
- **Cross-Platform Compatibility**: Works seamlessly on Windows, macOS, and Linux
- **Smart Updates**: Intelligently updates existing READMEs while preserving custom content
- **Customization**: Supports project-specific guidance through configuration files
- **License Management**: Includes built-in license generation and README integration
- **Model Selection**: Browse and choose from multiple AI models
- **Content Budgeting**: Efficiently analyzes large projects within token limits

## Tech Stack

- **Python 3.9+**
- **Typer**: Modern CLI framework
- **Rich**: Terminal styling and formatting
- **OpenAI**: AI integration via OpenRouter
- **python-dotenv**: Environment variable management
- **pathspec**: Gitignore-style file exclusion
- **PyYAML**: Configuration file handling
- **requests**: HTTP library for license API
- **build**: Package building utilities
- **twine**: Package publishing utilities

## Installation

Install directly from PyPI:

```bash
pip install mkaireadme
```

## Usage

### Setup
1. Set your OpenRouter API key:
   ```bash
   mkaireadme set-key YOUR_OPENROUTER_API_KEY
   ```

2. Initialize project configuration (optional):
   ```bash
   mkaireadme init
   ```

3. Generate or update LICENSE (recommended):
   ```bash
   mkaireadme license
   ```

### Commands

#### Generate README
```bash
mkaireadme gen --model google/gemini-flash-1.5
```

Options:
- `--model`: AI model to use (e.g., `google/gemini-flash-1.5`, `anthropic/claude-3-haiku`)
- `--force-overwrite`: Replace existing README without markers
- `--debug`: Enable verbose logging

#### Browse AI Models
```bash
# Show recommended models
mkaireadme models

# Search for specific models
mkaireadme models llama
```

#### License Management
```bash
mkaireadme license
```

## Example Workflow

1. Set API key:
   ```bash
   mkaireadme set-key sk-or-xxxx
   ```

2. Create license:
   ```bash
   mkaireadme license
   ```

3. Generate README:
   ```bash
   mkaireadme gen --model google/gemini-flash-1.5
   ```

4. Update README later (adds new content between markers):
   ```bash
   mkaireadme gen --model anthropic/claude-3-haiku
   ```

## Configuration

Create `.mkaireadme.yml` in your project root:
```yaml
project_goals: "Build a scalable web application"
custom_instructions: "Include performance benchmarks"
exclude:
  - "test/"
  - "*.log"
```

## License

This project is licensed under the MIT License - see the [LICENSE](LICENSE) file for details.

<!-- AUTOGEN:END -->