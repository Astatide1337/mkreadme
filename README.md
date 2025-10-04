<!-- AUTOGEN:START -->

```markdown
# mkaireadme

[![License: MIT](https://img.shields.io/badge/License-MIT-yellow.svg)](https://opensource.org/licenses/MIT)
![Python](https://img.shields.io/badge/Python-3.9+-blue.svg)
![Typer](https://img.shields.io/badge/CLI-Typer-green.svg)

An AI-powered CLI tool that generates professional README.md files for your software projects using advanced language models.

## Features

- 🤖 AI-driven content generation using OpenRouter models
- 📁 Smart project analysis (scans directory structure and key files)
- 🛠️ Customizable configuration via `.mkaireadme.yml`
- 🔒 Secure API key management with `.env`
- 🔄 Smart README updates with auto-gen markers
- 🎨 Rich terminal output for better UX
- ⚙️ Supports multiple AI models (search and browse options)

## Tech Stack

- **Language**: Python 3.9+
- **CLI Framework**: Typer
- **Terminal UI**: Rich
- **AI Integration**: OpenAI (OpenRouter)
- **Configuration**: YAML
- **File Handling**: pathspec
- **Environment Management**: python-dotenv

## Installation

```bash
pip install mkaireadme
```

## Usage

### 1. Initialize Configuration
Create a `.mkaireadme.yml` file to guide AI content generation:
```bash
mkaireadme init
```

### 2. Set API Key
Configure your OpenRouter API key:
```bash
mkaireadme set-key YOUR_OPENROUTER_API_KEY
```

### 3. Browse AI Models
List recommended models or search for specific ones:
```bash
# Show recommended models
mkaireadme models

# Search for models (e.g., "llama", "claude")
mkaireadme models llama
```

### 4. Generate README
Create or update your `README.md`:
```bash
# Generate with default settings
mkaireadme gen --model google/gemini-flash-1.5

# Force overwrite existing README
mkaireadme gen --model meta-llama/llama-3-8b-instruct --force-overwrite

# Enable debug output
mkaireadme gen --model anthropic/claude-3-haiku --debug
```

## Configuration

### `.mkaireadme.yml`
```yaml
# Project goals for AI guidance
project_goals: "Build a scalable microservice with Python"

# Custom instructions for content generation
custom_instructions: "Focus on deployment section"

# Files/directories to exclude from analysis
exclude:
  - "*.log"
  - "tests/"
```

### Auto-Gen Markers
For smart updates, add these markers to your existing README:
```markdown

[AI-generated content]

```

## Contributing

1. Fork the repository
2. Create your feature branch: `git checkout -b feature-name`
3. Commit your changes: `git commit -am 'Add feature'`
4. Push to the branch: `git push origin feature-name`
5. Submit a pull request

## License

This project is licensed under the MIT License - see the [LICENSE](LICENSE) file for details.

## Support

- **Issues**: [GitHub Issues](https://github.com/gemini-cli/mkaireadme/issues)
- **Documentation**: [Wiki](https://github.com/gemini-cli/mkaireadme/wiki)
- **OpenRouter Signup**: [OpenRouter.ai](https://openrouter.ai/keys)

---

Made with ❤️ by [Soham Bhagat](https://github.com/gemini-cli)
```

<!-- AUTOGEN:END -->