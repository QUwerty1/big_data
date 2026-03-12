# commands/supplier.py
import typer
from client import ApiClient
from dto import NewSupplier
from rich.table import Table
from rich.console import Console

app = typer.Typer(help="Supplier commands")
console = Console()

def print_supplier_table(data):
    if isinstance(data, list):
        table = Table(title="Suppliers")
        table.add_column("ID", style="cyan")
        table.add_column("Company", style="magenta")
        table.add_column("Phone")
        table.add_column("Email")
        for item in data:
            table.add_row(str(item.get('id', 'N/A')), item['companyName'], item['phone'], item['email'])
        console.print(table)
    else:
        table = Table(title="Supplier Details")
        table.add_column("Field", style="cyan")
        table.add_column("Value", style="magenta")
        for k, v in data.items():
            table.add_row(k, str(v))
        console.print(table)

@app.command("get")
def get_supplier(
    supplier_id: int = typer.Argument(None, help="Supplier ID"),
    token: str = typer.Option(None, "--token", "-t")
):
    if supplier_id is None:
        supplier_id = int(typer.prompt("Supplier ID"))
    client = ApiClient(token=token)
    try:
        data = client.get(f"/supplier/{supplier_id}")
        print_supplier_table(data)
    except Exception as e:
        typer.echo(f"Error: {e}", err=True)
        raise typer.Exit(code=1)

@app.command("get-all")
def get_all_suppliers(
    take: int = typer.Option(10, "--take"),
    skip: int = typer.Option(0, "--skip"),
    token: str = typer.Option(None, "--token", "-t")
):
    client = ApiClient(token=token)
    try:
        data = client.get("/supplier", params={"take": take, "skip": skip})
        print_supplier_table(data)
    except Exception as e:
        typer.echo(f"Error: {e}", err=True)
        raise typer.Exit(code=1)

@app.command("create")
def create_supplier(
    company_name: str = typer.Option(None, "--company-name", "-c"),
    phone: str = typer.Option(None, "--phone", "-p"),
    address: str = typer.Option(None, "--address", "-a"),
    email: str = typer.Option(None, "--email", "-e"),
    token: str = typer.Option(None, "--token", "-t")
):
    if not company_name: company_name = typer.prompt("Company Name")
    if not phone: phone = typer.prompt("Phone")
    if not address: address = typer.prompt("Address")
    if not email: email = typer.prompt("Email")

    client = ApiClient(token=token)
    body = NewSupplier(companyName=company_name, phone=phone, address=address, email=email).model_dump()
    try:
        data = client.post("/supplier", json=body)
        typer.echo("Supplier created successfully.")
        print_supplier_table(data)
    except Exception as e:
        typer.echo(f"Error: {e}", err=True)
        raise typer.Exit(code=1)

@app.command("me")
def me_supplier(token: str = typer.Option(None, "--token", "-t")):
    client = ApiClient(token=token)
    try:
        data = client.get("/supplier/me")
        print_supplier_table(data)
    except Exception as e:
        typer.echo(f"Error: {e}", err=True)
        raise typer.Exit(code=1)