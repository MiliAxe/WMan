import rich.table
from rich import print

import database
from sheetutils.reader import SheetReader


class ProductManager:
    def __init__(self):
        database.db.connect()
        database.db.create_tables([database.Product])

    @staticmethod
    def add(product_info: database.ProductInfo):
        database.add_product_to_database(product_info)

    @staticmethod
    def add_batch(filepath: str, id_column: int, description_column: int, brand_column: int,
                  price_column: int, count_in_carton_column: int):
        reader = SheetReader(filepath)
        data = reader.get_data()
        for product in data:
            new_product = database.ProductInfo(
                code=product[id_column],
                description=product[description_column],
                brand=product[brand_column],
                price=product[price_column],
                count_in_carton=product[count_in_carton_column]
            )
            try:
                ProductManager.add(new_product)
            except Exception as e:
                print(f"Error adding product: {e}")
                pass

    @staticmethod
    def list(min_price: int = None, max_price: int = None, brand: str = None):
        products = database.Product.select()
        if min_price:
            products = products.where(database.Product.price >= min_price)
        if max_price:
            products = products.where(database.Product.price <= max_price)
        if brand:
            products = products.where(database.Product.brand == brand)

        table = rich.table.Table(title="Products")
        table.add_column("Code", justify="center", style="cyan")
        table.add_column("Description", justify="right", style="magenta")
        table.add_column("Brand", justify="center", style="green")
        table.add_column("Count in carton", justify="center", style="blue")
        table.add_column("Price", justify="right", style="red")

        for product in products:
            table.add_row(product.id, product.description,
                          product.brand, str(product.count_in_carton), str(product.price))

        print(table)

    @staticmethod
    def remove(code: str):
        try:
            product = database.Product.get(database.Product.id == code)
            product.delete_instance()
        except Exception as e:
            print(f"Error deleting product: {e}")
            pass
