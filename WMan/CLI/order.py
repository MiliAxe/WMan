import typer
from WMan.OrderManager import OrderManager, OrderProductInfo
from datetime import datetime
import jdatetime
import rich

app = typer.Typer()


@app.command()
def create(
    customer_name: str = typer.Argument(
        ..., help="The name of the customer for whom the order is being created."
    ),
    date: datetime = typer.Option(
        None, help="The date of the order in the format 'YYYY-MM-DD'."
    ),
):
    """
    Create a new order for a specified customer.
    """
    input_date = datetime.today()
    if date:
        input_date = jdatetime.datetime.strptime(
            f"{date.date()}", "%Y-%m-%d"
        ).togregorian()
    new_order_manager = OrderManager.new(customer_name, input_date)
    rich.print(f"New order with ID {new_order_manager.get_id()} was created")


@app.command()
def add(
    order_id: int = typer.Argument(
        ..., help="The ID of the order to which the product will be added."
    ),
    product_code: str = typer.Argument(
        ..., help="The code of the product to add to the order."
    ),
    count: int = typer.Argument(..., help="The quantity of the product to add."),
):
    """
    Add a product to an existing order.
    """
    order = OrderManager.from_id(order_id)
    new_order_product = OrderProductInfo(product_code, count)
    order.add_product(new_order_product)


@app.command()
def add_batch(
    order_id: int = typer.Argument(
        ..., help="The ID of the order to which the products will be added."
    ),
    filename: str = typer.Argument(
        ...,
        help="The path to the Excel (.xlsx) file containing the products and their quantities.",
    ),
    product_code_index: int = typer.Argument(
        1,
        help="The column index of the product codes in the Excel file (default is 1).",
    ),
    count_index: int = typer.Argument(
        2,
        help="The column index of the product quantities in the Excel file (default is 2).",
    ),
):
    """
    Add multiple products to an order from an Excel (.xlsx) file.
    """
    pass


@app.command()
def remove(
    order_id: int = typer.Argument(
        ..., help="The ID of the order from which the product will be removed."
    ),
    product_code: str = typer.Argument(
        ..., help="The code of the product to remove from the order."
    ),
):
    """
    Remove a product from an existing order.
    """
    order = OrderManager.from_id(order_id)
    order.remove_product(OrderProductInfo(product_code))


@app.command()
def remove_batch(
    order_id: int = typer.Argument(
        ..., help="The ID of the order from which the products will be removed."
    ),
    filename: str = typer.Argument(
        ..., help="The path to the Excel (.xlsx) file containing the product codes."
    ),
    product_code_index: int = typer.Argument(
        1,
        help="The column index of the product codes in the Excel file (default is 1).",
    ),
):
    """
    Remove multiple products from an order using an Excel (.xlsx) file.
    """
    pass


@app.command()
def add_count(
    order_id: int = typer.Argument(
        ..., help="The ID of the order where the product count will be increased."
    ),
    product_code: str = typer.Argument(
        ..., help="The code of the product to increase the count for."
    ),
    count: int = typer.Argument(
        ..., help="The amount to increase the product count by."
    ),
):
    """
    Increase the quantity of a product in an existing order.
    """
    order = OrderManager.from_id(order_id)
    order.add_count(OrderProductInfo(product_code, count))


@app.command()
def add_count_batch(
    filename: str = typer.Argument(
        ...,
        help="The path to the Excel (.xlsx) file containing the product codes and quantities to increase.",
    ),
    order_id: int = typer.Argument(
        ..., help="The ID of the order where the product counts will be increased."
    ),
    product_code_index: int = typer.Argument(
        1,
        help="The column index of the product codes in the Excel file (default is 1).",
    ),
    count_index: int = typer.Argument(
        2, help="The column index of the quantities in the Excel file (default is 2)."
    ),
):
    """
    Increase the quantities of multiple products in an order using an Excel (.xlsx) file.
    """
    pass


@app.command()
def reduce_count(
    order_id: int = typer.Argument(
        ..., help="The ID of the order where the product count will be decreased."
    ),
    product_code: str = typer.Argument(
        ..., help="The code of the product to decrease the count for."
    ),
    count: int = typer.Argument(
        ..., help="The amount to decrease the product count by."
    ),
):
    """
    Decrease the quantity of a product in an existing order.
    """
    pass


@app.command()
def reduce_count_batch(
    filename: str = typer.Argument(
        ...,
        help="The path to the Excel (.xlsx) file containing the product codes and quantities to decrease.",
    ),
    order_id: int = typer.Argument(
        ..., help="The ID of the order where the products of it will be reduced"
    ),
    product_code_index: int = typer.Argument(
        1,
        help="The column index of the product codes in the Excel file (default is 1).",
    ),
    count_index: int = typer.Argument(
        2, help="The column index of the quantities in the Excel file (default is 2)."
    ),
):
    """
    Decrease the quantities of multiple products in an order using an Excel (.xlsx) file.
    """
