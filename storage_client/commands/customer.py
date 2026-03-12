# commands/customer.py
import typer
import json
from client import ApiClient
from dto import NewCustomer

app = typer.Typer(help="Customer commands")

@app.command("get")
def get_customer(customer_id: int = typer.Argument(...), 
                 token: str = typer.Option(None, "--token")):
    """Get a specific customer by ID."""
    client = ApiClient(token=token)
    try:
        data = client.get(f"/customer/{customer_id}")
        typer.echo(json.dumps(data, indent=2))
    except Exception as e:
        typer.echo(f"Error: {e}", err=True)
        raise typer.Exit(code=1)

@app.command("get-all")
def get_all_customers(take: int = typer.Option(10, "--take"), 
                      skip: int = typer.Option(0, "--skip"),
                      token: str = typer.Option(None, "--token")):
    """List customers with pagination."""
    client = ApiClient(token=token)
    try:
        data = client.get("/customer", params={"take": take, "skip": skip})
        typer.echo(json.dumps(data, indent=2))
    except Exception as e:
        typer.echo(f"Error: {e}", err=True)
        raise typer.Exit(code=1)

@app.command("create")
def create_customer(companyName: str = typer.Option(...), 
                    phone: str = typer.Option(...), 
                    address: str = typer.Option(...), 
                    email: str = typer.Option(...),
                    token: str = typer.Option(None, "--token")):
    """Create a new customer."""
    client = ApiClient(token=token)
    body = NewCustomer(companyName=companyName, phone=phone, address=address, email=email).model_dump()
    try:
        data = client.post("/customer", json=body)
        typer.echo("Customer created successfully.")
        typer.echo(json.dumps(data, indent=2))
    except Exception as e:
        typer.echo(f"Error: {e}", err=True)
        raise typer.Exit(code=1)

@app.command("me")
def me_customer(token: str = typer.Option(..., "--token")):
    """Get current customer details."""
    client = ApiClient(token=token)
    try:
        data = client.get("/customer/me")
        typer.echo(json.dumps(data, indent=2))
    except Exception as e:
        typer.echo(f"Error: {e}", err=True)
        raise typer.Exit(code=1)