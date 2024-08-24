from datetime import datetime
from typing import Callable

import WMan.database as database
from WMan.ProductManager import ColumnIndexes
from WMan.sheetutils.reader import SheetReader


class OrderProductInfo:
    def __init__(self, product_code: str | None = None, count: int | None = None):
        self.product_code = product_code
        self.count = count


class OrderProductIndexes:
    def __init__(
        self, product_code_index: int | None = None, count_index: int | None = None
    ):
        self.product_code = product_code_index
        self.count = count_index


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

    def get_id(self):
        return self.order.id
