import typer

from WMan.CLI import product as product

app = typer.Typer(no_args_is_help=True)
app.add_typer(product.app, name="product", help="Manage products and get product information")

if __name__ == "__main__":
    app()
