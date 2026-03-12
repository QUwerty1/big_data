import typer
from typing import Optional, List
from rich.console import Console
from rich.table import Table

from client import ApiClient, ApiError
from dto import SupplierDto

app = typer.Typer(help="Supplier commands")
console = Console()


def display_supplier(supplier: SupplierDto):
    """Display a single supplier"""
    table = Table(title=f"Supplier #{supplier.id}")
    table.add_column("Property", style="cyan")
    table.add_column("Value", style="green")
    
    table.add_row("ID", str(supplier.id) if supplier.id else "N/A")
    table.add_row("Company Name", supplier.companyName)
    table.add_row("Phone", supplier.phone)
    table.add_row("Address", supplier.address)
    table.add_row("Email", supplier.email)
    table.add_row("App User ID", supplier.appUserId)
    
    if supplier.supplies:
        table.add_row("Supplies Count", str(len(supplier.supplies)))
    
    console.print(table)


def display_suppliers(suppliers: List[SupplierDto]):
    """Display a list of suppliers"""
    if not suppliers:
        console.print("[yellow]No suppliers found[/yellow]")
        return
    
    table = Table(title="Suppliers")
    table.add_column("ID", style="cyan", justify="right")
    table.add_column("Company Name", style="green")
    table.add_column("Phone", style="blue")
    table.add_column("Email", style="magenta")
    
    for supplier in suppliers:
        table.add_row(
            str(supplier.id) if supplier.id else "N/A",
            supplier.companyName,
            supplier.phone,
            supplier.email
        )
    
    console.print(table)


@app.command("get")
def get_supplier(
    ctx: typer.Context,
    supplier_id: int = typer.Argument(..., help="Supplier ID"),
):
    """Get supplier by ID"""
    if ctx.obj is None:
        ctx.obj = ApiClient()
    client = ctx.obj
    
    try:
        supplier = client.get_supplier(supplier_id)
        display_supplier(supplier)
    except ApiError as e:
        console.print(f"[red]✗ Failed to get supplier: {e}[/red]")
        raise typer.Exit(1)
    except Exception as e:
        console.print(f"[red]✗ Error: {e}[/red]")
        raise typer.Exit(1)


@app.command("get-all")
def get_all_suppliers(
    ctx: typer.Context,
    take: Optional[int] = typer.Option(None, "--take", "-t", help="Number of suppliers to take"),
    skip: int = typer.Option(0, "--skip", "-s", help="Number of suppliers to skip"),
):
    """Get all suppliers with pagination"""
    if ctx.obj is None:
        ctx.obj = ApiClient()
    client = ctx.obj
    
    try:
        suppliers = client.get_all_suppliers(take=take, skip=skip)
        display_suppliers(suppliers)
    except ApiError as e:
        console.print(f"[red]✗ Failed to get suppliers: {e}[/red]")
        raise typer.Exit(1)
    except Exception as e:
        console.print(f"[red]✗ Error: {e}[/red]")
        raise typer.Exit(1)


@app.command("create")
def create_supplier(
    ctx: typer.Context,
    company_name: str = typer.Option(..., "--company", "-c", help="Company name"),
    phone: str = typer.Option(..., "--phone", "-p", help="Phone number"),
    address: str = typer.Option(..., "--address", "-a", help="Address"),
    email: str = typer.Option(..., "--email", "-e", help="Email"),
    app_user_id: str = typer.Option(..., "--app-user-id", "-u", help="App User ID"),
):
    """Create a new supplier"""
    if ctx.obj is None:
        ctx.obj = ApiClient()
    client = ctx.obj
    
    try:
        supplier = SupplierDto(
            companyName=company_name,
            phone=phone,
            address=address,
            email=email,
            appUserId=app_user_id
        )
        client.create_supplier(supplier)
        console.print("[green]✓ Supplier created successfully[/green]")
    except ApiError as e:
        console.print(f"[red]✗ Failed to create supplier: {e}[/red]")
        raise typer.Exit(1)
    except Exception as e:
        console.print(f"[red]✗ Error: {e}[/red]")
        raise typer.Exit(1)


@app.command("me")
def get_me(
    ctx: typer.Context,
):
    """Get current user's supplier profile"""
    if ctx.obj is None:
        ctx.obj = ApiClient()
    client = ctx.obj
    
    try:
        supplier = client.get_me_supplier()
        display_supplier(supplier)
    except ApiError as e:
        console.print(f"[red]✗ Failed to get profile: {e}[/red]")
        raise typer.Exit(1)
    except Exception as e:
        console.print(f"[red]✗ Error: {e}[/red]")
        raise typer.Exit(1)