# commands/auth.py
import typer
from client import ApiClient, save_token_to_file, clear_token_file
from dto import LoginBody
from rich.table import Table
from rich.console import Console

app = typer.Typer(help="Authentication commands")
console = Console()

def print_user_table(data):
    """Display user data in a formatted table."""
    table = Table(title="User Details")
    table.add_column("Field", style="cyan")
    table.add_column("Value", style="magenta")
    
    if isinstance(data, dict):
        for k, v in data.items():
            table.add_row(str(k), str(v))
    else:
        table.add_row("User", str(data))
    
    console.print(table)

@app.command("login")
def login(
    user_name: str = typer.Option(None, "--user-name", "-u", help="Username"),
    password: str = typer.Option(None, "--password", "-p", help="Password"),
    save: bool = typer.Option(False, "--save", "-s", help="Save token to file")
):
    """Login and retrieve JWT token."""
    # Interactive mode if flags not provided
    if not user_name:
        user_name = typer.prompt("Username")
    if not password:
        password = typer.prompt("Password", hide_input=True)

    client = ApiClient()
    body = LoginBody(userName=user_name, password=password).model_dump()
    try:
        token = client.post("/user/login", json=body)
        typer.echo(f"Token: {token}")
        if save:
            save_token_to_file(token)
            typer.echo("✓ Token saved to .cli_token")
    except Exception as e:
        typer.echo(f"✗ Error: {e}", err=True)
        raise typer.Exit(code=1)

@app.command("register")
def register(
    user_name: str = typer.Option(None, "--user-name", "-u", help="Username"),
    password: str = typer.Option(None, "--password", "-p", help="Password")
):
    """Register a new user."""
    # Interactive mode if flags not provided
    if not user_name:
        user_name = typer.prompt("Username")
    if not password:
        password = typer.prompt("Password", hide_input=True)
        password_confirm = typer.prompt("Confirm Password", hide_input=True)
        if password != password_confirm:
            typer.echo("✗ Passwords do not match!", err=True)
            raise typer.Exit(code=1)

    client = ApiClient()
    body = LoginBody(userName=user_name, password=password).model_dump()
    try:
        client.post("/user/register", json=body)
        typer.echo("✓ User registered successfully.")
    except Exception as e:
        typer.echo(f"✗ Error: {e}", err=True)
        raise typer.Exit(code=1)

@app.command("logout")
def logout():
    """Clear saved token."""
    clear_token_file()
    typer.echo("✓ Logged out (token file removed).")

@app.command("me")
def me(token: str = typer.Option(None, "--token", "-t", help="JWT Token")):
    """Get current user details."""
    client = ApiClient(token=token)
    try:
        data = client.get("/user/me")
        print_user_table(data)
    except Exception as e:
        typer.echo(f"✗ Error: {e}", err=True)
        raise typer.Exit(code=1)