import typer
from typing import Optional, List
from rich.console import Console
from rich.table import Table
from datetime import datetime

from client import ApiClient, ApiError
from dto import SupplyDto, SupplyUnitDto

app = typer.Typer(help="Supply commands")
console = Console()


def display_supply(supply: SupplyDto):
    """Display a single supply"""
    table = Table(title=f"Supply #{supply.id}")
    table.add_column("Property", style="cyan")
    table.add_column("Value", style="green")
    
    table.add_row("ID", str(supply.id) if supply.id else "N/A")
    table.add_row("Supplier ID", str(supply.supplierId) if supply.supplierId else "N/A")
    
    if supply.realDate:
        table.add_row("Real Date", supply.realDate.strftime("%Y-%m-%d %H:%M:%S"))
    if supply.plannedDate:
        table.add_row("Planned Date", supply.plannedDate.strftime("%Y-%m-%d %H:%M:%S"))
    
    if supply.supplyUnits:
        table.add_row("Units Count", str(len(supply.supplyUnits)))
        
        # Show units in a sub-table
        units_table = Table(title="Supply Units")
        units_table.add_column("ID", style="cyan")
        units_table.add_column("Product ID", style="blue")
        units_table.add_column("Amount", style="yellow")
        units_table.add_column("Price", style="green")
        
        for unit in supply.supplyUnits:
            units_table.add_row(
                str(unit.id),
                str(unit.productId),
                str(unit.amount),
                f"${unit.price:.2f}"
            )
        
        console.print(units_table)
    
    console.print(table)


def display_supplies(supplies: List[SupplyDto]):
    """Display a list of supplies"""
    if not supplies:
        console.print("[yellow]No supplies found[/yellow]")
        return
    
    table = Table(title="Supplies")
    table.add_column("ID", style="cyan", justify="right")
    table.add_column("Supplier ID", style="blue", justify="right")
    table.add_column("Real Date", style="green")
    table.add_column("Planned Date", style="yellow")
    table.add_column("Units", style="magenta", justify="right")
    
    for supply in supplies:
        table.add_row(
            str(supply.id) if supply.id else "N/A",
            str(supply.supplierId) if supply.supplierId else "N/A",
            supply.realDate.strftime("%Y-%m-%d") if supply.realDate else "N/A",
            supply.plannedDate.strftime("%Y-%m-%d") if supply.plannedDate else "N/A",
            str(len(supply.supplyUnits)) if supply.supplyUnits else "0"
        )
    
    console.print(table)


@app.command("get")
def get_supply(
    ctx: typer.Context,
    supply_id: int = typer.Argument(..., help="Supply ID"),
):
    """Get supply by ID"""
    if ctx.obj is None:
        ctx.obj = ApiClient()
    client = ctx.obj
    
    try:
        supply = client.get_supply(supply_id)
        display_supply(supply)
    except ApiError as e:
        console.print(f"[red]✗ Failed to get supply: {e}[/red]")
        raise typer.Exit(1)
    except Exception as e:
        console.print(f"[red]✗ Error: {e}[/red]")
        raise typer.Exit(1)


@app.command("get-all")
def get_all_supplies(
    ctx: typer.Context,
):
    """Get all supplies"""
    if ctx.obj is None:
        ctx.obj = ApiClient()
    client = ctx.obj
    
    try:
        supplies = client.get_all_supplies()
        display_supplies(supplies)
    except ApiError as e:
        console.print(f"[red]✗ Failed to get supplies: {e}[/red]")
        raise typer.Exit(1)
    except Exception as e:
        console.print(f"[red]✗ Error: {e}[/red]")
        raise typer.Exit(1)


@app.command("create")
def create_supply(
    ctx: typer.Context,
    supplier_id: Optional[int] = typer.Option(None, "--supplier-id", "-s", help="Supplier ID"),
    real_date: Optional[str] = typer.Option(None, "--real-date", "-r", help="Real date (YYYY-MM-DD HH:MM:SS)"),
    planned_date: Optional[str] = typer.Option(None, "--planned-date", "-p", help="Planned date (YYYY-MM-DD HH:MM:SS)"),
):
    """Create a new supply"""
    if ctx.obj is None:
        ctx.obj = ApiClient()
    client = ctx.obj
    
    try:
        supply = SupplyDto(
            supplierId=supplier_id,
            realDate=datetime.strptime(real_date, "%Y-%m-%d %H:%M:%S") if real_date else None,
            plannedDate=datetime.strptime(planned_date, "%Y-%m-%d %H:%M:%S") if planned_date else None,
            supplyUnits=[]
        )
        client.create_supply(supply)
        console.print("[green]✓ Supply created successfully[/green]")
    except ApiError as e:
        console.print(f"[red]✗ Failed to create supply: {e}[/red]")
        raise typer.Exit(1)
    except Exception as e:
        console.print(f"[red]✗ Error: {e}[/red]")
        raise typer.Exit(1)


@app.command("update")
def update_supply(
    ctx: typer.Context,
    supply_id: int = typer.Option(..., "--id", "-i", help="Supply ID"),
    supplier_id: Optional[int] = typer.Option(None, "--supplier-id", "-s", help="Supplier ID"),
    real_date: Optional[str] = typer.Option(None, "--real-date", "-r", help="Real date (YYYY-MM-DD HH:MM:SS)"),
    planned_date: Optional[str] = typer.Option(None, "--planned-date", "-p", help="Planned date (YYYY-MM-DD HH:MM:SS)"),
):
    """Update an existing supply"""
    if ctx.obj is None:
        ctx.obj = ApiClient()
    client = ctx.obj
    
    try:
        existing = client.get_supply(supply_id)
        
        if supplier_id:
            existing.supplierId = supplier_id
        if real_date:
            existing.realDate = datetime.strptime(real_date, "%Y-%m-%d %H:%M:%S")
        if planned_date:
            existing.plannedDate = datetime.strptime(planned_date, "%Y-%m-%d %H:%M:%S")
        
        client.update_supply(existing)
        console.print("[green]✓ Supply updated successfully[/green]")
    except ApiError as e:
        console.print(f"[red]✗ Failed to update supply: {e}[/red]")
        raise typer.Exit(1)
    except Exception as e:
        console.print(f"[red]✗ Error: {e}[/red]")
        raise typer.Exit(1)