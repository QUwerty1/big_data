# commands/supply.py
import typer
import rich
from typing import Any, Dict, Optional
from client import ApiClient
from rich.table import Table
from rich.console import Console

app = typer.Typer(help="Supply commands")
console = Console()

# commands/supply.py
from config import format_price  # Add this import at the top

def print_supply_table(data):
    if isinstance(data, list):
        table = Table(title="Supplies")
        table.add_column("ID", style="cyan")
        table.add_column("Supplier ID", style="magenta")
        table.add_column("Planned Date")
        table.add_column("Real Date")
        table.add_column("Total", style="green", justify="right")
        for item in data:
            total = 0
            # Check for supplyUnits (SupplyDto) or supplyUnitIds (SupplyViewDto)
            if 'supplyUnits' in item and item['supplyUnits']:
                total = sum(unit.get('price', 0) * unit.get('amount', 0) for unit in item['supplyUnits'])
            elif 'supplyUnitIds' in item and item['supplyUnitIds']:
                # For SupplyViewDto, we only have IDs, cannot calculate total
                total = 0
            table.add_row(
                str(item.get('id', 'N/A')),
                str(item.get('supplierId', 'N/A')),
                str(item.get('plannedDate', '-'))[:10] if item.get('plannedDate') else '-',
                str(item.get('realDate', '-'))[:10] if item.get('realDate') else '-',
                format_price(total)
            )
        console.print(table)
    else:
        # Main supply details table
        table = Table(title="Supply Details")
        table.add_column("Field", style="cyan")
        table.add_column("Value", style="magenta")
        for k, v in data.items():
            if k == 'supplyUnits' and isinstance(v, list):
                continue  # Skip supplyUnits, will show in separate table
            elif k == 'supplyUnitIds' and isinstance(v, list):
                continue  # Skip supplyUnitIds
            elif 'price' in k.lower() and isinstance(v, (int, float)):
                table.add_row(k, format_price(v))
            elif 'date' in k.lower() and v:
                table.add_row(k, str(v)[:10])
            else:
                table.add_row(k, str(v))
        console.print(table)

        # Second table: Supply Units
        if 'supplyUnits' in data and data['supplyUnits']:
            units_table = Table(title="Supply Units", box=rich.box.DOUBLE_EDGE) # type: ignore
            units_table.add_column("ID", style="cyan", justify="right")
            units_table.add_column("Product ID", style="magenta", justify="right")
            units_table.add_column("Amount", justify="right")
            units_table.add_column("Price", style="green", justify="right")
            units_table.add_column("Total", style="green", justify="right")

            grand_total = 0
            for unit in data['supplyUnits']:
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
def get_supply(
    supply_id: int = typer.Argument(None, help="Supply ID"),
    token: str = typer.Option(None, "--token", "-t")
):
    if supply_id is None:
        supply_id = int(typer.prompt("Supply ID"))
    client = ApiClient(token=token)
    try:
        data = client.get(f"/supply/{supply_id}")
        print_supply_table(data)
    except Exception as e:
        typer.echo(f"Error: {e}", err=True)
        raise typer.Exit(code=1)

@app.command("get-all")
def get_all_supplies(token: str = typer.Option(None, "--token", "-t")):
    client = ApiClient(token=token)
    try:
        data = client.get("/supply")
        print_supply_table(data)
    except Exception as e:
        typer.echo(f"Error: {e}", err=True)
        raise typer.Exit(code=1)

@app.command("create")
def create_supply(
    supplier_id: int = typer.Option(None, "--supplier-id", "-s"),
    planned_date: str = typer.Option(None, "--planned-date", "-d"),
    real_date: str = typer.Option(None, "--real-date", "-r"),
    token: str = typer.Option(None, "--token", "-t")
):
    if supplier_id is None:
        supplier_id = int(typer.prompt("Supplier ID"))
    if not planned_date:
        planned_date = typer.prompt("Planned Date (YYYY-MM-DD)", default="")
    if not real_date:
        real_date = typer.prompt("Real Date (YYYY-MM-DD)", default="")
    
    client = ApiClient(token=token)
    # Fix: Explicitly type the dictionary
    body: Dict[str, Any] = {
        "supplierId": supplier_id,
        "plannedDate": planned_date if planned_date else None,
        "realDate": real_date if real_date else None
    }
    body = {k: v for k, v in body.items() if v is not None}
    
    try:
        data = client.post("/supply", json=body)
        typer.echo("Supply created successfully.")
        print_supply_table(data)
    except Exception as e:
        typer.echo(f"Error: {e}", err=True)
        raise typer.Exit(code=1)
    
@app.command("update")
def update_supply(
    supply_id: int = typer.Argument(None, help="Supply ID"),
    supplier_id: int = typer.Option(None, "--supplier-id", "-s"),
    planned_date: str = typer.Option(None, "--planned-date", "-d"),
    real_date: str = typer.Option(None, "--real-date", "-r"),
    token: str = typer.Option(None, "--token", "-t")
):
    """Update an existing supply."""
    if supply_id is None:
        supply_id = int(typer.prompt("Supply ID"))
    if supplier_id is None:
        supplier_id = int(typer.prompt("Supplier ID"))
    if not planned_date:
        planned_date = typer.prompt("Planned Date (YYYY-MM-DD)", default="")
    if not real_date:
        real_date = typer.prompt("Real Date (YYYY-MM-DD)", default="")
    
    client = ApiClient(token=token)
    body: Dict[str, Any] = {
        "id": supply_id,
        "supplierId": supplier_id,
        "plannedDate": planned_date if planned_date else None,
        "realDate": real_date if real_date else None
    }
    # Remove None values to match API expectations
    body = {k: v for k, v in body.items() if v is not None}
    
    try:
        data = client.put("/supply", json=body)
        typer.echo("✓ Supply updated successfully.")
        if data:
            print_supply_table(data)
        else:
            typer.echo(f"Supply ID {supply_id} has been updated.")
    except Exception as e:
        typer.echo(f"✗ Error: {e}", err=True)
        raise typer.Exit(code=1)