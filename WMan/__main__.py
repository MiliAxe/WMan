from typer import Typer

from WMan.CLI import product as product
from WMan.database import create_tables

app = Typer(no_args_is_help=True)
app.add_typer(
    product.app, name="product", help="Manage products and get product information"
)

if __name__ == "__main__":
    create_tables()
    app()
