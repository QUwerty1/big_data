#!/usr/bin/env python3
import typer
from rich.console import Console
from typing import Optional

from commands import auth, customer, product, sale, supplier, supply, generator
from client import ApiClient

# ✅ Option 1: Disable rich markup if you're still getting typer/click errors
# Set to None or "markdown" if "rich" causes issues
RICH_MODE: Optional[str] = "rich"  # Change to None if needed

app = typer.Typer(
    name="storage-client",
    help="CLI client for StorageServer API",
    rich_markup_mode=RICH_MODE,
)
console = Console()

# Add command groups
app.add_typer(auth.app, name="auth", help="Authentication commands")
app.add_typer(customer.app, name="customer", help="Customer operations")
app.add_typer(product.app, name="product", help="Product operations")
app.add_typer(sale.app, name="sale", help="Sale operations")
app.add_typer(supplier.app, name="supplier", help="Supplier operations")
app.add_typer(supply.app, name="supply", help="Supply operations")
app.add_typer(generator.app, name="generate", help="Generate test data")


@app.callback(invoke_without_command=True)  # ✅ Allow running without subcommand
def callback(
    ctx: typer.Context,
    server: Optional[str] = typer.Option(None, "--server", "-s", help="Server URL (overrides config)"),
):
    """
    StorageServer CLI client
    
    Use this tool to interact with the StorageServer API.
    """
    if ctx.invoked_subcommand is not None:
        try:
            ctx.obj = ApiClient(base_url=server) if server else ApiClient()
        except Exception as e:
            console.print(f"[red]✗ Failed to initialize API client: {e}[/red]")
            raise typer.Exit(1)


@app.command()
def version():  # ✅ Remove unused ctx parameter
    """Show version information"""
    console.print("[bold]StorageServer CLI Client[/bold]")
    console.print("Version: 1.0.0")
    console.print("API: v1")


@app.command()
def config():  # ✅ Remove unused ctx parameter
    """Show current configuration"""
    try:
        from config import settings  # ✅ Import inside function to avoid circular imports
        
        console.print("[bold]Current Configuration[/bold]")
        console.print(f"API URL: {settings.api_base_url}")
        console.print(f"Timeout: {settings.api_timeout}s")
        console.print(f"Token file: {settings.token_file}")
    except ImportError as e:
        console.print(f"[red]✗ Failed to load config: {e}[/red]")
        raise typer.Exit(1)
    except AttributeError as e:
        console.print(f"[red]✗ Config missing required fields: {e}[/red]")
        raise typer.Exit(1)


if __name__ == "__main__":
    app()