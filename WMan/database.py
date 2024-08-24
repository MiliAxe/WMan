import datetime
from typing import Dict, Optional, Type

from peewee import (
    CharField,
    CompositeKey,
    DateField,
    DoesNotExist,
    ForeignKeyField,
    IntegerField,
    Model,
    SqliteDatabase,
    fn
)

db = SqliteDatabase("warehouse.db")


class ProductInfo:
    def __init__(
        self,
        code: str | None,
        description: str | None = None,
        brand: str | None = None,
        count_in_carton: int | None = None,
        price: int | None = None,
        count: int | None = None,
    ) -> None:
        self.code = code
        self.description = description
        self.brand = brand
        self.count_in_carton = count_in_carton
        self.price = price
        self.count = count

    def __eq__(self, value: object) -> bool:
        if not isinstance(value, ProductInfo):
            return False
        return (
            self.code == value.code
            and self.description == value.description
            and self.brand == value.brand
            and self.count_in_carton == value.count_in_carton
            and self.price == value.price
            and self.count == value.count
        )


class OrderProductInfo:
    def __init__(self, product_code: str | None = None, count: int | None = None):
        self.product_code = product_code
        self.count = count


class OrderInfo:
    def __init__(
        self,
        order_id: int = None,
        total_count: int = None,
        total_price: int = None,
        customer_name: str = None,
        date: datetime = None,
    ):
        self.id = order_id
        self.total_count = total_count
        self.total_price = total_price
        self.customer_name = customer_name
        self.date = date


class BaseModel(Model):
    class Meta:
        database = db


class Product(BaseModel):
    id = CharField(primary_key=True)
    description = CharField(null=True)
    brand = CharField(null=True)
    price = IntegerField(null=True)
    count_in_carton = IntegerField(null=True)
    count = IntegerField(default=0)

    @classmethod
    def add_count(cls, product_code: str, count: int) -> None:
        selected_product = get_or_raise(cls, product_code)
        selected_product.count += count
        selected_product.save()

    @classmethod
    def reduce_count(cls, product_code: str, count: int) -> None:
        selected_product = get_or_raise(cls, product_code)
        if selected_product.count < count:
            raise Exception("There is not enough available product")
        selected_product.count -= count
        selected_product.save()

    @classmethod
    def add(cls, product_info: ProductInfo):
        new_product = Product.create(
            id=product_info.code,
            description=product_info.description,
            brand=product_info.brand,
            count_in_carton=product_info.count_in_carton,
            count=0,
            price=product_info.price,
        )
        return new_product

    @classmethod
    def remove(cls, product_code: str):
        product = get_or_raise(Product, product_code)
        product.delete_instance()

    @classmethod
    def get_count(cls, product_code: str):
        selected_product = get_or_raise(Product, product_code)
        return selected_product.count

    @classmethod
    def get_filtered(cls, filters: Optional[Dict[str, str | int | None]]):
        query = cls.select()

        if filters:
            for field, value in filters.items():
                if field == "min_price" and value:
                    query = query.where(cls.price >= value)
                if field == "max_price" and value:
                    query = query.where(cls.price <= value)
                if field == "brand" and value:
                    query = query.where(cls.brand == value)
                if field == "min_count" and value:
                    query = query.where(cls.count >= value)
                if field == "max_count" and value:
                    query = query.where(cls.count <= value)

        return [
            ProductInfo(
                code=product.id,
                description=product.description,
                brand=product.brand,
                count_in_carton=product.count_in_carton,
                price=product.price,
                count=product.count,
            )
            for product in query
        ]

    @classmethod
    def get_product_info(cls, product_code: str) -> ProductInfo:
        selected_product = get_or_raise(cls, product_code)
        return ProductInfo(
            code=selected_product.id,
            description=selected_product.description,
            brand=selected_product.brand,
            count_in_carton=selected_product.count_in_carton,
            price=selected_product.price,
            count=selected_product.count,
        )


class Customer(BaseModel):
    name = CharField()

    @classmethod
    def add(cls, name: str) -> "Customer":
        if cls.does_customer_exist(name):
            raise Exception("A customer with this name already exists")
        customer = Customer.create(name=name)
        return customer

    @classmethod
    def does_customer_exist(cls, name: str) -> bool:
        found_customer = cls.select().where(cls.name == name)
        if found_customer:
            return True
        return False

    @classmethod
    def get_customer_id(cls, customer_name: str) -> int:
        selected_customer = Customer.get(Customer.name == customer_name)
        return selected_customer.id

    @classmethod
    def get_filtered(cls, filters: dict[str, str | int | None]):
        return cls.select()


