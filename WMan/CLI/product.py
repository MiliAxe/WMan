import os
import sys
from typing import Optional

import typer

from WMan.ProductManager import ProductManager
from WMan.database import ProductInfo

sys.path.insert(0, os.path.abspath(os.path.join(os.path.dirname(__file__), '../../')))

app = typer.Typer()


@app.command()
def add(interactive: bool = False, code: Optional[str] = None, description: Optional[str] = None,
        brand: Optional[str] = None, price: Optional[float] = None, count_in_carton: Optional[int] = None):
    """
    Add a new product
    """
    if interactive:
        code = typer.prompt("Enter the product id")
        description = typer.prompt("Enter the product description")
        brand = typer.prompt("Enter the product brand")
        price = typer.prompt("Enter the product price", type=float)
        count_in_carton = typer.prompt("Enter the count in carton", type=int)
    pass

    new_product = ProductInfo(
        code=code,
        description=description,
        brand=brand,
        price=price,
        count_in_carton=count_in_carton
    )

    ProductManager.add(new_product)


@app.command()
def add_batch(filepath: str, id_column: int = 1, description_column: int = 3, brand_column: int = 7,
              price_column: int = 4, count_in_carton: int = 2):
    """
    Add multiple products from a file
    """
    ProductManager.add_batch(filepath, id_column, description_column, brand_column, price_column, count_in_carton)


@app.command()
def list(brand: Optional[str] = None, min_price: Optional[float] = None, max_price: Optional[float] = None):
    """
    List all products or specific products
    """
    ProductManager.list(brand=brand, min_price=min_price, max_price=max_price)
    pass


@app.command()
def remove(code: str):
    """
    Delete the product with the given code
    """
    ProductManager.remove(code)
    pass
