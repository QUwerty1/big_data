import typer
from typing import Optional
from rich.console import Console
from rich.table import Table
from datetime import datetime

from client import ApiClient, ApiError
from commands.customer import display_customers
from commands.supplier import display_suppliers
from commands.product import display_products
from commands.sale import display_sales

app = typer.Typer(help="Generator commands")
console = Console()


@app.command("users")
def generate_users(
    ctx: typer.Context,
    count: int = typer.Option(
        1, "--count", "-c", help="Number of users to generate"
    ),
):
    """Generate random users"""
    if ctx.obj is None:
        ctx.obj = ApiClient()
    client = ctx.obj

    try:
        users = client.generate_users(count)

        table = Table(title=f"Generated {len(users)} Users")
        table.add_column("#", style="cyan", justify="right")
        table.add_column("Username", style="green")

        for i, username in enumerate(users, 1):
            table.add_row(str(i), username)

        console.print(table)
    except ApiError as e:
        console.print(f"[red]✗ Failed to generate users: {e}[/red]")
        raise typer.Exit(1)
    except Exception as e:
        console.print(f"[red]✗ Error: {e}[/red]")
        raise typer.Exit(1)


@app.command("customers")
def generate_customers(
    ctx: typer.Context,
    count: int = typer.Option(
        1, "--count", "-c", help="Number of customers to generate"
    ),
):
    """Generate random customers"""
    if ctx.obj is None:
        ctx.obj = ApiClient()
    client = ctx.obj

    try:
        customers = client.generate_customers(count)
        console.print(f"[green]✓ Generated {len(customers)} customers[/green]")
        display_customers(customers)
    except ApiError as e:
        console.print(f"[red]✗ Failed to generate customers: {e}[/red]")
        raise typer.Exit(1)
    except Exception as e:
        console.print(f"[red]✗ Error: {e}[/red]")
        raise typer.Exit(1)


@app.command("suppliers")
def generate_suppliers(
    ctx: typer.Context,
    count: int = typer.Option(
        1, "--count", "-c", help="Number of suppliers to generate"
    ),
):
    """Generate random suppliers"""
    if ctx.obj is None:
        ctx.obj = ApiClient()
    client = ctx.obj

    try:
        suppliers = client.generate_suppliers(count)
        console.print(f"[green]✓ Generated {len(suppliers)} suppliers[/green]")
        display_suppliers(suppliers)
    except ApiError as e:
        console.print(f"[red]✗ Failed to generate suppliers: {e}[/red]")
        raise typer.Exit(1)
    except Exception as e:
        console.print(f"[red]✗ Error: {e}[/red]")
        raise typer.Exit(1)


@app.command("products")
def generate_products(
    ctx: typer.Context,
    count: int = typer.Option(
        1, "--count", "-c", help="Number of products to generate"
    ),
    min_price: float = typer.Option(
        1.0, "--min-price", "-min", help="Minimum price"
    ),
    max_price: float = typer.Option(
        1000000.0, "--max-price", "-max", help="Maximum price"
    ),
):
    """Generate random products"""
    if ctx.obj is None:
        ctx.obj = ApiClient()
    client = ctx.obj

    try:
        products = client.generate_products(count, min_price, max_price)
        console.print(f"[green]✓ Generated {len(products)} products[/green]")
        display_products(products)
    except ApiError as e:
        console.print(f"[red]✗ Failed to generate products: {e}[/red]")
        raise typer.Exit(1)
    except Exception as e:
        console.print(f"[red]✗ Error: {e}[/red]")
        raise typer.Exit(1)


@app.command("sales")
def generate_sales(
    ctx: typer.Context,
    count: int = typer.Option(
        1, "--count", "-c", help="Number of sales to generate"
    ),
    min_date: Optional[str] = typer.Option(
        None, "--min-date", "-md", help="Minimum date (YYYY-MM-DD)"
    ),
    max_date: Optional[str] = typer.Option(
        None, "--max-date", "-xd", help="Maximum date (YYYY-MM-DD)"
    ),
):
    """Generate random sales"""
    if ctx.obj is None:
        ctx.obj = ApiClient()
    client = ctx.obj

    try:
        min_date_dt = (
            datetime.strptime(min_date, "%Y-%m-%d") if min_date else None
        )
        max_date_dt = (
            datetime.strptime(max_date, "%Y-%m-%d") if max_date else None
        )

        sales = client.generate_sales(count, min_date_dt, max_date_dt)
        console.print(f"[green]✓ Generated {len(sales)} sales[/green]")
        display_sales(sales)
    except ApiError as e:
        console.print(f"[red]✗ Failed to generate sales: {e}[/red]")
        raise typer.Exit(1)
    except Exception as e:
        console.print(f"[red]✗ Error: {e}[/red]")
        raise typer.Exit(1)