class Order(BaseModel):
    date = DateField(default=datetime.datetime.now)
    customer = ForeignKeyField(Customer, backref="orders")

    @classmethod
    def new(cls, customer_name: str, date: datetime) -> "Order":
        if not Customer.does_customer_exist(customer_name):
            raise Exception(f"Customer with name '{customer_name}' does not exist")
        found_customer = Customer.get(Customer.name == customer_name)
        new_order = Order.create(customer=found_customer, date=date)
        return new_order

    @classmethod
    def add_product(cls, order_id: int, product_code: str, count: int) -> None:
        if Product.get_count(product_code) < count:
            raise Exception("There is not enough available product for this order")

        selected_order = get_or_raise(Order, order_id)
        selected_product = get_or_raise(Product, product_code)
        Product.reduce_count(product_code, count)
        return OrderProduct.create(
            count=count, order=selected_order, product=selected_product
        )

    @classmethod
    def remove_product(cls, order_id: int, product_code: str) -> None:
        order_product = OrderProduct.find_by_ids(order_id, product_code)
        order_product.delete_instance()
        Product.add_count(product_code, order_product.count)

    @staticmethod
    def add_count_product(order_id: int, product_code: str, count: int):
        order_product = OrderProduct.find_by_ids(order_id, product_code)
        if Product.get_count(product_code) < count:
            raise Exception("There is not enough product to add to order")
        Product.reduce_count(product_code, count)
        order_product.count += count
        order_product.save()

    @staticmethod
    def reduce_count_product(order_id, product_code: str, count: int):
        order_product = OrderProduct.find_by_ids(order_id, product_code)
        if order_product.count < count:
            raise Exception("The order does not have this amount of product to reduce")

        if order_product.count == count:
            order_product.delete_instance()
        else:
            order_product.count -= count
        Product.add_count(product_code, count)
        order_product.save()

    @classmethod
    def get_filtered(cls, filters: Dict[str, str | int | None] = None):
        query = cls.select()
        subquery = (OrderProduct
                        .select(fn.SUM(OrderProduct.product.price * Product.price))
                        .join(Product)
                        .where(OrderProduct.order == cls.id))

        if filters:
            for field, value in filters.items():
                if field == "customer" and value is not None:
                    query = query.where(cls.customer.name == value)
                if field == "min_price" and value is not None:
                    subquery = (OrderProduct
                                    .select(fn.SUM(OrderProduct.product.price * Product.price))
                                    .join(Product)
                                    .where(OrderProduct.order == cls.id))
                    query = query.where(subquery >= value)
                if field == "max_price" and value is not None:
                    subquery = (OrderProduct
                                    .select(fn.SUM(OrderProduct.product.price * Product.price))
                                    .join(Product)
                                    .where(OrderProduct.order == cls.id))
                    query = query.where(subquery <= value)
                if field == "start_date" and value is not None:
                    query = query.where(cls.date >= value)
                if field == "end_date" and value is not None:
                    query = query.where(cls.date <= value)

        return [
            OrderInfo(
                order.id,
                cls.get_order_total_count(order.id),
                cls.get_order_total_price(order.id),
                order.customer.name,
                order.date,
            )
            for order in query
        ]

    @classmethod
    def get_order_products(cls, order_id: int) -> list[OrderProductInfo]:
        selected_order = get_or_raise(cls, order_id)
        return [
            OrderProductInfo(
                product_code=order_product.product.id, count=order_product.count
            )
            for order_product in selected_order.products
        ]

    @classmethod
    def get_order_product_infos(cls, order_id: int) -> list[ProductInfo]:
        selected_order = get_or_raise(cls, order_id)
        return [
            ProductInfo(
                code=order_product.product.id,
                description=order_product.product.description,
                brand=order_product.product.brand,
                count_in_carton=order_product.product.count_in_carton,
                price=order_product.product.price,
                count=order_product.count,
            )
            for order_product in selected_order.products
        ]

    @classmethod
    def get_order_total_count(cls, order_id: int) -> int:
        selected_order = get_or_raise(cls, order_id)
        return sum(order_product.count for order_product in selected_order.products)

    @classmethod
    def get_order_total_price(cls, order_id: int) -> int:
        selected_order = get_or_raise(cls, order_id)
        return sum(
            (
                order_product.count
                * Product.get_product_info(order_product.product).price
            )
            for order_product in selected_order.products
        )


class OrderProduct(BaseModel):
    count = IntegerField()
    product = ForeignKeyField(Product, backref="orders")
    order = ForeignKeyField(Order, backref="products")

    @classmethod
    def find_by_ids(cls, order_id: int, product_code: str) -> "OrderProduct":
        found_order = get_or_raise(Order, order_id)
        found_product = get_or_raise(Product, product_code)

        order_product = OrderProduct.get(
            OrderProduct.order == found_order, OrderProduct.product == found_product
        )
        return order_product

    class Meta:
        primary_key = CompositeKey("product", "order")


class NotFoundException(Exception):
    def __init__(self, model_object: Type[Model], model_id: str):
        super().__init__(f"{model_object.__name__} with id {model_id} was not found")


def get_or_raise(model_object: Type[Model], model_identifier: str):
    try:
        selected_object = model_object.get(model_object.id == model_identifier)
    except DoesNotExist:
        raise NotFoundException(model_object, model_identifier)
    return selected_object


def create_tables():
    db.create_tables([Product, Customer, Order, OrderProduct])


if __name__ == "__main__":
    # print(Order.get_order_total_count(1))
    orders = Order.get_filtered({
        "min_price": 0,
    })
    for order in orders:
        print(order.id, order.total_count, order.total_price, order.customer_name, order.date)
