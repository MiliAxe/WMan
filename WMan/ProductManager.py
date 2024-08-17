from typing import Callable

import babel.numbers
import rich
from rich.table import Table

from WMan.database import Product, ProductInfo, db, get_or_raise
from WMan.sheetutils.reader import SheetReader
from WMan.sheetutils.writer import SheetWriter


class ColumnIndexes:
    def __init__(
        self,
        code_column: int | None = None,
        description_column: int | None = None,
        brand_column: int | None = None,
        price_column: int | None = None,
        count_in_carton_column: int | None = None,
        count_column: int | None = None,
    ):
        self.code = code_column
        self.description = description_column
        self.brand = brand_column
        self.price = price_column
        self.count_in_carton = count_in_carton_column
        self.count = count_column


class ProductManager:
    def __init__(self):
        db.connect()
        db.create_tables([Product])

    @staticmethod
    def get_product_from_indexes(product: list, indexes: ColumnIndexes):
        return ProductInfo(
            code=product[indexes.code] if indexes.code is not None else None,
            description=(
                product[indexes.description]
                if indexes.description is not None
                else None
            ),
            brand=product[indexes.brand] if indexes.brand is not None else None,
            price=product[indexes.price] if indexes.price is not None else None,
            count_in_carton=(
                product[indexes.count_in_carton]
                if indexes.count_in_carton is not None
                else None
            ),
            count=product[indexes.count] if indexes.count is not None else None,
        )

    @staticmethod
    def batch_apply(
        filepath: str,
        indexes: ColumnIndexes,
        method_to_apply: Callable[[ProductInfo], None],
        *args,
    ):
        reader = SheetReader(filepath)
        data = reader.get_data()
        for product in data:
            new_product = ProductManager.get_product_from_indexes(product, indexes)
            method_to_apply(new_product, *args)

    @staticmethod
    def add(product_info: ProductInfo):
        Product.add(product_info)

    @staticmethod
    def add_batch(filepath: str, indexes: ColumnIndexes):
        ProductManager.batch_apply(filepath, indexes, ProductManager.add)

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
                product.code,
                product.description,
                product.brand,
                str(product.count_in_carton),
                babel.numbers.format_currency(
                    product.price, "IRR", format="¤¤ #,##0", locale="en_US"
                ),
            )

        rich.print(table)

    @staticmethod
    def save_products(filepath: str, products):
        writer = SheetWriter()

        data = [
            [
                product.code,
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
    def list_products(
        output: str | None = None, filters: dict[str, str | int | None] = {}
    ):
        products = Product.get_filtered(filters=filters)

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

    @staticmethod
    def update(edited_product: ProductInfo):
        selected_product: Product = get_or_raise(Product, edited_product.code)
        if edited_product.description:
            selected_product.description = edited_product.description
        if edited_product.brand:
            selected_product.brand = edited_product.brand
        if edited_product.price:
            selected_product.price = edited_product.price
        if edited_product.count_in_carton:
            selected_product.count_in_carton = edited_product.count_in_carton
        selected_product.save()

    @staticmethod
    def update_batch(filepath: str, indexes: ColumnIndexes):
        ProductManager.batch_apply(filepath, indexes, ProductManager.update)

    @staticmethod
    def add_count(product: ProductInfo):
        Product.add_count(product.code, product.count)

    @staticmethod
    def add_count_batch(filepath: str, column_index: ColumnIndexes):
        ProductManager.batch_apply(filepath, column_index, ProductManager.add_count)

    @staticmethod
    def reduce_count(product: ProductInfo):
        Product.reduce_count(product.code, product.count)

    @staticmethod
    def reduce_count_batch(filepath: str, column_index: ColumnIndexes):
        ProductManager.batch_apply(filepath, column_index, ProductManager.reduce_count)

    @staticmethod
    def print_availability(products):
        table = Table(title="Availability")
        table.add_column("Code", justify="center", style="cyan")
        table.add_column("Description", justify="right", style="magenta")
        table.add_column("Brand", justify="center", style="green")
        table.add_column("CIC", justify="center", style="blue")
        table.add_column("Price", justify="right", style="red")
        table.add_column("Total Price", justify="center", style="cyan")
        table.add_column("Count", justify="right", style="yellow")

        total_count = 0
        total_price = 0

        for product in products:
            total_count += product.count
            total_price += product.price * product.count
            table.add_row(
                product.code,
                product.description,
                product.brand,
                str(product.count_in_carton),
                babel.numbers.format_currency(
                    product.price, "IRR", format="¤¤ #,##0", locale="en_US"
                ),
                babel.numbers.format_currency(
                    product.price * product.count,
                    "IRR",
                    format="¤¤ #,##0",
                    locale="en_US",
                ),
                str(product.count),
            )

        table.add_section()
        table.add_row(
            "Total",
            "",
            "",
            "",
            "",
            babel.numbers.format_currency(
                total_price, "IRR", format="¤¤ #,##0", locale="en_US"
            ),
            str(total_count),
        )

        rich.print(table)

    @staticmethod
    def save_availability(filepath: str, products):
        writer = SheetWriter()

        data = [
            [
                product.code,
                product.description,
                product.brand,
                product.count_in_carton,
                product.price,
                product.price * product.count,
                product.count,
            ]
            for product in products
        ]

        headers = [
            "Code",
            "Description",
            "Brand",
            "CIC",
            "Price",
            "Total Price",
            "Count",
        ]

        writer.add_data(data)
        writer.add_headers(headers)
        writer.add_row_index_column()
        writer.make_table("Availability")
        writer.set_column_currency_format(7)
        writer.set_column_currency_format(6)
        writer.set_optimal_column_widths()

        writer.save(filepath)

    @staticmethod
    def list_availability(
        output: str | None = None, filters: dict[str, str | int | None] = {}
    ):
        selected_products = Product.get_filtered(filters)

        if output:
            ProductManager.save_availability(
                filepath=output, products=selected_products
            )
        else:
            ProductManager.print_availability(selected_products)

    @staticmethod
    def get_availability(codes: list[str]):
        products = []
        for code in codes:
            selected_product = get_or_raise(Product, code)
            products.append(selected_product)
        ProductManager.print_availability(products)


if __name__ == "__main__":
    ProductManager.list_products()
