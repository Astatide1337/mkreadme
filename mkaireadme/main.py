import typer
from rich.console import Console
from rich.panel import Panel
from rich.table import Table
import os
from pathlib import Path
import pathspec
import yaml
from openai import OpenAI, AuthenticationError, PermissionDeniedError, RateLimitError, NotFoundError
from dotenv import load_dotenv, set_key as dotenv_set_key

# --- Configuration ---
app = typer.Typer(help="A CLI tool to generate professional README.md files using AI.")
console = Console()
dotenv_path = Path('.env')
config_path = Path('.mkaireadme.yml')
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
            "HTTP-Referer": "https://github.com/gemini-cli/mkaireadme",
            "X-Title": "mkaireadme CLI",
        },
    )

@app.command()
def init():
    """
    Creates a .mkaireadme.yml file to help guide the AI.
    """
    if config_path.exists():
        console.print(f"[yellow]'{{config_path}}' already exists.[/yellow]")
        return

    default_config = """
# --- mkaireadme Configuration ---
# Use this file to guide the AI and fine-tune your README generation.

# project_goals: Describe the main purpose and vision of your project.
# This helps the AI write a better high-level description.
project_goals: ""

# custom_instructions: Provide specific instructions for the AI.
# For example: "Emphasize the real-time features." or "Do not mention the legacy API."
custom_instructions: ""

# exclude: A list of glob patterns for files/directories to exclude from analysis.
# This is in addition to your .gitignore file.
exclude:
  - ""
"""
    config_path.write_text(default_config.strip())
    console.print(f"✅ [bold green]Created '{config_path}'! Edit it to guide the AI.[/bold green]")

@app.command()
def set_key(api_key: str = typer.Argument(..., help="Your OpenRouter API key.")):
    """
    Saves your OpenRouter API key securely to a .env file.
    """
    dotenv_set_key(dotenv_path, "OPENROUTER_API_KEY", api_key)
    console.print("✅ [bold green]OpenRouter API Key saved successfully![/bold green]")

@app.command()
def models(search: str = typer.Argument(None, help="An optional term to search for models.")):
    """
    Lists recommended models or searches for a specific model.
    """
    # ... (This function remains the same as the last correct version)
    api_key = load_api_key()
    if not api_key:
        console.print(Panel("[bold]No API Key Found[/bold]\n\nPlease set your key first: [cyan]python main.py set-key YOUR_KEY[/cyan]", title="[yellow]Action Required[/yellow]", border_style="red"))
        raise typer.Exit()

    client = create_openrouter_client(api_key)
    
    recommended_models = [
        "google/gemini-flash-1.5", "anthropic/claude-3-haiku", "mistralai/mistral-7b-instruct",
        "meta-llama/llama-3-8b-instruct", "openai/gpt-4o-mini",
    ]

    if not search:
        console.print(Panel("Showing a few recommended models. To see more, search for a term like 'llama', 'claude', or 'gemma'.\nExample: [cyan]python main.py models llama[/cyan]", title="[green]Recommended Models[/green]"))
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
            console.print("[bold red]Authentication Error:[/bold red] Your OpenRouter API key is invalid.")
            raise typer.Exit(code=1)
        except Exception as e:
            console.print(f"[bold red]An unexpected error occurred:[/bold red] {e}")
            raise typer.Exit(code=1)

@app.command()
def gen(
    model: str = typer.Option(..., "--model", help="The model ID to use for generation."),
    force_overwrite: bool = typer.Option(False, "--force-overwrite", help="Forcibly overwrite a README.md that has no autogen markers."),
    debug: bool = typer.Option(False, "--debug", help="Enable debug output."),
):
    """
    Generates or smartly updates a professional README.md file for your project.
    """
    api_key = load_api_key()
    if not api_key:
        console.print(Panel("[bold]No API Key Found[/bold]\n\nPlease set your key first: [cyan]mkaireadme set-key YOUR_KEY[/cyan]", title="[yellow]Action Required[/yellow]", border_style="red"))
        raise typer.Exit()

    readme_path = Path("README.md")
    autogen_start_marker = "<!-- AUTOGEN:START -->"
    autogen_end_marker = "<!-- AUTOGEN:END -->"

    if readme_path.exists() and not force_overwrite:
        content = readme_path.read_text(encoding="utf-8")
        if autogen_start_marker not in content or autogen_end_marker not in content:
            console.print(Panel(
                "[bold]Custom README.md Detected[/bold]\n\n"
                "To enable smart updates, I need to add markers to this file.\n"
                "This will wrap your existing content safely. It is a one-time operation.",
                title="[yellow]Action Required[/yellow]", border_style="yellow"
            ))
            if typer.confirm("Proceed with adding markers?", default=True):
                readme_path.write_text(
                    f"{autogen_start_marker}\n\n{content.strip()}\n\n{autogen_end_marker}",
                    encoding="utf-8"
                )
                console.print("✅ Markers added successfully.")
            else:
                console.print("[red]Aborted.[/red] To generate a new README, run again with the `--force-overwrite` flag.")
                raise typer.Exit()

    client = create_openrouter_client(api_key)
    
    with console.status("[bold green]🤖 Analyzing project...") as status:
        project_context, user_guidance = analyze_project(Path("."), debug=debug)
        status.update(f"[bold green]🧠 Contacting OpenRouter with model '{model}'...")
        generated_content = generate_readme(client, project_context, user_guidance, model)
        generated_content = generated_content.replace(autogen_start_marker, "").replace(autogen_end_marker, "")

    try:
        if readme_path.exists():
            content = readme_path.read_text(encoding="utf-8")
            if autogen_start_marker in content and autogen_end_marker in content:
                pre_content = content.split(autogen_start_marker)[0]
                post_content = content.split(autogen_end_marker)[1]
                new_content = (f"{pre_content.strip()}\n\n{autogen_start_marker}\n\n{generated_content.strip()}\n\n{autogen_end_marker}\n\n{post_content.strip()}").strip()
                readme_path.write_text(new_content, encoding="utf-8")
                console.print("✅ Successfully updated README.md!", style="bold green")
            else:
                full_content = f"{autogen_start_marker}\n\n{generated_content.strip()}\n\n{autogen_end_marker}"
                readme_path.write_text(full_content, encoding="utf-8")
                console.print("✅ Successfully overwrote README.md!", style="bold green")
        else:
            full_content = f"{autogen_start_marker}\n\n{generated_content.strip()}\n\n{autogen_end_marker}"
            readme_path.write_text(full_content, encoding="utf-8")
            console.print("✅ Successfully created README.md!", style="bold green")
    except (IOError, PermissionError) as e:
        console.print(f"Error writing to README.md: {e}", style="bold red")
        raise typer.Exit(code=1)

    console.print("\n--- Generated README.md ---\n", style="bold blue")
    console.print(generated_content)

