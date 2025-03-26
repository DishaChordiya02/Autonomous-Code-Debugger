import argparse
import os
from rich.console import Console # type: ignore
from rich.panel import Panel # type: ignore
from rich.syntax import Syntax # type: ignore
from debugger import analyze_code
from llm_debugger import get_suggestions  # Now safely importing after fixing the issue

# Initialize Rich Console
console = Console()

def autonomous_debugger(source_code):
    """
    Combines AST-based issue detection with AI-powered debugging.
    """
    issues = analyze_code(source_code)  # Step 1: Detect issues using AST

    if not issues:
        console.print(Panel(" No issues found in the code!", title="AI Debugger", style="green"))
        return

    for issue in issues:
        console.print(Panel(f" [bold yellow]Issue Detected:[/bold yellow]\n{issue}", style="yellow"))

        fix = get_suggestions(issue, source_code)  # Step 2: Get AI-generated fixes
        
        console.print(Panel(f" [bold cyan]Suggested Fix:[/bold cyan]\n{fix}", style="cyan"))

if __name__ == "__main__":
    parser = argparse.ArgumentParser(description="AI Debugger for Python Code")
    parser.add_argument("file", help="Path to the Python file to analyze")

    args = parser.parse_args()
    
    if not os.path.exists(args.file):
        console.print(f" [bold red]Error:[/bold red] The file '{args.file}' does not exist.", style="red")
        exit(1)

    # Read the content of the provided file
    with open(args.file, "r", encoding="utf-8") as f:
        code_content = f.read()

    # Display the original code with syntax highlighting
    console.print(Panel(Syntax(code_content, "python", theme="monokai", line_numbers=True), title="📜 Source Code", style="blue"))

    # Run the debugger on the file's content
    console.print("\n [bold green]AI Debugger Output:[/bold green]\n", style="green")
    autonomous_debugger(code_content)
