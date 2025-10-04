import typer
from rich.console import Console
from rich.panel import Panel
from rich.table import Table
import os
from pathlib import Path
import pathspec
from openai import OpenAI, AuthenticationError, RateLimitError, NotFoundError
from dotenv import load_dotenv, set_key as dotenv_set_key

# --- Configuration ---
app = typer.Typer()
console = Console()
dotenv_path = Path(".env")
# ---


def load_api_key():
    """Loads the .env file and returns the OpenRouter API key."""
    load_dotenv(dotenv_path=dotenv_path)
    return os.getenv("OPENROUTER_API_KEY")


def create_openrouter_client(api_key: str) -> OpenAI:
    """Creates and configures an OpenAI client for OpenRouter."""
    return OpenAI(
        base_url="https://openrouter.ai/api/v1",
        api_key=api_key,
        default_headers={
            "HTTP-Referer": "https://github.com/gemini-cli/readme-cli",
            "X-Title": "AutoReadMe CLI",
        },
    )


@app.command()
def set_key(api_key: str = typer.Argument(..., help="Your OpenRouter API key.")):
    """
    Saves your OpenRouter API key securely to a .env file.
    """
    dotenv_set_key(dotenv_path, "OPENROUTER_API_KEY", api_key)
    console.print("✅ [bold green]OpenRouter API Key saved successfully![/bold green]")


@app.command()
def models(
    search: str = typer.Argument(None, help="An optional term to search for models.")
):
    """
    Lists recommended models or searches for a specific model.
    """
    api_key = load_api_key()
    if not api_key:
        console.print(
            Panel(
                "[bold]No API Key Found[/bold]\n\nPlease set your key first: [cyan]python main.py set-key YOUR_KEY[/cyan]",
                title="[yellow]Action Required[/yellow]",
                border_style="red",
            )
        )
        raise typer.Exit()

    client = create_openrouter_client(api_key)

    recommended_models = [
        "google/gemini-flash-1.5",
        "anthropic/claude-3-haiku",
        "mistralai/mistral-7b-instruct",
        "meta-llama/llama-3-8b-instruct",
        "openai/gpt-4o-mini",
    ]

    if not search:
        console.print(
            Panel(
                "Showing a few recommended models. To see more, search for a term like 'llama', 'claude', or 'gemma'.\nExample: [cyan]python main.py models llama[/cyan]",
                title="[green]Recommended Models[/green]",
            )
        )
        table = Table(show_lines=True)
        table.add_column("Recommended Model ID", style="cyan")
        for model_id in recommended_models:
            table.add_row(model_id)
        console.print(table)
        return

    with console.status(f"[bold green]Searching for models matching '{search}'..."):
        try:
            model_list = client.models.list().data
            model_ids = sorted([model.id for model in model_list])

            filtered_models = [m for m in model_ids if search.lower() in m.lower()]

            if not filtered_models:
                console.print(f"[yellow]No models found matching '{search}'.[/yellow]")
                raise typer.Exit()

            table = Table(title=f"Models Matching '{search}'", show_lines=True)
            table.add_column("Model ID", style="cyan")
            for model_id in filtered_models:
                table.add_row(model_id)
            console.print(table)

        except AuthenticationError:
            console.print(
                "[bold red]Authentication Error:[/bold red] Your OpenRouter API key is invalid."
            )
            raise typer.Exit(code=1)
        except Exception as e:
            console.print(f"[bold red]An unexpected error occurred:[/bold red] {e}")
            raise typer.Exit(code=1)


