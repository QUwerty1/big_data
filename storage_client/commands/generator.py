# commands/generator.py
import typer
from typing import Optional
from client import ApiClient
from rich.table import Table
from rich.console import Console

app = typer.Typer(help="Data Generator commands")
console = Console()

# commands/generator.py
from config import format_price  # Add this import at the top

def print_list_table(data, title="Generated Data"):
    table = Table(title=title)
    if not data:
        console.print("No data returned.")
        return
    
    # Dynamic columns based on first item keys
    if isinstance(data[0], dict):
        keys = list(data[0].keys())
        for k in keys:
            # Style price columns green
            if 'price' in k.lower():
                table.add_column(str(k), style="green", justify="right")
            else:
                table.add_column(str(k), style="magenta")
        
        for item in data:
            row_values = []
            for k in keys:
                val = item.get(k, '')
                # Format price fields
                if 'price' in k.lower() and isinstance(val, (int, float)):
                    row_values.append(format_price(val))
                # Format nested units (saleUnits/supplyUnits) as summary
                elif k in ('saleUnits', 'supplyUnits') and isinstance(val, list):
                    total = sum(unit.get('price', 0) * unit.get('amount', 0) for unit in val)
                    row_values.append(f"{len(val)} units\n{format_price(total)}")
                # Format dates (show only date part)
                elif 'date' in k.lower() and val:
                    row_values.append(str(val)[:10] if len(str(val)) > 10 else str(val))
                else:
                    row_values.append(str(val))
            table.add_row(*row_values)
        console.print(table)
    else:
        # Handle non-dict data (e.g., array of strings from /generator/users)
        table.add_column("Item", style="magenta")
        for item in data:
            table.add_row(str(item))
        console.print(table)

# commands/generator.py
@app.command("products")
def gen_products(
    count: int = typer.Option(1, "--count", "-c"),
    min_price: float = typer.Option(1, "--min-price"),
    max_price: float = typer.Option(1000000, "--max-price"),
    token: str = typer.Option(None, "--token", "-t")
):
    client = ApiClient(token=token)
    try:
        params = {
            "count": str(count),
            "minPrice": str(min_price),
            "maxPrice": str(max_price)
        }
        data = client.post("/generator/products", params=params)
        print_list_table(data, "Generated Products")
    except Exception as e:
        typer.echo(f"Error: {e}", err=True)
        raise typer.Exit(code=1)

@app.command("customers")
def gen_customers(
    count: int = typer.Option(1, "--count", "-c"),
    token: str = typer.Option(None, "--token", "-t")
):
    client = ApiClient(token=token)
    try:
        params = {"count": str(count)}
        data = client.post("/generator/customers", params=params)
        print_list_table(data, "Generated Customers")
    except Exception as e:
        typer.echo(f"Error: {e}", err=True)
        raise typer.Exit(code=1)

@app.command("suppliers")
def gen_suppliers(
    count: int = typer.Option(1, "--count", "-c"),
    token: str = typer.Option(None, "--token", "-t")
):
    client = ApiClient(token=token)
    try:
        params = {"count": str(count)}
        data = client.post("/generator/suppliers", params=params)
        print_list_table(data, "Generated Suppliers")
    except Exception as e:
        typer.echo(f"Error: {e}", err=True)
        raise typer.Exit(code=1)

@app.command("sales")
def gen_sales(
    count: int = typer.Option(1, "--count", "-c"),
    min_date: str = typer.Option(None, "--min-date"),
    max_date: str = typer.Option(None, "--max-date"),
    token: str = typer.Option(None, "--token", "-t")
):
    client = ApiClient(token=token)
    try:
        params = {"count": str(count)}
        if min_date:
            params["minDate"] = min_date
        if max_date:
            params["maxDate"] = max_date
        data = client.post("/generator/sales", params=params)
        print_list_table(data, "Generated Sales")
    except Exception as e:
        typer.echo(f"Error: {e}", err=True)
        raise typer.Exit(code=1)

@app.command("supplies")
def gen_supplies(
    count: int = typer.Option(1, "--count", "-c"),
    min_date: str = typer.Option(None, "--min-date"),
    max_date: str = typer.Option(None, "--max-date"),
    token: str = typer.Option(None, "--token", "-t")
):
    client = ApiClient(token=token)
    try:
        params = {"count": str(count)}
        if min_date:
            params["minDate"] = min_date
        if max_date:
            params["maxDate"] = max_date
        data = client.post("/generator/supplies", params=params)
        print_list_table(data, "Generated Supplies")
    except Exception as e:
        typer.echo(f"Error: {e}", err=True)
        raise typer.Exit(code=1)

@app.command("users")
def gen_users(
    count: int = typer.Option(1, "--count", "-c"),
    token: str = typer.Option(None, "--token", "-t")
):
    client = ApiClient(token=token)
    try:
        params = {"count": str(count)}
        data = client.post("/generator/users", params=params)
        print_list_table(data, "Generated Users")
    except Exception as e:
        typer.echo(f"Error: {e}", err=True)
        raise typer.Exit(code=1)