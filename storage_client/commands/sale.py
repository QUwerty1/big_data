# commands/sale.py
import typer
from typing import Optional, Dict, Any
from client import ApiClient
from rich.table import Table
from rich.console import Console
import rich

from config import format_price

app = typer.Typer(help="Sale commands")
console = Console()

def print_sale_table(data, show_units=False):
    if isinstance(data, list):
        table = Table(title="Sales")
        table.add_column("ID", style="cyan")
        table.add_column("Customer ID", style="magenta")
        table.add_column("Planned Date")
        table.add_column("Real Date")
        table.add_column("Total", style="green", justify="right")
        for item in data:
            total = 0
            # Check for saleUnits (SaleDto) or saleUnitIds (SaleViewDto)
            if 'saleUnits' in item and item['saleUnits']:
                total = sum(unit.get('price', 0) * unit.get('amount', 0) for unit in item['saleUnits'])
            elif 'saleUnitIds' in item and item['saleUnitIds']:
                # For SaleViewDto, we only have IDs, cannot calculate total
                total = 0
            table.add_row(
                str(item.get('id', 'N/A')),
                str(item.get('customerId', 'N/A')),
                str(item.get('plannedDate', '-'))[:10] if item.get('plannedDate') else '-',
                str(item.get('realDate', '-'))[:10] if item.get('realDate') else '-',
                format_price(total)
            )
        console.print(table)
    else:
        table = Table(title="Sale Details")
        table.add_column("Field", style="cyan")
        table.add_column("Value", style="magenta")
        for k, v in data.items():
            if k == 'saleUnits' and isinstance(v, list):
                continue  # Skip saleUnits, will show in separate table
            elif k == 'saleUnitIds' and isinstance(v, list):
                continue  # Skip saleUnitIds
            elif 'price' in k.lower() and isinstance(v, (int, float)):
                table.add_row(k, format_price(v))
            elif 'date' in k.lower() and v:
                table.add_row(k, str(v)[:10])
            else:
                table.add_row(k, str(v))
        console.print(table)

        # Show saleUnits if present (SaleDto)
        if 'saleUnits' in data and data['saleUnits']:
            units_table = Table(title="Sale Units", box=rich.box.DOUBLE_EDGE) # type: ignore
            units_table.add_column("ID", style="cyan", justify="right")
            units_table.add_column("Product ID", style="magenta", justify="right")
            units_table.add_column("Amount", justify="right")
            units_table.add_column("Price", style="green", justify="right")
            units_table.add_column("Total", style="green", justify="right")

            grand_total = 0
            for unit in data['saleUnits']:
                unit_total = unit.get('price', 0) * unit.get('amount', 0)
                grand_total += unit_total
                units_table.add_row(
                    str(unit.get('id', 'N/A')),
                    str(unit.get('productId', 'N/A')),
                    str(unit.get('amount', 0)),
                    format_price(unit.get('price', 0)),
                    format_price(unit_total)
                )

            # Add total row
            units_table.add_row(
                "", "", "", "Grand Total:", format_price(grand_total),
                style="bold"
            )

            console.print()  # Empty line between tables
            console.print(units_table)

@app.command("get")
def get_sale(
    sale_id: int = typer.Argument(None, help="Sale ID"),
    token: str = typer.Option(None, "--token", "-t")
):
    """Get a specific sale by ID."""
    if sale_id is None:
        sale_id = int(typer.prompt("Sale ID"))
    client = ApiClient(token=token)
    try:
        data = client.get(f"/sale/{sale_id}")
        print_sale_table(data)
    except Exception as e:
        typer.echo(f"Error: {e}", err=True)
        raise typer.Exit(code=1)

@app.command("get-all")
def get_all_sales(
    take: int = typer.Option(10, "--take"),
    skip: int = typer.Option(0, "--skip"),
    token: str = typer.Option(None, "--token", "-t")
):
    """List all sales with pagination."""
    client = ApiClient(token=token)
    try:
        data = client.get("/sale")
        print_sale_table(data)
    except Exception as e:
        typer.echo(f"Error: {e}", err=True)
        raise typer.Exit(code=1)

@app.command("create")
def create_sale(
    customer_id: int = typer.Option(None, "--customer-id", "-c"),
    planned_date: str = typer.Option(None, "--planned-date", "-d"),
    real_date: str = typer.Option(None, "--real-date", "-r"),
    token: str = typer.Option(None, "--token", "-t")
):
    """Create a new sale."""
    if customer_id is None:
        customer_id = int(typer.prompt("Customer ID"))
    if not planned_date:
        planned_date = typer.prompt("Planned Date (YYYY-MM-DD)", default="")
    if not real_date:
        real_date = typer.prompt("Real Date (YYYY-MM-DD)", default="")
    
    client = ApiClient(token=token)
    # Fix: Explicitly type the dictionary as Dict[str, Any]
    body: Dict[str, Any] = {
        "customerId": customer_id,
        "plannedDate": planned_date if planned_date else None,
        "realDate": real_date if real_date else None
    }
    # Remove None values to match API expectations
    body = {k: v for k, v in body.items() if v is not None}
    
    try:
        data = client.post("/sale", json=body)
        typer.echo("Sale created successfully.")
        print_sale_table(data)
    except Exception as e:
        typer.echo(f"Error: {e}", err=True)
        raise typer.Exit(code=1)

@app.command("update")
def update_sale(
    sale_id: int = typer.Argument(None),
    customer_id: int = typer.Option(None, "--customer-id", "-c"),
    planned_date: str = typer.Option(None, "--planned-date", "-d"),
    real_date: str = typer.Option(None, "--real-date", "-r"),
    token: str = typer.Option(None, "--token", "-t")
):
    """Update an existing sale."""
    if sale_id is None:
        sale_id = int(typer.prompt("Sale ID"))
    if customer_id is None:
        customer_id = int(typer.prompt("Customer ID"))
    if not planned_date:
        planned_date = typer.prompt("Planned Date (YYYY-MM-DD)", default="")
    if not real_date:
        real_date = typer.prompt("Real Date (YYYY-MM-DD)", default="")
    
    client = ApiClient(token=token)
    # Fix: Explicitly type the dictionary as Dict[str, Any]
    body: Dict[str, Any] = {
        "id": sale_id,
        "customerId": customer_id,
        "plannedDate": planned_date if planned_date else None,
        "realDate": real_date if real_date else None
    }
    # Remove None values to match API expectations
    body = {k: v for k, v in body.items() if v is not None}
    
    try:
        data = client.put("/sale", json=body)
        typer.echo("✓ Sale updated successfully.")
        if data:
            print_sale_table(data)
        else:
            typer.echo(f"Sale ID {sale_id} has been updated.")
    except Exception as e:
        typer.echo(f"Error: {e}", err=True)
        raise typer.Exit(code=1)