import typer
from rich.console import Console
from rich.panel import Panel
from rich.table import Table
import os
from pathlib import Path
import pathspec
import yaml
import requests
import datetime
from openai import OpenAI, AuthenticationError, RateLimitError, NotFoundError, PermissionDeniedError
from dotenv import load_dotenv, set_key as dotenv_set_key

# --- Configuration ---
app = typer.Typer(help="A powerful CLI to generate and manage project documentation using AI.")
console = Console()
dotenv_path = Path('.env')
config_path = Path('.mkaireadme.yml')
# ---

# ... (Helper functions: load_api_key, create_openrouter_client remain the same) ...
def load_api_key():
    """Loads the .env file and returns the OpenRouter API key."""
    load_dotenv(dotenv_path=dotenv_path)
    return os.getenv("OPENROUTER_API_KEY")

def create_openrouter_client(api_key: str) -> OpenAI:
    """Creates and new_string an OpenAI client for OpenRouter."""
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
project_goals: ""
custom_instructions: ""
exclude:
  - "docs/"
  - "*.log"
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
def license():
    """
    Creates a LICENSE file for your project.
    """
    if Path("LICENSE").exists():
        console.print("[yellow]A LICENSE file already exists in this directory.[/yellow]")
        if not typer.confirm("Do you want to overwrite it?"):
            console.print("[red]Aborted.[/red]")
            raise typer.Exit()

    licenses = {
        "MIT": "mit",
        "Apache 2.0": "apache-2.0",
        "GPLv3": "gpl-3.0",
    }
    
    console.print(Panel("Choose a license for your project:", title="[green]License Selection[/green]"))
    for i, name in enumerate(licenses.keys(), 1):
        console.print(f"{i}. {name}")
    
    choice = typer.prompt("Enter the number of your choice", type=int)
    
    if choice < 1 or choice > len(licenses):
        console.print("[bold red]Invalid selection.[/bold red]")
        raise typer.Exit(code=1)
        
    license_key = list(licenses.values())[choice - 1]
    
    full_name = typer.prompt("Please enter your full name (for the copyright notice)")

    try:
        with console.status(f"[bold green]Fetching license text for {license_key}...[/bold green]"):
            response = requests.get(f"https://api.github.com/licenses/{license_key}")
            response.raise_for_status()
            license_data = response.json()
        
        license_text = license_data["body"]
        year = datetime.datetime.now().year
        
        # Replace placeholders
        final_text = license_text.replace("[year]", str(year)).replace("[fullname]", full_name)
        
        Path("LICENSE").write_text(final_text, encoding="utf-8")
        console.print(f"✅ [bold green]Successfully created LICENSE file with the {list(licenses.keys())[choice - 1]} license![/bold green]")

    except requests.RequestException as e:
        console.print(f"[bold red]Error fetching license data:[/bold red] {e}")
        raise typer.Exit(code=1)

