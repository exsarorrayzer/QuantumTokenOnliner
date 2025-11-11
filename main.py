import asyncio
import json
from pathlib import Path
from func.banner import show_banner
from func.creds import show_creds
from func.token_manager import TokenManager
from func.proxy_manager import ProxyManager
from func.online_manager import OnlineManager
from rich.console import Console
from rich.prompt import Prompt
from rich.panel import Panel
from rich.layout import Layout
from rich.live import Live
from rich.table import Table
import time

class QuantumOnliner:
    def __init__(self):
        self.console = Console()
        self.token_manager = TokenManager()
        self.proxy_manager = ProxyManager()
        self.online_manager = OnlineManager()
        self.config = self.load_config()
    
    def load_config(self):
        config_path = Path(__file__).resolve().parent / "db" / "config.json"
        try:
            with open(config_path, "r", encoding="utf-8") as f:
                return json.load(f)
        except Exception:
            return {}
    
    def show_main_menu(self):
        show_banner()
        
        menu_options = [
            "[bold blue]1.[/bold blue] Token Management",
            "[bold blue]2.[/bold blue] Proxy Management", 
            "[bold blue]3.[/bold blue] Start Online",
            "[bold blue]4.[/bold blue] Statistics",
            "[bold blue]5.[/bold blue] Settings",
            "[bold blue]6.[/bold blue] Exit"
        ]
        
        menu_text = "\n".join(menu_options)
        panel = Panel(
            menu_text,
            title="[bold blue]QuantumOnliner - Main Menu[/bold blue]",
            border_style="blue",
            width=50
        )
        
        self.console.print(panel)
    
    def token_management_menu(self):
        self.console.print(Panel("[bold blue]Token Management[/bold blue]", border_style="blue"))
        
        options = [
            "1. Add Token",
            "2. List Tokens",
            "3. Delete Token", 
            "4. Validate Tokens",
            "5. Back to Main Menu"
        ]
        
        for option in options:
            self.console.print(option)
        
        choice = Prompt.ask("Choice", choices=["1", "2", "3", "4", "5"])
        
        if choice == "1":
            token = Prompt.ask("Token")
            note = Prompt.ask("Note (optional)")
            self.token_manager.add_token(token, note)
            self.console.print("[green]Token added![/green]")
        
        elif choice == "2":
            tokens = self.token_manager.get_all_tokens()
            if tokens:
                table = Table(show_header=True, header_style="bold blue")
                table.add_column("Token", style="cyan")
                table.add_column("Status", style="green")
                table.add_column("Note", style="white")
                
                for token_data in tokens:
                    status = "Online" if token_data.get("online") else "Offline"
                    table.add_row(
                        token_data["token"][:20] + "...",
                        status,
                        token_data.get("note", "")
                    )
                self.console.print(table)
            else:
                self.console.print("[yellow]No tokens found[/yellow]")
        
        elif choice == "3":
            token = Prompt.ask("Token to delete")
            if self.token_manager.remove_token(token):
                self.console.print("[green]Token deleted![/green]")
            else:
                self.console.print("[red]Token not found[/red]")
        
        elif choice == "4":
            # Token validation logic
            self.console.print("[yellow]Validation feature coming soon[/yellow]")
        
        self.token_management_menu()
    
    def proxy_management_menu(self):
        self.console.print(Panel("[bold blue]Proxy Management[/bold blue]", border_style="blue"))
        
        options = [
            "1. Add Proxy",
            "2. List Proxies", 
            "3. Delete Proxy",
            "4. Back to Main Menu"
        ]
        
        for option in options:
            self.console.print(option)
        
        choice = Prompt.ask("Choice", choices=["1", "2", "3", "4"])
        
        if choice == "1":
            proxy_type = Prompt.ask("Type", choices=["residential", "datacenter", "rotating"])
            ip = Prompt.ask("IP")
            port = Prompt.ask("Port")
            username = Prompt.ask("Username")
            password = Prompt.ask("Password")
            country = Prompt.ask("Country")
            
            self.proxy_manager.add_proxy(proxy_type, ip, port, username, password, country)
            self.console.print("[green]Proxy added![/green]")
        
        elif choice == "2":
            stats = self.proxy_manager.proxies["statistics"]
            self.console.print(f"Total Proxies: {stats['total_proxies']}")
            self.console.print(f"Active Proxies: {stats['active_proxies']}")
        
        elif choice == "3":
            proxy_type = Prompt.ask("Type", choices=["residential", "datacenter", "rotating"])
            ip = Prompt.ask("IP")
            port = Prompt.ask("Port")
            
            if self.proxy_manager.remove_proxy(proxy_type, ip, port):
                self.console.print("[green]Proxy deleted![/green]")
            else:
                self.console.print("[red]Proxy not found[/red]")
        
        self.proxy_management_menu()
    
    def statistics_menu(self):
        self.console.print(Panel("[bold blue]Statistics[/bold blue]", border_style="blue"))
        
        token_stats = self.token_manager.tokens_data["statistics"]
        proxy_stats = self.proxy_manager.proxies["statistics"]
        
        table = Table(show_header=True, header_style="bold blue")
        table.add_column("Category", style="cyan")
        table.add_column("Value", style="white")
        
        table.add_row("Total Tokens", str(token_stats["total"]))
        table.add_row("Valid Tokens", str(token_stats["valid"]))
        table.add_row("Online Tokens", str(token_stats["online"]))
        table.add_row("Total Proxies", str(proxy_stats["total_proxies"]))
        table.add_row("Active Proxies", str(proxy_stats["active_proxies"]))
        
        self.console.print(table)
        
        Prompt.ask("Press Enter to continue")
    
    async def start_online_mode(self):
        self.console.print(Panel("[bold blue]Starting Online Mode[/bold blue]", border_style="blue"))
        
        tokens = self.token_manager.get_valid_tokens()
        if not tokens:
            self.console.print("[red]No valid tokens found![/red]")
            return
        
        self.console.print(f"[green]Starting {len(tokens)} tokens...[/green]")
        
        try:
            await self.online_manager.start_online()
        except KeyboardInterrupt:
            self.console.print("[yellow]Stopping online mode...[/yellow]")
            self.online_manager.stop_online()
    
    def run(self):
        while True:
            self.show_main_menu()
            choice = Prompt.ask("Select option", choices=["1", "2", "3", "4", "5", "6"])
            
            if choice == "1":
                self.token_management_menu()
            elif choice == "2":
                self.proxy_management_menu()
            elif choice == "3":
                asyncio.run(self.start_online_mode())
            elif choice == "4":
                self.statistics_menu()
            elif choice == "5":
                self.console.print("[yellow]Settings menu coming soon[/yellow]")
            elif choice == "6":
                self.console.print("[blue]Thanks for using QuantumOnliner![/blue]")
                break

if __name__ == "__main__":
    app = QuantumOnliner()
    app.run()