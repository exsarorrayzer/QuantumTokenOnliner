import json
from pathlib import Path
from time import sleep
from rich.console import Console
from rich.panel import Panel
from rich.align import Align
from rich.text import Text
from rich.box import ROUNDED

def show_creds():
    base = Path(__file__).resolve().parent.parent
    data_path = base / "db" / "data.json"
    console = Console()
    
    try:
        with open(data_path, "r", encoding="utf-8") as f:
            data = json.load(f)
    except Exception:
        console.print("[bold red]Error: Cannot read data.json[/bold red]")
        return

    name = data.get("name", "Unknown")
    author = data.get("author", "Unknown")
    
    info_lines = []
    info_lines.append(f"[bold blue]Developer:[/bold blue] {author}")
    
    social = data.get("social", {})
    if social:
        info_lines.append("")
        info_lines.append("[bold blue]Social Media:[/bold blue]")
        for platform, username in social.items():
            info_lines.append(f"  {platform.capitalize()}: {username}")

    body = "\n".join(info_lines)

    panel = Panel(
        Align.center(body), 
        title=Text(name, style="bold blue"),
        box=ROUNDED, 
        border_style="blue",
        width=50
    )
    
    console.print(panel)
    sleep(0.6)