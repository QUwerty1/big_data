# commands/product.py
from typing import Any, Dict

import typer
from client import ApiClient
from rich.table import Table
from rich.console import Console

from config import format_price

app = typer.Typer(help="Product commands")
console = Console()

def format_rubles(value):
    return format_price(value)

def print_product_table(data):
    if isinstance(data, list):
        table = Table(title="Products")
        table.add_column("ID", style="cyan")
        table.add_column("Name", style="magenta")
        table.add_column("Price", justify="right")
        for item in data:
            table.add_row(str(item['id']), item['productName'], format_rubles(item['price']))
        console.print(table)
    else:
        table = Table(title="Product Details")
        table.add_column("Field", style="cyan")
        table.add_column("Value", style="magenta")
        for k, v in data.items():
            val = format_rubles(v) if k == 'price' else str(v)
            table.add_row(k, val)
        console.print(table)

@app.command("get")
def get_product(
    product_id: int = typer.Argument(None, help="Product ID"),
    token: str = typer.Option(None, "--token", "-t")
):
    if product_id is None:
        product_id = int(typer.prompt("Product ID"))
    client = ApiClient(token=token)
    try:
        data = client.get(f"/product/{product_id}")
        print_product_table(data)
    except Exception as e:
        typer.echo(f"Error: {e}", err=True)
        raise typer.Exit(code=1)

@app.command("get-all")
def get_all_products(token: str = typer.Option(None, "--token", "-t")):
    client = ApiClient(token=token)
    try:
        data = client.get("/product")
        print_product_table(data)
    except Exception as e:
        typer.echo(f"Error: {e}", err=True)
        raise typer.Exit(code=1)

@app.command("create")
def create_product(
    name: str = typer.Option(None, "--name", "-n"),
    price: float = typer.Option(None, "--price", "-p"),
    token: str = typer.Option(None, "--token", "-t")
):
    if not name: name = typer.prompt("Product Name")
    if price is None: price = float(typer.prompt("Price"))
    
    client = ApiClient(token=token)
    body = {"productName": name, "price": price}
    try:
        data = client.post("/product", json=body)
        typer.echo("Product created successfully.")
        print_product_table(data)
    except Exception as e:
        typer.echo(f"Error: {e}", err=True)
        raise typer.Exit(code=1)

@app.command("update")
def update_product(
    product_id: int = typer.Argument(None),
    name: str = typer.Option(None, "--name", "-n"),
    price: float = typer.Option(None, "--price", "-p"),
    token: str = typer.Option(None, "--token", "-t")
):
    if product_id is None:
        product_id = int(typer.prompt("Product ID"))
    if not name:
        name = typer.prompt("Product Name")
    if price is None:
        price = float(typer.prompt("Price"))
    
    client = ApiClient(token=token)
    body: Dict[str, Any] = {"id": product_id, "productName": name, "price": price}
    try:
        data = client.put("/product", json=body)
        typer.echo("✓ Product updated successfully.")
        # Fix: Only print table if data is returned (not None)
        if data:
            print_product_table(data)
        else:
            # Optionally fetch and display the updated product
            typer.echo(f"Product ID {product_id} has been updated.")
    except Exception as e:
        typer.echo(f"✗ Error: {e}", err=True)
        raise typer.Exit(code=1)