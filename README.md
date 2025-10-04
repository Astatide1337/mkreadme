<div align="center">
  <br />
    <a href="https://pypi.org/project/mkaireadme/"><img src="https://i.imgur.com/L1p2s2u.png" alt="Logo" width="120"></a>
  <br />

  <h1 align="center">mkaireadme</h1>

  <p align="center">
    An intelligent CLI that uses AI to write your project's README, so you don't have to.
    <br />
    <a href="#-features"><strong>Explore the features »</strong></a>
    <br />
    <br />
    <a href="https://github.com/your-username/mkaireadme/issues">Report Bug</a>
    ·
    <a href="https://github.com/your-username/mkaireadme/issues">Request Feature</a>
  </p>
</div>

<p align="center">
  <a href="https://pypi.org/project/mkaireadme/"><img alt="PyPI Version" src="https://badge.fury.io/py/mkaireadme.svg"></a>
  <a href="https://opensource.org/licenses/MIT"><img alt="License: MIT" src="https://img.shields.io/badge/License-MIT-yellow.svg"></a>
  <a href="https://pypi.org/project/mkaireadme/"><img alt="PyPI - Python Version" src="https://img.shields.io/pypi/pyversions/mkaireadme"></a>
  <a href="https://github.com/psf/black"><img alt="Code style: black" src="https://img.shields.io/badge/code%20style-black-000000.svg"></a>
</p>

---

`mkaireadme` is a cross-platform Python CLI tool that leverages state-of-the-art AI to instantly craft professional `README.md` files.

By analyzing your project's structure and source code, it connects to language models via the OpenRouter API to generate comprehensive, well-structured documentation—allowing you to focus on coding, not writing.

### ✨ Key Benefits

*   **Save Time:** Go from a complex project to a beautiful README in seconds.
*   **Improve Quality:** Leverage powerful AI to write clearer, more comprehensive documentation than you would by hand.
*   **Ensure Consistency:** Maintain a professional and standardized format across all your projects.

##  Demo

Here's a quick look at the tool in action, from initialization to a fully generated README:



## 🚀 Getting Started

Getting started with `mkaireadme` is a simple, two-step process.

### 1. Installation

Install the package directly from PyPI:```bash
pip install mkaireadme
```

### 2. Set Your API Key

The tool requires an API key from [OpenRouter](https://openrouter.ai/) to function. OpenRouter provides access to a wide variety of AI models.

```bash
# Replace YOUR_API_KEY with your actual key from openrouter.ai
mkaireadme set-key sk-or-v1-xxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxx
```

## 🛠️ Usage

Once installed and configured, you can generate and manage your documentation with a few simple commands.

### Main Command: `gen`

This is the core command that generates or updates your `README.md`.

```bash
# Generate a README using a recommended fast and capable model
mkaireadme gen --model google/gemini-flash-1.5
```
> **Note:** The first time you run `gen`, it creates a new `README.md`. Subsequent runs will intelligently update the file, preserving any custom content you've added outside of the special `<!-- MKAIR-START -->` and `<!-- MKAIR-END -->` markers.

**Common Options:**
*   `--model`: Specify which AI model to use (e.g., `anthropic/claude-3-haiku`, `mistralai/mistral-7b-instruct`). Use `mkaireadme models` to see your options.
*   `--force-overwrite`: Completely replace the existing `README.md` instead of performing a smart update.
*   `--debug`: Enable verbose logging for troubleshooting.

### Utility Commands

#### `init`
Initializes the project by creating a `.mkaireadme.yml` configuration file. This is where you can provide custom instructions to the AI.
```bash
mkaireadme init
```

#### `license`
An interactive command to generate a `LICENSE` file (e.g., MIT, Apache 2.0) and automatically link it in your README.
```bash
mkaireadme license
```

#### `models`
Browse and search for compatible AI models available through OpenRouter.
```bash
# Show a list of recommended models
mkaireadme models

# Search for models by name
mkaireadme models llama
```

## ⚙️ Configuration

For more fine-grained control, create a `.mkaireadme.yml` file in your project's root directory (or run `mkaireadme init`).

```yaml
# .mkaireadme.yml

# High-level goals to guide the AI's description
project_goals: "Build a scalable, real-time chat application using FastAPI and WebSockets."

# Specific instructions for the AI to follow
custom_instructions: "Emphasize the low-latency features and include an example of the WebSocket API. Do not mention the database structure."

# Gitignore-style patterns to exclude files/directories from analysis
exclude:
  - "tests/"
  - "*.log"
  - "notebooks/experimental.ipynb"
```

## 💻 Tech Stack

`mkaireadme` is built with a modern, robust set of Python tools:

*   **Core:** Python 3.9+
*   **CLI Framework:** Typer & Rich
*   **AI Integration:** OpenAI API client (for OpenRouter)
*   **Configuration:** PyYAML & python-dotenv
*   **File Handling:** pathspec
*   **Tooling:** build & twine

## 📄 License

This project is licensed under the MIT License - see the [LICENSE](LICENSE) file for details.