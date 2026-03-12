import typer
import click
from typing import Optional
from rich.console import Console
from rich.table import Table

from client import ApiClient, ApiError

app = typer.Typer(help="Sale operations")
console = Console()


def _get_client() -> ApiClient:
    """Get ApiClient from context or create new one"""
    try:
        ctx = click.get_current_context()
        if ctx.obj is not None:
            return ctx.obj
    except (RuntimeError, AttributeError):
        pass
    return ApiClient()


@app.command("list")
def list_sales(
    take: Optional[int] = typer.Option(None, "--take", "-t", help="Number of sales to retrieve"),
    skip: int = typer.Option(0, "--skip", "-s", help="Number of sales to skip"),
):
    """List all sales"""
    client = _get_client()
    
    try:
        sales = client.get_all_sales()
        
        if not sales:
            console.print("[yellow]⚠ No sales found[/yellow]")
            return
        
        table = Table(show_header=True, header_style="bold magenta")
        table.add_column("ID", style="cyan")
        table.add_column("Customer ID", style="cyan")
        table.add_column("Real Date", style="green")
        table.add_column("Planned Date", style="green")
        table.add_column("Units", style="yellow")
        
        for sale in sales:
            units_count = len(sale.saleUnits) if sale.saleUnits else 0
            table.add_row(
                str(sale.id),
                str(sale.customerId),
                sale.realDate.strftime("%Y-%m-%d %H:%M:%S") if sale.realDate else "N/A",
                sale.plannedDate.strftime("%Y-%m-%d %H:%M:%S") if sale.plannedDate else "N/A",
                str(units_count)
            )
        
        console.print(table)
    except ApiError as e:
        console.print(f"[red]✗ Failed to list sales: {e}[/red]")
        raise typer.Exit(1)
    except Exception as e:
        console.print(f"[red]✗ Error: {e}[/red]")
        raise typer.Exit(1)


@app.command("get")
def get_sale(
    sale_id: int = typer.Argument(..., help="Sale ID"),
):
    """Get sale by ID"""
    client = _get_client()
    
    try:
        sale = client.get_sale(sale_id)
        
        # ✅ Table 1: Sale Information
        console.print("[bold]Sale Information[/bold]")
        sale_table = Table(show_header=True, header_style="bold magenta")
        sale_table.add_column("Field", style="cyan")
        sale_table.add_column("Value", style="green")
        
        sale_table.add_row("ID", str(sale.id))
        sale_table.add_row("Customer ID", str(sale.customerId))
        sale_table.add_row("Real Date", sale.realDate.strftime("%Y-%m-%d %H:%M:%S") if sale.realDate else "N/A")
        sale_table.add_row("Planned Date", sale.plannedDate.strftime("%Y-%m-%d %H:%M:%S") if sale.plannedDate else "N/A")
        
        console.print(sale_table)
        console.print()
        
        # ✅ Table 2: Sale Units
        console.print("[bold]Sale Units[/bold]")
        
        if sale.saleUnits and len(sale.saleUnits) > 0:
            units_table = Table(show_header=True, header_style="bold magenta")
            units_table.add_column("ID", style="cyan")
            units_table.add_column("Product ID", style="cyan")
            units_table.add_column("Amount", style="green")
            units_table.add_column("Price", style="green")
            units_table.add_column("Total", style="yellow")
            
            for unit in sale.saleUnits:
                total = unit.amount * unit.price
                units_table.add_row(
                    str(unit.id),
                    str(unit.productId),
                    str(unit.amount),
                    f"${unit.price:.2f}",
                    f"${total:.2f}"
                )
            
            console.print(units_table)
        else:
            console.print("[yellow]⚠ No sale units found[/yellow]")
            
    except ApiError as e:
        console.print(f"[red]✗ Failed to get sale: {e}[/red]")
        raise typer.Exit(1)
    except Exception as e:
        console.print(f"[red]✗ Error: {e}[/red]")
        raise typer.Exit(1)


@app.command("create")
def create_sale(
    customer_id: int = typer.Option(..., "--customer-id", "-c", help="Customer ID"),
    real_date: Optional[str] = typer.Option(None, "--real-date", "-r", help="Real date (YYYY-MM-DD HH:MM:SS)"),
    planned_date: Optional[str] = typer.Option(None, "--planned-date", "-p", help="Planned date (YYYY-MM-DD HH:MM:SS)"),
):
    """Create a new sale"""
    client = _get_client()
    
    try:
        from dto import SaleDto
        from datetime import datetime
        
        sale = SaleDto(
            id=0,
            customerId=customer_id,
            realDate=datetime.strptime(real_date, "%Y-%m-%d %H:%M:%S") if real_date else datetime.now(),
            plannedDate=datetime.strptime(planned_date, "%Y-%m-%d %H:%M:%S") if planned_date else datetime.now(),
            saleUnits=[]
        )
        
        client.create_sale(sale)
        console.print("[green]✓ Sale created successfully[/green]")
    except ApiError as e:
        console.print(f"[red]✗ Failed to create sale: {e}[/red]")
        raise typer.Exit(1)
    except Exception as e:
        console.print(f"[red]✗ Error: {e}[/red]")
        raise typer.Exit(1)