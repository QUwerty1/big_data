import typer
import click
from typing import Optional

from client import ApiClient, ApiError

app = typer.Typer(help="Authentication commands")


def _get_client() -> ApiClient:
    """✅ Get ApiClient from context or create new one"""
    try:
        ctx = click.get_current_context()
        if ctx.obj is not None:
            return ctx.obj
    except (RuntimeError, AttributeError):
        pass
    return ApiClient()


@app.command()
def login(
    username: Optional[str] = typer.Argument(None, help="Username"),
    password: Optional[str] = typer.Option(None, "--password", "-p", 
                                          help="Password (will prompt if not provided)"),
):
    """Login to the API and get JWT token"""
    client = _get_client()
    
    try:
        if not username:
            username = typer.prompt("Username")
        
        if not password:
            password = typer.prompt("Password", hide_input=True)
        
        # ✅ Type narrowing - tell Pylance these are definitely str
        assert username is not None
        assert password is not None
        
        token = client.login(username, password)
        typer.echo(f"✓ Successfully logged in as {username}")
        typer.echo(f"Token saved to file")
    except ApiError as e:
        typer.echo(f"✗ Login failed: {e}", err=True)
        raise typer.Exit(1)


@app.command()
def logout():
    """Logout and clear saved token"""
    client = _get_client()
    
    try:
        client.logout()
        typer.echo("✓ Successfully logged out")
    except Exception as e:
        typer.echo(f"✗ Error: {e}", err=True)
        raise typer.Exit(1)


@app.command()
def register(
    username: Optional[str] = typer.Argument(None, help="Username"),
    password: Optional[str] = typer.Option(None, "--password", "-p", 
                                          help="Password (will prompt if not provided)"),
):
    """Register a new user"""
    client = _get_client()
    
    try:
        if not username:
            username = typer.prompt("Username")
        
        if not password:
            password = typer.prompt("Password", hide_input=True)
        
        # ✅ Type narrowing - tell Pylance these are definitely str
        assert username is not None
        assert password is not None
        
        client.register(username, password)
        typer.echo(f"✓ Successfully registered user {username}")
    except ApiError as e:
        typer.echo(f"✗ Registration failed: {e}", err=True)
        raise typer.Exit(1)


@app.command()
def staff():
    """✅ Check if current user is staff"""
    client = _get_client()
    
    try:
        is_staff = client.is_staff()
        if is_staff:
            typer.echo("✓ Current user is staff")
        else:
            typer.echo("✗ Current user is not staff")
    except ApiError as e:
        typer.echo(f"✗ Failed to check staff status: {e}", err=True)
        raise typer.Exit(1)