@app.command()
def gen(
    model: str = typer.Option(
        ...,
        "--model",
        help="The model ID to use for generation (e.g., 'google/gemini-flash-1.5').",
    ),
    force_overwrite: bool = typer.Option(
        False,
        "--force-overwrite",
        help="Forcibly overwrite a README.md that has no autogen markers.",
    ),
    debug: bool = typer.Option(
        False, "--debug", help="Enable debug output to see context analysis."
    ),
):
    """
    Generates or smartly updates a professional README.md file for your project.
    """
    # --- Fail Fast Checks ---
    api_key = load_api_key()
    if not api_key:
        console.print(
            Panel(
                "[bold]No API Key Found[/bold]\n\nPlease set your key first: [cyan]python main.py set-key YOUR_KEY[/cyan]",
                title="[yellow]Action Required[/yellow]",
                border_style="red",
            )
        )
        raise typer.Exit()

    readme_path = Path("README.md")
    autogen_start_marker = "<!-- AUTOGEN:START -->"
    autogen_end_marker = "<!-- AUTOGEN:END -->"

    # Check for custom README without markers
    if readme_path.exists() and not force_overwrite:
        content = readme_path.read_text(encoding="utf-8")
        if autogen_start_marker not in content or autogen_end_marker not in content:
            console.print(
                Panel(
                    "[bold]Custom README.md Detected[/bold]\n\n"
                    "This tool will only modify content between `AUTOGEN` markers to avoid data loss.\n\n"
                    "[bold]What you can do:[/bold]\n"
                    "1. To enable smart updates, add these markers to your `README.md`:\n"
                    f"   [cyan]{autogen_start_marker}[/cyan]\n"
                    f"   [cyan]{autogen_end_marker}[/cyan]\n\n"
                    "2. To replace the entire file, run the command again with the `--force-overwrite` flag.",
                    title="[yellow]Action Required[/yellow]",
                    border_style="red",
                )
            )
            raise typer.Exit()

    # --- Main Logic ---
    client = create_openrouter_client(api_key)

    with console.status("[bold green]🤖 Analyzing project...") as status:
        project_context = analyze_project(Path("."), debug=debug)
        status.update(f"[bold green]🧠 Contacting OpenRouter with model '{model}'...")
        generated_content = generate_readme(client, project_context, model)

    # --- File Writing Logic ---
    try:
        if readme_path.exists():
            # Smart update if markers are present or force_overwrite is used on a custom file
            content = readme_path.read_text(encoding="utf-8")
            if autogen_start_marker in content and autogen_end_marker in content:
                pre_content = content.split(autogen_start_marker)[0]
                post_content = content.split(autogen_end_marker)[1]

                new_content = (
                    pre_content.strip()
                    + f"\n\n{autogen_start_marker}\n\n"
                    + generated_content.strip()
                    + f"\n\n{autogen_end_marker}\n\n"
                    + post_content.strip()
                ).strip()
                readme_path.write_text(new_content, encoding="utf-8")
                console.print(
                    "✅ Successfully updated README.md with new content!",
                    style="bold green",
                )
            else:  # This case is only hit if --force-overwrite was used
                full_content = f"{autogen_start_marker}\n\n{generated_content.strip()}\n\n{autogen_end_marker}"
                readme_path.write_text(full_content, encoding="utf-8")
                console.print(
                    "✅ Successfully overwrote README.md!", style="bold green"
                )
        else:
            # Create new file with markers
            full_content = f"{autogen_start_marker}\n\n{generated_content.strip()}\n\n{autogen_end_marker}"
            readme_path.write_text(full_content, encoding="utf-8")
            console.print("✅ Successfully created README.md!", style="bold green")

    except (IOError, PermissionError) as e:
        console.print(
            f"Error: Could not write to README.md. Please check file permissions.",
            style="bold red",
        )
        raise typer.Exit(code=1)

    console.print("\n--- Generated README.md ---\n", style="bold blue")
    console.print(generated_content)


