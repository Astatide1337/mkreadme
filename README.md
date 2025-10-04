<!-- AUTOGEN:START -->

# mkaireadme

[![License: MIT](https://img.shields.io/badge/License-MIT-yellow.svg)](https://opensource.org/licenses/MIT)

An AI-powered CLI tool to generate professional README.md files using OpenRouter's language models.

## 🔍 Overview

mkaireadme analyzes your project structure and source code to generate comprehensive README.md files tailored to your project. It supports smart updates, custom configuration, and integrates with OpenRouter's diverse model ecosystem.

## 🛠️ Tech Stack

- **Language**: Python 3.9+
- **CLI Framework**: Typer
- **Terminal UI**: Rich
- **AI Provider**: OpenRouter (OpenAI client)
- **Configuration**: YAML (.mkaireadme.yml)
- **Environment**: dotenv
- **File Processing**: pathspec, Pathlib

## 📦 Installation

Install the package using pip:

```bash
pip install mkaireadme
```

## 🚀 Usage

### 1. Initialize Configuration
Create a `.mkaireadme.yml` configuration file:
```bash
mkaireadme init
```

### 2. Set OpenRouter API Key
Configure your API key:
```bash
mkaireadme set-key YOUR_OPENROUTER_API_KEY
```

### 3. Explore Available Models
List recommended models or search specific ones:
```bash
# Show recommended models
mkaireadme models

# Search for models
mkaireadme models llama
```

### 4. Generate README
Create or update your project's README:
```bash
# Basic generation
mkaireadme gen --model google/gemini-flash-1.5

# Force overwrite existing README
mkaireadme gen --model anthropic/claude-3-haiku --force-overwrite

# Enable debug output
mkaireadme gen --model mistralai/mistral-7b-instruct --debug
```

## ⚙️ Configuration

Edit `.mkaireadme.yml` to customize README generation:
```yaml
project_goals: "A Python CLI tool for generating professional README files"
custom_instructions: "Emphasize AI integration and cross-platform compatibility"
exclude:
  - "*.tmp"
  - "tests/"
```

## 📖 Features

- **Smart Updates**: Preserves custom content between generations using HTML markers
- **Project Analysis**: Reads source files (Python, JS, TOML, etc.) for context
- **Model Flexibility**: Compatible with all OpenRouter-supported models
- **Git Integration**: Respects .gitignore patterns
- **Error Handling**: Robust API error management with user-friendly messages

## 🤝 Contributing

Contributions are welcome! Please follow these steps:
1. Fork the repository
2. Create a feature branch (`git checkout -b feature/amazing-feature`)
3. Commit your changes (`git commit -m 'Add amazing feature'`)
4. Push to the branch (`git push origin feature/amazing-feature`)
5. Open a Pull Request

## 📄 License

This project is licensed under the MIT License - see the [LICENSE](LICENSE) file for details.

## 🔗 Links

- [OpenRouter API](https://openrouter.ai/docs)
- [Typer Documentation](https://typer.tiangolo.com/)
- [Rich Library](https://rich.readthedocs.io/)

<!-- AUTOGEN:END -->