def generate_readme(client: OpenAI, context: str, guidance: str, model_name: str) -> str:
    """Generates a README file using the OpenRouter API."""
    prompt = f"""
    As an expert technical writer, create a professional README.md file for a software project.
    Based on the following context (directory structure and key file contents) and user guidance, generate a complete README.
    
    {guidance}

    The README should have standard sections like Project Title, Description, Tech Stack, Installation, and Usage.
    Generate only the Markdown content. Do not include any other explanatory text.
    
    Here is the code context:
    ---
    {context}
    ---
    """
    try:
        response = client.chat.completions.create(
            model=model_name,
            messages=[{"role": "user", "content": prompt.strip()}],
        )
        return response.choices[0].message.content or "# README Generation Failed"
    except PermissionDeniedError as e:
        console.print(Panel(
            "[bold]Model Moderation Error[/bold]\n\n"
            f"The model '{model_name}' has a strict safety filter that incorrectly flagged your project's source code.\n\n"
            "[bold]This is not an error with your project.[/bold]\n\n"
            "Please try a different model from another provider.\n"
            "Good alternatives include models from Google, Anthropic, or MistralAI.",
            title="[yellow]Action Required[/yellow]", border_style="red"
        ))
        raise typer.Exit(code=1)
    except (RateLimitError, NotFoundError, AuthenticationError) as e:
        console.print(f"[bold red]API Error:[/bold red] {e}")
        raise typer.Exit(code=1)

def analyze_project(base_path: Path, max_files_to_read: int = 5, debug: bool = False) -> tuple[str, str]:
    """
    Analyzes the project, respecting .gitignore and .mkaireadme.yml, and returns the code context and user guidance.
    """
    # --- User Guidance from .mkaireadme.yml ---
    user_guidance = ""
    config = {}
    if config_path.exists():
        if debug: console.print(f"[cyan]DEBUG: Loading config from {config_path}[/cyan]")
        with config_path.open('r') as yf:
            config = yaml.safe_load(yf) or {}
        
        goals = config.get('project_goals', '')
        instructions = config.get('custom_instructions', '')
        if goals or instructions:
            user_guidance += "--- User Guidance ---\n"
        if goals: 
            user_guidance += f"Project Goals: {goals}\n"
        if instructions: 
            user_guidance += f"Instructions: {instructions}\n"
        user_guidance += "-------------------\n\n"

    # --- Code Context Analysis ---
    gitignore_path = base_path / '.gitignore'
    spec_lines = []
    if gitignore_path.exists():
        with gitignore_path.open('r') as gf:
            spec_lines = gf.readlines()
    
    # Add excludes from .mkaireadme.yml
    for pattern in config.get('exclude', []):
        spec_lines.append(pattern)
    
    spec = pathspec.PathSpec.from_lines('gitwildmatch', spec_lines) if spec_lines else None

    tree_str, file_contents = "", ""
    files_read_count = 0
    
    paths_to_process = [p for p in sorted(base_path.rglob("*")) if not (spec and spec.match_file(str(p.relative_to(base_path))))] if spec else sorted(base_path.rglob("*"))

    ignore_dirs = {".git", ".qodo"}
    ignore_files = {"README.md", ".env", ".mkaireadme.yml"}

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
            if files_read_count < max_files_to_read and path.suffix in {".py", ".js", ".ts", ".go", ".java", ".toml", ".json"}:
                try:
                    if debug: console.print(f"[cyan]DEBUG: Reading file for context: {path.name}[/cyan]")
                    content = path.read_text(encoding="utf-8")
                    file_contents += f"\n--- START OF {path.name} ---\n{content}\n--- END OF {path.name}---\n"
                    files_read_count += 1
                except Exception: pass

    context_package = f"PROJECT DIRECTORY STRUCTURE:\n{tree_str}\n\nKEY FILE CONTENTS:\n{file_contents}"
    if debug: console.print(f"[cyan]DEBUG: Total context package size: {len(context_package)} characters[/cyan]")
    return context_package, user_guidance

if __name__ == "__main__":
    app()
