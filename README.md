<!-- AUTOGEN:START -->
# mkaireadme

[![Python Version](https://img.shields.io/badge/python-3.9+-blue.svg)](https://python.org)
[![License: MIT](https://img.shields.io/badge/License-MIT-yellow.svg)](https://opensource.org/licenses/MIT)
[![Platform](https://img.shields.io/badge/Platform-Windows%20%7C%20macOS%20%7C%20Linux-green.svg)](https://github.com/gemini-cli/mkaireadme)

An AI-powered CLI tool that generates professional README.md files by analyzing your project structure and code.

## ✨ Features

- 🤖 **AI Integration**: Powered by OpenRouter's diverse model ecosystem (Google Gemini, Anthropic Claude, Mistral, Llama, GPT)
- 📁 **Smart Analysis**: Intelligently examines your project directory respecting `.gitignore` and custom exclusions
- ⚙️ **Configuration-Driven**: Use `.mkaireadme.yml` to provide project goals and custom instructions
- 🔄 **Smart Updates**: Intelligently preserves existing content when updating READMEs
- 🎨 **Rich Output**: Beautiful terminal UI with progress indicators and formatted output
- 🔄 **Cross-Platform**: Works seamlessly on Windows, macOS, and Linux

## 🛠️ Tech Stack

- **Core**: Python 3.9+
- **CLI Framework**: Typer
- **UI Library**: Rich
- **AI Client**: OpenAI (for OpenRouter API)
- **Configuration**: PyYAML, python-dotenv
- **File Handling**: pathspec
- **Deployment**: Setuptools, Twine

## 📦 Installation

### Prerequisites
- Python 3.9 or higher
- OpenRouter API key (get one at [openrouter.ai](https://openrouter.ai/keys))

### Install from PyPI
```bash
pip install mkaireadme
```

### Install from Source
```bash
git clone https://github.com/gemini-cli/mkaireadme.git
cd mkaireadme
pip install -e .
```

## 🚀 Usage

### 1. Set Your API Key
```bash
mkaireadme set-key YOUR_OPENROUTER_API_KEY
```

### 2. Initialize Configuration (Optional)
Creates a `.mkaireadme.yml` file to guide AI generation:
```bash
mkaireadme init
```

Edit `.mkaireadme.yml` to add:
```yaml
project_goals: "Build a cross-platform task automation tool"
custom_instructions: "Focus on security features and Windows compatibility"
exclude:
  - "*.log"
  - "tests/"
```

### 3. Generate README
Generate a new README or update an existing one:
```bash
# Basic generation with recommended model
mkaireadme gen --model google/gemini-flash-1.5

# Force overwrite existing README
mkaireadme gen --model meta-llama/llama-3-8b-instruct --force-overwrite

# Enable debug mode
mkaireadme gen --model mistralai/mistral-7b-instruct --debug
```

### 4. Browse Available Models
List recommended models or search for specific ones:
```bash
# Show recommended models
mkaireadme models

# Search for specific models
mkaireadme models llama
mkaireadme models claude
```

## 📋 Command Reference

| Command          | Description                                                                 |
|------------------|-----------------------------------------------------------------------------|
| `set-key`        | Save your OpenRouter API key securely                                       |
| `init`           | Create `.mkaireadme.yml` configuration file                                |
| `gen`            | Generate/update README.md                                                  |
| `models`         | List/search available models on OpenRouter                                  |

### `gen` Options
| Option          | Description                                                  | Default   |
|-----------------|--------------------------------------------------------------|-----------|
| `--model`       | Model ID to use for generation                               | Required  |
| `--force-overwrite` | Overwrite existing README without autogen markers          | `False`   |
| `--debug`       | Enable debug output and detailed analysis                    | `False`   |

## 🤝 Contributing

We welcome contributions! Please see our [Contributing Guide](CONTRIBUTING.md) for details on:
- Setting up your development environment
- Submitting pull requests
- Reporting bugs

## 📄 License

This project is licensed under the MIT License - see the [LICENSE](LICENSE) file for details.

## 🙏 Acknowledgments

- Built with [Typer](https://typer.tiangolo.com/) for the CLI interface
- Terminal UI powered by [Rich](https://github.com/Textualize/rich)
- AI capabilities provided by [OpenRouter](https://openrouter.ai/)
- Inspired by the need for better project documentation automation

---

**mkaireadme** - Because great documentation shouldn't be hard to write.

<!-- AUTOGEN:END -->