@app.command()
def models(search: str = typer.Argument(None, help="An optional term to search for models.")):
    """
    Lists recommended models or searches for a specific model.
    """
    # ... (This function remains the same) ...
    api_key = load_api_key()
    if not api_key:
        console.print(Panel("[bold]No API Key Found[/bold]\n\nPlease set your key first: [cyan]mkaireadme set-key YOUR_KEY[/cyan]", title="[yellow]Action Required[/yellow]", border_style="red"))
        raise typer.Exit()
    client = create_openrouter_client(api_key)
    recommended_models = ["google/gemini-flash-1.5", "anthropic/claude-3-haiku", "mistralai/mistral-7b-instruct", "meta-llama/llama-3-8b-instruct", "openai/gpt-4o-mini"]
    if not search:
        console.print(Panel("Showing a few recommended models. To see more, search for a term like 'llama', 'claude', or 'gemma'.\nExample: [cyan]mkaireadme models llama[/cyan]", title="[green]Recommended Models[/green]"))
        table = Table(show_lines=True)
        table.add_column("Recommended Model ID", style="cyan")
        for model_id in recommended_models: table.add_row(model_id)
        console.print(table)
        return
    with console.status(f"[bold green]Searching for models matching '{search}'...[/bold green]"):
        try:
            model_list = client.models.list().data
            model_ids = sorted([model.id for model in model_list])
            filtered_models = [m for m in model_ids if search.lower() in m.lower()]
            if not filtered_models:
                console.print(f"[yellow]No models found matching '{search}'.[/yellow]")
                raise typer.Exit()
            table = Table(title=f"Models Matching '{search}'", show_lines=True)
            table.add_column("Model ID", style="cyan")
            for model_id in filtered_models: table.add_row(model_id)
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
    # ... (This function's logic is updated by analyze_project and generate_readme) ...
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
            console.print(Panel("[bold]Custom README.md Detected[/bold]\n\nTo enable smart updates, I need to add markers to this file.\nThis will wrap your existing content safely. It is a one-time operation.", title="[yellow]Action Required[/yellow]", border_style="yellow"))
            if typer.confirm("Proceed with adding markers?", default=True):
                readme_path.write_text(f"{autogen_start_marker}\n\n{content.strip()}\n\n{autogen_end_marker}", encoding="utf-8")
                console.print("✅ Markers added successfully.")
            else:
                console.print("[red]Aborted.[/red] To generate a new README, run again with the `--force-overwrite` flag.")
                raise typer.Exit()
    client = create_openrouter_client(api_key)
    with console.status("[bold green]🤖 Analyzing project...") as status:
        project_context, user_guidance = analyze_project(Path("."), debug=debug)
        status.update(f"[bold green]🧠 Contacting OpenRouter with model '{model}'...")
        generated_content = generate_readme(client, project_context, user_guidance, model)
        if generated_content.strip().startswith("```markdown"): generated_content = generated_content.strip()[10:]
        if generated_content.strip().endswith("```"): generated_content = generated_content.strip()[:-3]
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
    """Generates a README file using the OpenRouter API with a flexible and powerful prompt."""
    prompt = f"""
    As an expert technical writer and open-source project designer, your primary goal is to create a README.md file that is **clear, professional, and easy for a new developer to understand.**
    Based on the project evidence provided, generate a complete and visually appealing README. Your response should be a single Markdown file.

    ---

    ### **Guiding Principles for Your README:**

    1.  **Start with a "Hook":** Begin with a strong, visually appealing hero section. Use HTML for a centered layout. This section must include the project's title, a concise one-line description, and 3-4 relevant shields.io badges.
    2.  **Explain the "Why":** Immediately after the hook, create a "Key Features" or "Introduction" section. Use bullet points (with emojis for visual appeal) to explain what the project does and why it's useful.
    3.  **Show, Don't Just Tell:** Provide clear, copy-pasteable code blocks for "Installation" and "Usage." The commands you provide must be idiomatic for the project's ecosystem (e.g., `npm install` for a Node.js project, `pip install` for Python).
    4.  **Be Comprehensive but Concise:** Include other relevant sections as you see fit, based on the evidence. Good optional sections include "Tech Stack," "Configuration," "Contributing," and "License." Only include a section if you have meaningful information to put in it.
    5.  **Maintain a Professional Aesthetic:** Use Markdown formatting (headings, bold text, lists) to create a clean, well-structured, and easily scannable document.

    ---

    **Final Instructions:**
    - Do not invent features or commands that are not supported by the evidence.
    - Do not include images or logos unless one is explicitly found in the project's assets.
    - Generate only the Markdown content for the README.md file.

    Here is the project evidence:
    ---
    {context}
    ---
    {guidance}
    ---
    """
    try:
        response = client.chat.completions.create(
            model=model_name,
            messages=[{"role": "user", "content": prompt.strip()}],
        )
        return response.choices[0].message.content or "# README Generation Failed"
    except PermissionDeniedError as e:
        console.print(Panel("[bold]Model Moderation Error[/bold]\n\nThe model '{model_name}' has a strict safety filter that incorrectly flagged your project's source code.\n\nPlease try a different model from another provider.", title="[yellow]Action Required[/yellow]", border_style="red"))
        raise typer.Exit(code=1)
    except (RateLimitError, NotFoundError, AuthenticationError) as e:
        console.print(f"[bold red]API Error:[/bold red] {e}")
        raise typer.Exit(code=1)
    except Exception as e:
        console.print(f"[bold red]An unexpected error occurred:[/bold red] {e}")
        raise typer.Exit(code=1)

