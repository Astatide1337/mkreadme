
<div align="center">

# mkaireadme

**An AI-powered CLI to generate professional README.md files in seconds.**

</div>

<div align="center">

[![PyPI Version](https://img.shields.io/pypi/v/mkaireadme.svg?style=for-the-badge&logo=pypi&color=blue)](https://pypi.org/project/mkaireadme/)
[![Python Versions](https://img.shields.io/pypi/pyversions/mkaireadme.svg?style=for-the-badge&logo=python&color=blue)](https://pypi.org/project/mkaireadme/)
[![License: MIT](https://img.shields.io/badge/License-MIT-yellow.svg?style=for-the-badge)](https://opensource.org/licenses/MIT)
[![Code style: black](https://img.shields.io/badge/code%20style-black-000000.svg?style=for-the-badge)](https://github.com/psf/black)

</div>

<br>

`mkaireadme` is a cross-platform Python CLI that leverages the power of generative AI to create and maintain high-quality `README.md` files for any project. Stop writing documentation from scratch—let your code speak for itself.

---

### ✨ Visual Demo

<div align="center">

![Demo Image - a code block showing the tool in action](httpss://user-images.githubusercontent.com/your-image-url.png) 
*A placeholder for a real GIF, the code block below simulates the experience.*

</div>

```bash
# Navigate to your project directory
$ cd my-awesome-project

# Run the generation command
$ mkaireadme gen --model google/gemini-flash-1.5

🤖 Analyzing project context...
🧠 Contacting google/gemini-flash-1.5 via OpenRouter...
📝 Writing README.md...

✅ Successfully created README.md!
```

---

## 📋 Table of Contents

- [Features](#-key-features)
- [Tech Stack](#-tech-stack)
- [Installation](#-installation)
- [Getting Started](#-getting-started)
- [Command Reference](#-command-reference)
- [Configuration](#-configuration)
- [Contributing](#-contributing)
- [License](#-license)

## ✨ Key Features

-   🧠 **AI-Powered Generation**: Uses state-of-the-art language models (via OpenRouter) to analyze your project and generate a tailored, comprehensive README.
-   🌐 **Cross-Platform Compatibility**: Works seamlessly on Windows, macOS, and Linux.
-   🔄 **Smart Updates**: Intelligently updates existing READMEs by injecting new content between markers, preserving your custom sections.
-   🛠️ **Deep Customization**: Guide the AI with a simple `.mkaireadme.yml` file to specify project goals and custom instructions.
-   📜 **License Management**: Includes built-in license generation (from a list of common templates) and automatic README integration.
-   🤖 **Flexible Model Selection**: Browse and choose from dozens of AI models to find the perfect fit for your needs and budget.
-   💰 **Content Budgeting**: Smartly analyzes large projects by prioritizing key files, ensuring you stay within the AI model's token limits.

## 🛠️ Tech Stack

-   **Python 3.9+**
-   **Typer**: Modern CLI framework for a great user experience.
-   **Rich**: Beautiful terminal styling, tables, and progress indicators.
-   **OpenAI**: Official library for robust AI integration via OpenRouter.
-   **python-dotenv**: Secure environment variable management.
-   **pathspec**: Gitignore-style file exclusion for precise context analysis.
-   **PyYAML**: Simple and clean configuration file handling.

## 🚀 Installation

Install `mkaireadme` directly from PyPI with a single command:

```bash
pip install mkaireadme
```

## 🏁 Getting Started

Get your first AI-generated README in just 3 simple steps.

### Step 1: Set Your API Key

The tool requires an API key from [OpenRouter](https://openrouter.ai/keys) to function. Set it once, and it will be saved locally for all future use.

```bash
mkaireadme set-key YOUR_OPENROUTER_API_KEY```

### Step 2: Create a License (Recommended)

A `LICENSE` file is crucial for any serious project. `mkaireadme` can create one for you.

```bash
mkaireadme license
```
This will prompt you to choose from a list of popular open-source licenses.

### Step 3: Generate Your README!

Navigate to your project's root directory and run the `gen` command.

```bash
# Use the recommended Gemini Flash model
mkaireadme gen --model google/gemini-flash-1.5
```

That's it! Your new `README.md` is ready. To update it later after making changes to your project, just run the same command again.

## 📚 Command Reference

### `gen`
The core command to generate or update the README.

| Option              | Description                                                    | Example                                     |
| :------------------ | :------------------------------------------------------------- | :------------------------------------------ |
| `--model`           | **(Required)** The AI model to use.                            | `anthropic/claude-3-haiku`                  |
| `--force-overwrite` | Replace the entire README, ignoring update markers.            | `--force-overwrite`                         |
| `--debug`           | Enable verbose logging for troubleshooting.                    | `--debug`                                   |

### `models`
Browse and search for available AI models on OpenRouter.

```bash
# Show a list of recommended models
mkaireadme models

# Search for a specific model provider or name
mkaireadme models llama
```

### `license`
An interactive command to generate a `LICENSE` file for your project.

### `set-key`
Securely saves your OpenRouter API key for future use.

## ⚙️ Configuration

For more control over the AI's output, create a `.mkaireadme.yml` file in your project's root directory.

```yaml
# .mkaireadme.yml

# Provide high-level goals to guide the AI's description
project_goals: "To build a fast, lightweight, and user-friendly CLI tool for automating documentation."

# Give specific instructions to include in the AI prompt
custom_instructions: "Emphasize the cross-platform compatibility. Mention that it is open-source and contributions are welcome."

# Exclude files or directories from the analysis to save tokens
exclude:
  - "docs/"
  - "tests/"
  - "*.log"
  - "dist/"
```

## 🤝 Contributing

Contributions are welcome! Whether it's a bug report, a feature request, or a pull request, your input is valued. Please feel free to open an issue to discuss your ideas.

## 📜 License

This project is licensed under the MIT License - see the [LICENSE](LICENSE) file for details.