def generate_readme(client: OpenAI, context: str, model_name: str) -> str:
    """Generates a README file using the OpenRouter API."""
    prompt = f"""
You are an expert technical writer and senior software engineer, tasked with creating a professional, comprehensive, and user-friendly README.md file for a new project. Your tone should be clear, concise, and welcoming to new developers.

Based on the detailed project context provided below, which includes the directory structure and key file contents, generate a complete README.md file.

Follow these rules and section-by-section instructions precisely:

**--- GENERAL RULES ---**
1.  **Markdown Only:** Generate only the raw Markdown content for the README.md file. Do not include any other explanatory text, greetings, or sign-offs in your response.
2.  **Security:** DO NOT include any sensitive information like API keys, secrets, or passwords, even if they appear in the provided file contents.
3.  **Code Blocks:** ALWAYS use Markdown code fences with the correct language identifier (e.g., ```python, ```bash, ```json).

**--- README SECTION INSTRUCTIONS ---**

**1. Project Title & Badges:**
   - Infer the project title from the root directory name. It should be a level-1 heading (e.g., `# My Awesome Project`).
   - Immediately after the title, identify the primary language and key frameworks from the dependencies. For each major technology, generate a `shields.io` badge on the same line. For example, for a Python/Flask project: `![Python](https://img.shields.io/badge/python-3670A0?style=for-the-badge&logo=python&logoColor=ffdd54) ![Flask](https://img.shields.io/badge/flask-%23000.svg?style=for-the-badge&logo=flask&logoColor=white)`.

**2. High-Level Description:**
   - Write a concise, one-paragraph summary of the project's purpose and the problem it solves. Analyze the function names, class names, and comments in the source code to understand *what* the project does and *why* it is useful.

**3. Key Features:**
   - Generate a bulleted list of 2-4 key features. Infer these by analyzing the main functions, classes, or exported modules in the code.

**4. Prerequisites & Installation:**
   - Under a "Prerequisites" sub-heading, state what needs to be installed globally (e.g., Python 3.9+, Node.js v18+).
   - Under an "Installation" sub-heading, provide the exact commands to clone and install the project dependencies in a code block. Assume a `git clone` command followed by the dependency installation command (e.g., `pip install -r requirements.txt`).

**5. Usage:**
   - This is the most critical section. Infer the primary use case from the code.
   - Look for a `main` function, a `if __name__ == "__main__":` block, or exported scripts in `package.json`.
   - Provide a clear, simple code block demonstrating how to run the project. For a Python script, this would be `python main.py [arguments]`.

**6. Project File Structure:**
   - Generate an ASCII tree diagram of the project structure inside a code block.
   - **Crucially, exclude** common noise and unimportant directories/files like `__pycache__`, `node_modules`, `.git`, `.vscode`, `.idea`, `venv`, and `dist`. Only show the files relevant to understanding the project's architecture.
---
Here is the project context:
    ---
    {context}
    ---
    """
    try:
        response = client.chat.completions.create(
            model=model_name,
            messages=[{"role": "user", "content": prompt}],
        )
        return response.choices[0].message.content or "# README Generation Failed"
    except RateLimitError:
        console.print(
            "[bold red]Rate Limit Error:[/bold red] You have exceeded your OpenRouter API quota."
        )
        raise typer.Exit(code=1)
    except NotFoundError:
        console.print(
            f"[bold red]Model Not Found:[/bold red] The model '{model_name}' does not exist or is not available."
        )
        raise typer.Exit(code=1)
    except AuthenticationError:
        console.print(
            "[bold red]Authentication Error:[/bold red] Your OpenRouter API key is invalid."
        )
        raise typer.Exit(code=1)
    except Exception as e:
        console.print(f"[bold red]An unexpected error occurred:[/bold red] {e}")
        raise typer.Exit(code=1)


def analyze_project(
    base_path: Path, max_files_to_read: int = 5, debug: bool = False
) -> str:
    """
    Analyzes the project structure and content, respecting .gitignore rules.
    """
    gitignore_path = base_path / ".gitignore"
    spec = None
    if gitignore_path.exists():
        with gitignore_path.open("r") as gf:
            spec = pathspec.PathSpec.from_lines("gitwildmatch", gf)
        if debug:
            console.print(
                f"[cyan]DEBUG: Loaded .gitignore from: {gitignore_path}[/cyan]"
            )

    tree_str, file_contents = "", ""
    files_read_count = 0

    all_paths = sorted(base_path.rglob("*"))

    paths_to_process = (
        [
            p
            for p in all_paths
            if not (spec and spec.match_file(str(p.relative_to(base_path))))
        ]
        if spec
        else all_paths
    )

    ignore_dirs = {".git", ".qodo"}
    ignore_files = {"README.md"}

    for path in paths_to_process:
        if any(part in ignore_dirs for part in path.parts) or path.name in ignore_files:
            continue

        relative_path = path.relative_to(base_path)
        if spec and any(spec.match_file(str(p)) for p in relative_path.parents):
            continue

        depth = len(relative_path.parts) - 1
        indent = "    " * depth
        if path.is_dir():
            tree_str += f"{indent}├── {path.name}/\n"
        else:
            tree_str += f"{indent}└── {path.name}\n"
            if files_read_count < max_files_to_read and path.suffix in {
                ".py",
                ".js",
                ".ts",
                ".go",
                ".java",
                ".toml",
                ".json",
                ".yml",
            }:
                try:
                    if debug:
                        console.print(
                            f"[cyan]DEBUG: Reading file for context: {path.name}[/cyan]"
                        )
                    content = path.read_text(encoding="utf-8")
                    file_contents += f"\n--- START OF {path.name} ---\n{content}\n--- END OF {path.name}---\n"
                    files_read_count += 1
                except Exception:
                    pass

    context_package = f"PROJECT DIRECTORY STRUCTURE:\n{tree_str}\n\nKEY FILE CONTENTS:\n{file_contents}"
    if debug:
        console.print(
            f"[cyan]DEBUG: Total context package size: {len(context_package)} characters[/cyan]"
        )
    return context_package


if __name__ == "__main__":
    app()
