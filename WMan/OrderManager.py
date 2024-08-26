import datetime
from typing import Callable
import rich
from rich.table import Table

import WMan.database as database
from WMan.ProductManager import ColumnIndexes
from WMan.sheetutils.reader import SheetReader
from WMan.sheetutils.writer import SheetWriter
from WMan.database import OrderProductInfo


class OrderProductIndexes:
    def __init__(
        self, product_code_index: int | None = None, count_index: int | None = None
    ):
        self.product_code = product_code_index
        self.count = count_index


class OrdersIO:
    def __init__(self, orders: list[database.OrderInfo]) -> None:
        self.orders = orders

        self.table = Table(title="Orders")
        self.table.add_column("ID", style="cyan")
        self.table.add_column("Customer Name", style="magenta")
        self.table.add_column("Date", style="green")
        self.table.add_column("Total Price", style="yellow")
        self.table.add_column("Total Count", style="blue")

    def print_orders(self):
        for order in self.orders:
            self.table.add_row(
                str(order.id),
                order.customer_name,
                order.date.strftime("%Y-%m-%d"),
                str(order.total_price),
                str(order.total_count),
            )
        total_price = sum([order.total_price for order in self.orders])
        total_count = sum([order.total_count for order in self.orders])

        self.table.add_section()
        self.table.add_row(
            "Total:",
            "",
            "",
            rich.text.Text(
                f"{total_price}",
                style="bold green",
            ),
            rich.text.Text(
                f"{total_count}",
                style="bold green",
            ),
        )

        rich.print(self.table)


class OrderIO:
    def __init__(self, products: list[database.ProductInfo]) -> None:
        self.products = products

        self.table = Table(title="Products")
        self.table.add_column("Code", style="cyan")
        self.table.add_column("Description", style="magenta")
        self.table.add_column("Brand", style="green")
        self.table.add_column("Count", style="blue")
        self.table.add_column("Price", style="yellow")
        self.table.add_column("Total Price", style="red")

    def print_products(self):
        for product in self.products:
            self.table.add_row(
                product.code,
                product.description,
                product.brand,
                str(product.count),
                str(product.price),
                str(product.price * product.count),
            )
        total_price = sum([product.price * product.count for product in self.products])
        total_count = sum([product.count for product in self.products])

        self.table.add_section()
        self.table.add_row(
            "Total:",
            "",
            "",
            rich.text.Text(
                f"{total_count}",
                style="bold green",
            ),
            "",
            rich.text.Text(
                f"{total_price}",
                style="bold green",
            ),
        )

        rich.print(self.table)

    def save_products(self, path: str) -> None:
        data = [
            [
                product.code,
                product.description,
                product.brand,
                product.count,
                product.price,
                product.price * product.count,
            ]
            for product in self.products
        ]

        headers = ["Code", "Description", "Brand", "Count", "Price", "Full Price"]

        writer = SheetWriter()
        writer.add_data(data)
        writer.add_headers(headers)
        writer.add_row_index_column()
        writer.add_subheader("Buyer:", "Order")
        writer.add_header("Order")
        writer.make_table("Order", start_row=3)
        writer.set_column_currency_format(7)
        writer.set_column_currency_format(6)
        writer.set_optimal_column_widths()

        writer.save(path)


class OrderManager:
    def __init__(self, order: database.Order) -> None:
        self.order = order

    @staticmethod
    def new(customer_name: str, date: datetime) -> "OrderManager":
        new_order = database.Order.new(customer_name, date)
        new_order_manager = OrderManager(new_order)
        return new_order_manager

    @staticmethod
    def from_id(order_id: int) -> "OrderManager":
        found_order = database.get_or_raise(database.Order, order_id)
        new_order_manager = OrderManager(found_order)
        return new_order_manager

    @staticmethod
    def get_order_product_from_indexes(
        order_product_list: list[str | int], indexes: OrderProductIndexes
    ):
        return OrderProductInfo(
            product_code=(
                order_product_list[indexes.product_code]
                if indexes.product_code is not None
                else None
            ),
            count=(
                order_product_list[indexes.count] if indexes.count is not None else None
            ),
        )

    def batch_apply(
        self,
        filepath: str,
        indexes: ColumnIndexes,
        method_to_apply: Callable[[OrderProductInfo], None],
        *args,
    ):
        reader = SheetReader(filepath)
        data = reader.get_data()
        for order_product in data:
            new_order_product_info = self.get_order_product_from_indexes(
                order_product, indexes
            )
            method_to_apply(new_order_product_info, *args)

    def add_product(self, order_product: OrderProductInfo):
        database.Order.add_product(
            order_id=self.order.id,
            product_code=order_product.product_code,
            count=order_product.count,
        )

    def remove_product(self, order_product: OrderProductInfo):
        database.Order.remove_product(self.get_id(), order_product.product_code)

    def add_count(self, order_product: OrderProductInfo):
        database.Order.add_count_product(
            self.get_id(), order_product.product_code, order_product.count
        )

    def reduce_count(self, order_product: OrderProductInfo):
        database.Order.reduce_count_product(
            self.get_id(), order_product.product_code, order_product.count
        )

    def get_products(self) -> list[database.ProductInfo]:
        return database.Order.get_order_product_infos(self.get_id())

    @staticmethod
    def get_orders(
        filters: dict[str, str | int | None] = {},
    ) -> list[database.OrderInfo]:
        return database.Order.get_filtered(filters)

    def get_id(self):
        return self.order.id
