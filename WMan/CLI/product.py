from typer import Typer, prompt
from typing import Optional

from WMan.database import ProductInfo
from WMan.ProductManager import ProductManager

app = Typer()


@app.command()
def add(
    interactive: bool = False,
    code: Optional[str] = None,
    description: Optional[str] = None,
    brand: Optional[str] = None,
    price: Optional[int] = None,
    count_in_carton: Optional[int] = None,
):
    """
    Add a new product
    """
    if interactive:
        code = prompt("Enter the product id")
        description = prompt("Enter the product description")
        brand = prompt("Enter the product brand")
        price = prompt("Enter the product price", type=int)
        count_in_carton = prompt("Enter the count in carton", type=int)
    pass

    new_product = ProductInfo(
        code=code,
        description=description,
        brand=brand,
        price=price,
        count_in_carton=count_in_carton,
    )

    ProductManager.add(new_product)


@app.command()
def add_batch(
    filepath: str,
    id_column: int = 1,
    description_column: int = 3,
    brand_column: int = 7,
    price_column: int = 4,
    count_in_carton: int = 2,
):
    """
    Add multiple products from a .xlsx file
    """
    indexes = ColumnIndexes(
        code_column=id_column,
        description_column=description_column,
        brand_column=brand_column,
        price_column=price_column,
        count_in_carton_column=count_in_carton
    )
    ProductManager.add_batch(
            filepath,
            indexes
    )


@app.command()
def list(
    output: Optional[str] = None,
    brand: Optional[str] = None,
    min_price: Optional[int] = None,
    max_price: Optional[int] = None,
):
    """
    List all products or specific products
    """
    ProductManager.list_products(
        output=output, filters= {
            "brand": brand,
            "min_price": min_price,
            "max_price": max_price
        }
    )
    pass

@app.command()
def remove(code: str):
    """
    Delete the product with the given code
    """
    ProductManager.remove(code)
    pass


@app.command()
def update(
    code: str,
    new_brand: Optional[str] = None,
    new_description: Optional[str] = None,
    new_price: Optional[int] = None,
    new_count_in_carton: Optional[int] = None,
):
    """
    Updates the given product with the new values
    """
    edited_product = ProductInfo(
        code=code,
        description=new_description,
        brand=new_brand,
        count_in_carton=new_count_in_carton,
        price=new_price,
    )
    ProductManager.update(code, edited_product)


@app.command()
def update_batch(
    filepath: str,
    id_column: int = 1,
    description_column: int = 3,
    brand_column: int = 7,
    price_column: int = 4,
    count_in_carton: int = 2,
):
    """
    Update multiple products from a .xlsx file
    """
    indexes = ColumnIndexes(
        code_column=id_column,
        description_column=description_column,
        brand_column=brand_column,
        price_column=price_column,
        count_in_carton_column=count_in_carton
    )

    ProductManager.update_batch(
        filepath,
        indexes,
    )
