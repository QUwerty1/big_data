import typer
from typing import Optional, List
from rich.console import Console
from rich.table import Table

from client import ApiClient, ApiError
from dto import CustomerDto

app = typer.Typer(help="Customer commands")
console = Console()

def display_customer(customer: CustomerDto):
    """Display a single customer"""
    table = Table(title=f"Customer #{customer.id}")
    table.add_column("Property", style="cyan")
    table.add_column("Value", style="green")
    
    table.add_row("ID", str(customer.id))
    table.add_row("Company Name", customer.companyName)
    table.add_row("Phone", customer.phone)
    table.add_row("Address", customer.address)
    table.add_row("Email", customer.email)
    table.add_row("App User ID", customer.appUserId)
    
    if customer.sales:
        table.add_row("Sales Count", str(len(customer.sales)))
    
    console.print(table)


def display_customers(customers: List[CustomerDto]):
    """Display a list of customers"""
    if not customers:
        console.print("[yellow]No customers found[/yellow]")
        return
    
    table = Table(title="Customers")
    table.add_column("ID", style="cyan", justify="right")
    table.add_column("Company Name", style="green")
    table.add_column("Phone", style="blue")
    table.add_column("Email", style="magenta")
    
    for customer in customers:
        table.add_row(
            str(customer.id),
            customer.companyName,
            customer.phone,
            customer.email
        )
    
    console.print(table)


@app.command("get")
def get_customer(
    ctx: typer.Context,
    customer_id: int = typer.Argument(..., help="Customer ID"),
):
    """Get customer by ID"""
    if ctx.obj is None:
        ctx.obj = ApiClient()
    client = ctx.obj
    
    try:
        customer = client.get_customer(customer_id)
        display_customer(customer)
    except ApiError as e:
        console.print(f"[red]✗ Failed to get customer: {e}[/red]")
        raise typer.Exit(1)
    except Exception as e:
        console.print(f"[red]✗ Error: {e}[/red]")
        raise typer.Exit(1)


@app.command("get-all")
def get_all_customers(
    ctx: typer.Context,
    take: Optional[int] = typer.Option(None, "--take", "-t", help="Number of customers to take"),
    skip: int = typer.Option(0, "--skip", "-s", help="Number of customers to skip"),
):
    """Get all customers with pagination"""
    if ctx.obj is None:
        ctx.obj = ApiClient()
    client = ctx.obj
    
    try:
        customers = client.get_all_customers(take=take, skip=skip)
        display_customers(customers)
    except ApiError as e:
        console.print(f"[red]✗ Failed to get customers: {e}[/red]")
        raise typer.Exit(1)
    except Exception as e:
        console.print(f"[red]✗ Error: {e}[/red]")
        raise typer.Exit(1)


@app.command("create")
def create_customer(
    ctx: typer.Context,
    company_name: str = typer.Option(..., "--company", "-c", help="Company name"),
    phone: str = typer.Option(..., "--phone", "-p", help="Phone number"),
    address: str = typer.Option(..., "--address", "-a", help="Address"),
    email: str = typer.Option(..., "--email", "-e", help="Email"),
    app_user_id: str = typer.Option(..., "--app-user-id", "-u", help="App User ID"),
):
    """Create a new customer"""
    if ctx.obj is None:
        ctx.obj = ApiClient()
    client = ctx.obj
    
    try:
        customer = CustomerDto(
            id=0,
            companyName=company_name,
            phone=phone,
            address=address,
            email=email,
            appUserId=app_user_id
        )
        client.create_customer(customer)
        console.print("[green]✓ Customer created successfully[/green]")
    except ApiError as e:
        console.print(f"[red]✗ Failed to create customer: {e}[/red]")
        raise typer.Exit(1)
    except Exception as e:
        console.print(f"[red]✗ Error: {e}[/red]")
        raise typer.Exit(1)


@app.command("me")
def get_me(
    ctx: typer.Context,
):
    """Get current user's customer profile"""
    if ctx.obj is None:
        ctx.obj = ApiClient()
    client = ctx.obj
    
    try:
        customer = client.get_me_customer()
        display_customer(customer)
    except ApiError as e:
        console.print(f"[red]✗ Failed to get profile: {e}[/red]")
        raise typer.Exit(1)
    except Exception as e:
        console.print(f"[red]✗ Error: {e}[/red]")
        raise typer.Exit(1)