from typing import Optional

import babel.numbers
from rich import print
from rich.table import Table

from WMan.database import Product, ProductInfo, db
from WMan.sheetutils.reader import SheetReader
from WMan.sheetutils.writer import SheetWriter


class ProductManager:
    def __init__(self):
        db.connect()
        db.create_tables([Product])

    @staticmethod
    def add(product_info: ProductInfo):
        Product.add(product_info)

    @staticmethod
    def add_batch(
        filepath: str,
        id_column: int,
        description_column: int,
        brand_column: int,
        price_column: int,
        count_in_carton_column: int,
    ):
        reader = SheetReader(filepath)
        data = reader.get_data()
        for product in data:
            new_product = ProductInfo(
                code=product[id_column],
                description=product[description_column],
                brand=product[brand_column],
                price=product[price_column],
                count_in_carton=product[count_in_carton_column],
            )
            try:
                ProductManager.add(new_product)
            except Exception as e:
                print(f"Error adding product: {e}")
                pass

    @staticmethod
    def print_products(products):
        table = Table(title="Products")
        table.add_column("Code", justify="center", style="cyan")
        table.add_column("Description", justify="right", style="magenta")
        table.add_column("Brand", justify="center", style="green")
        table.add_column("CIC", justify="center", style="blue")
        table.add_column("Price", justify="right", style="red")

        for product in products:
            table.add_row(
                product.id,
                product.description,
                product.brand,
                str(product.count_in_carton),
                babel.numbers.format_currency(
                    product.price, "IRR", format="¤¤ #,##0", locale="en_US"
                ),
            )

        print(table)

    @staticmethod
    def save_products(filepath: str, products):
        writer = SheetWriter()

        data = [
            [
                product.id,
                product.description,
                product.brand,
                product.count_in_carton,
                product.price,
            ]
            for product in products
        ]

        headers = ["Code", "Description", "Brand", "CIC", "Price"]

        writer.add_data(data)
        writer.add_headers(headers)
        writer.add_row_index_column()
        writer.make_table("Pricelist")
        writer.set_column_currency_format(6)
        writer.set_optimal_column_widths()

        writer.save(filepath)

    @staticmethod
    def list(
        output: Optional[str] = None,
        min_price: Optional[int] = None,
        max_price: Optional[int] = None,
        brand: Optional[int] = None,
    ):
        products = Product.get_filtered(
            {"min_price": min_price, "max_price": max_price, "brand": brand}
        )

        if output:
            ProductManager.save_products(filepath=output, products=products)
        else:
            ProductManager.print_products(products)

    @staticmethod
    def remove(code: str):
        try:
            product = Product.get(Product.id == code)
            product.delete_instance()
        except Exception as e:
            print(f"Error deleting product: {e}")
            pass


if __name__ == "__main__":
    ProductManager.list()