def analyze_project(base_path: Path, debug: bool = False) -> tuple[str, str]:
    """
    Analyzes the project, respecting all configs, and returns the code context and user guidance.
    """
    # ... (Content budget logic remains the same, but we add license detection) ...
    MAX_CONTEXT_CHARS = 35000
    user_guidance = ""
    config = {}
    if config_path.exists():
        if debug: console.print(f"[cyan]DEBUG: Loading config from {config_path}[/cyan]")
        with config_path.open('r') as yf:
            config = yaml.safe_load(yf) or {}
    
    goals = config.get('project_goals', '')
    instructions = config.get('custom_instructions', '')
    
    # --- License Detection ---
    license_info = ""
    if Path("LICENSE").exists() or Path("LICENSE.md").exists():
        license_info = "A LICENSE file was found. Please add a section to the README referencing it."

    if goals or instructions or license_info:
        user_guidance += "--- User Guidance ---\n"
        if goals: user_guidance += f"Project Goals: {goals}\n"
        if instructions: user_guidance += f"Instructions: {instructions}\n"
        if license_info: user_guidance += f"License Info: {license_info}\n"
        user_guidance += "-------------------\n\n"

    # ... (The rest of the content budget analysis logic remains the same) ...
    gitignore_path = base_path / '.gitignore'
    spec_lines = []
    if gitignore_path.exists():
        with gitignore_path.open('r') as gf: spec_lines = gf.readlines()
    for pattern in config.get('exclude', []): spec_lines.append(pattern)
    spec = pathspec.PathSpec.from_lines('gitwildmatch', spec_lines) if spec_lines else None
    candidate_files = []
    ignore_dirs = {".git", ".qodo", ".venv", "dist", "build"}
    ignore_files = {"README.md", ".env", ".mkaireadme.yml", "LICENSE", "LICENSE.md"}
    source_extensions = {".py", ".js", ".ts", ".go", ".java", ".toml", ".json", ".yml"}
    for path in base_path.rglob("*"):
        if any(part in ignore_dirs for part in path.parts) or path.name in ignore_files: continue
        if spec and spec.match_file(str(path.relative_to(base_path))): continue
        if not path.is_file(): continue
        if path.suffix in source_extensions: candidate_files.append(path)
    candidate_files.sort(key=lambda p: p.stat().st_size)
    tree_str, file_contents = "", ""
    current_content_size = 0
    for path in candidate_files:
        try:
            content_to_add = path.read_text(encoding="utf-8")
            content_chunk = f"\n--- START OF {path.name} ---\n{content_to_add}\n--- END OF {path.name} ---\n"
            if current_content_size + len(content_chunk) > MAX_CONTEXT_CHARS:
                if debug: console.print(f"[yellow]DEBUG: Content budget reached. Stopping analysis.[/yellow]")
                break
            if debug: console.print(f"[cyan]DEBUG: Reading file for context: {path.name} ({path.stat().st_size} bytes)[/cyan]")
            file_contents += content_chunk
            current_content_size += len(content_chunk)
        except Exception: pass
    tree_str = "A brief overview of the project structure is inferred from the file contents below."
    context_package = f"PROJECT DIRECTORY STRUCTURE:\n{tree_str}\n\nKEY FILE CONTENTS:\n{file_contents}"
    if debug: console.print(f"[cyan]DEBUG: Total context package size: {len(context_package)} characters[/cyan]")
    return context_package, user_guidance

if __name__ == "__main__":
    app()