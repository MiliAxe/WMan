from typer import Typer

from WMan.CustomerManager import CustomerManager

app = Typer()


@app.command()
def create(name: str):
    """
    Create a customer with the specified name.
    """
    CustomerManager.create(name)


# TODO: add cool filters to this command
@app.command()
def list():
    """
    List all the customers with their corresponding names and IDs
    """
    CustomerManager.list({})
