import typer
from typing import Optional, List
from rich.console import Console
from rich.table import Table

from client import ApiClient, ApiError
from dto import ProductDto

app = typer.Typer(help="Product commands")
console = Console()


def display_product(product: ProductDto):
    """Display a single product"""
    table = Table(title=f"Product #{product.id}")
    table.add_column("Property", style="cyan")
    table.add_column("Value", style="green")
    
    table.add_row("ID", str(product.id))
    table.add_row("Product Name", product.productName)
    table.add_row("Price", f"{product.price:.2f} руб.")
    
    console.print(table)


def display_products(products: List[ProductDto]):
    """Display a list of products"""
    if not products:
        console.print("[yellow]No products found[/yellow]")
        return
    
    table = Table(title="Products")
    table.add_column("ID", style="cyan", justify="right")
    table.add_column("Product Name", style="green")
    table.add_column("Price", style="yellow", justify="right")
    
    for product in products:
        table.add_row(
            str(product.id),
            product.productName,
            f"{product.price:.2f} руб."
        )
    
    console.print(table)


@app.command("get")
def get_product(
    ctx: typer.Context,
    product_id: int = typer.Argument(..., help="Product ID"),
):
    """Get product by ID"""
    if ctx.obj is None:
        ctx.obj = ApiClient()
    client = ctx.obj
    
    try:
        product = client.get_product(product_id)
        display_product(product)
    except ApiError as e:
        console.print(f"[red]✗ Failed to get product: {e}[/red]")
        raise typer.Exit(1)
    except Exception as e:
        console.print(f"[red]✗ Error: {e}[/red]")
        raise typer.Exit(1)


@app.command("get-all")
def get_all_products(
    ctx: typer.Context,
):
    """Get all products"""
    if ctx.obj is None:
        ctx.obj = ApiClient()
    client = ctx.obj
    
    try:
        products = client.get_all_products()
        display_products(products)
    except ApiError as e:
        console.print(f"[red]✗ Failed to get products: {e}[/red]")
        raise typer.Exit(1)
    except Exception as e:
        console.print(f"[red]✗ Error: {e}[/red]")
        raise typer.Exit(1)


@app.command("create")
def create_product(
    ctx: typer.Context,
    product_name: str = typer.Option(..., "--name", "-n", help="Product name"),
    price: float = typer.Option(..., "--price", "-p", help="Product price"),
):
    """Create a new product"""
    if ctx.obj is None:
        ctx.obj = ApiClient()
    client = ctx.obj
    
    try:
        product = ProductDto(
            id=0,
            productName=product_name,
            price=price
        )
        client.create_product(product)
        console.print("[green]✓ Product created successfully[/green]")
    except ApiError as e:
        console.print(f"[red]✗ Failed to create product: {e}[/red]")
        raise typer.Exit(1)
    except Exception as e:
        console.print(f"[red]✗ Error: {e}[/red]")
        raise typer.Exit(1)


@app.command("update")
def update_product(
    ctx: typer.Context,
    product_id: int = typer.Option(..., "--id", "-i", help="Product ID"),
    product_name: Optional[str] = typer.Option(None, "--name", "-n", help="Product name"),
    price: Optional[float] = typer.Option(None, "--price", "-p", help="Product price"),
):
    """Update an existing product"""
    if ctx.obj is None:
        ctx.obj = ApiClient()
    client = ctx.obj
    
    try:
        existing = client.get_product(product_id)
        
        if product_name:
            existing.productName = product_name
        if price:
            existing.price = price
        
        client.update_product(existing)
        console.print("[green]✓ Product updated successfully[/green]")
    except ApiError as e:
        console.print(f"[red]✗ Failed to update product: {e}[/red]")
        raise typer.Exit(1)
    except Exception as e:
        console.print(f"[red]✗ Error: {e}[/red]")
        raise typer.Exit(1)