from typing import Optional

from typer import Typer, prompt, Argument
from typing_extensions import Annotated
from WMan.ProductManager import ProductManager, ColumnIndexes
from WMan.database import ProductInfo

app = Typer()


@app.command()
def add(code: str, count: Annotated[int, Argument(min=1)]):
    """
    Add AMOUNT to the specified product's availability
    """
    product_to_add = ProductInfo(code=code, count=count)
    ProductManager.add_count(product_to_add)


@app.command()
def add_batch(filepath: str, code_column_index: int = 1, count_column_index: int = 2):
    """
    Add to the availability of the product from the specified file
    """
    indexes = ColumnIndexes(code_column=code_column_index, count_column=count_column_index)
    ProductManager.add_count_batch(filepath, indexes)


@app.command()
def reduce(code: str, amount: int):
    """
    Reduce AMOUNT from the specified product's availability
    """
    product_to_reduce = ProductInfo(code=code, count=amount)
    ProductManager.reduce_count(product_to_reduce)


@app.command()
def reduce_batch(
    filepath: str, code_column_index: int = 1, count_column_index: int = 2
):
    """
    Reduce the availability of the products from the specified file
    """
    indexes = ColumnIndexes(code_column=code_column_index, count_column=count_column_index)
    ProductManager.reduce_count_batch(filepath, indexes)



@app.command()
def list(
    output: Optional[str] = None,
    min_price: Optional[int] = None,
    max_price: Optional[int] = None,
    min_count: Optional[int] = None,
    max_count: Optional[int] = None,
    brand: Optional[str] = None,
):
    """
    Print the availability of the products by default or output them to an
    .xlsx file
    """
    filters = {
        "min_price": min_price,
        "max_price": max_price,
        "min_count": min_count,
        "max_count": max_count,
        "brand": brand,
    }
    ProductManager.list_availability(output, filters)


@app.command()
def info(codes: str):
    """
    Print the availability of the specified codes (separated with ,)
    along with other information
    """
    ProductManager.get_availability(codes.split(","))
