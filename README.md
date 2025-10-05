<!-- AUTOGEN:START -->

n
<p align="center">
  <h1>mkaireadme</h1>
  <p>An AI-powered CLI to generate professional README.md files.</p>
  <p align="center">
    <a href="https://badge.fury.io/py/mkaireadme"><img src="https://badge.fury.io/py/mkaireadme.svg" alt="PyPI version"></a>
    <a href="https://www.python.org"><img src="https://img.shields.io/badge/python-3.9+-blue.svg" alt="Python Version"></a>
    <a href="https://github.com/gemini-cli/mkaireadme/blob/main/LICENSE"><img src="https://img.shields.io/badge/License-MIT-yellow.svg" alt="License: MIT"></a>
    <a href="https://openrouter.ai"><img src="https://img.shields.io/badge/OpenRouter-API-orange" alt="OpenRouter API"></a>
  </p>
</p>

---

## 🚀 Key Features

- 🤖 **AI-Powered Generation**: Leverages OpenRouter's AI models to create professional, context-aware README files
- 🔄 **Smart Updates**: Intelligently updates existing READMEs using special markers without overwriting custom content
- 🔒 **Secure API Management**: Securely store and manage your OpenRouter API keys
- 📁 **Project Analysis**: Automatically analyzes your project structure and source code to generate relevant documentation
- 🛠️ **Built-in Tools**: Includes commands for license generation, model discovery, and configuration management

---

## 💡 Installation

```bash
pip install mkaireadme
```

> **Note**: Requires Python 3.9 or higher

---

## 📖 Usage

### Getting Started
```bash
# Set your OpenRouter API key
mkaireadme set-key YOUR_API_KEY

# Initialize a configuration file
mkaireadme init

# Generate a README
mkaireadme gen --model google/gemini-flash-1.5
```

### Key Commands
```bash
# Generate README with specific model
mkaireadme gen --model anthropic/claude-3-haiku

# Force overwrite existing README
mkaireadme gen --force-overwrite

# List available AI models
mkaireadme models

# Create a LICENSE file
mkaireadme license

# Enable debug output
mkaireadme gen --debug
```

---

## 🔧 Tech Stack

- **Python 3.9+**: Core language
- **Typer**: CLI framework
- **Rich**: Beautiful terminal output
- **OpenAI**: Client for OpenRouter API
- **python-dotenv**: Environment variable management
- **pathspec**: Gitignore pattern parsing
- **PyYAML**: Configuration file handling
- **requests**: License template fetching

---

## ⚙️ Configuration

Create a `.mkaireadme.yml` file to guide AI generation:

```yaml
# Project-specific goals
project_goals: "A Python CLI tool for generating professional README files"

# Custom instructions for AI
custom_instructions: "Emphasize AI integration and cross-platform compatibility"

# Files/directories to exclude
exclude:
  - "docs/"
  - "*.log"
  - "tests/"
```

---

## 🤝 Contributing

Contributions are welcome! Please feel free to submit a Pull Request. For major changes, please open an issue first to discuss what you would like to change.

---

## 📄 License

This project is licensed under the MIT License - see the [LICENSE](LICENSE) file for details.

---

## 👨‍💻 Contact

Soham Bhagat - bhagatsoham14@gmail.com  
Project Link: [https://github.com/gemini-cli/mkaireadme](https://github.com/gemini-cli/mkaireadme)

<!-- AUTOGEN:END -->