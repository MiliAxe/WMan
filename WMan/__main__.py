from typer import Typer

from WMan.CLI import availability as availability
from WMan.CLI import customer as customer
from WMan.CLI import product as product
from WMan.database import create_tables

app = Typer(no_args_is_help=True)
app.add_typer(
    product.app, name="product", help="Manage products and get product information"
)
app.add_typer(
    availability.app,
    name="availability",
    help="Manage and get availability of products",
)
app.add_typer(
    customer.app,
    name="customer",
    help="Manage and get information about customers",
)

if __name__ == "__main__":
    create_tables()
    app()
