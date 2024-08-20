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


class Customer(BaseModel):
    name = CharField()

    @classmethod
    def add(cls, name: str) -> "Customer":
        customer = Customer.create(name=name)
        return customer

    @classmethod
    def get_customer_id(cls, customer_name: str) -> int:
        selected_customer = Customer.get(Customer.name == customer_name)
        return selected_customer.id


class Order(BaseModel):
    date = DateField(default=datetime.datetime.now)
    customer = ForeignKeyField(Customer, backref="orders")

    @classmethod
    def create_order(cls, customer_id: int) -> "Order":
        selected_customer = get_or_raise(Customer, str(customer_id))

        order = Order.create(customer=selected_customer)
        return order

    @classmethod
    def add_product_to_order(cls, order_id: int, product_code: str, count: int) -> None:
        if Product.get_count(product_code) < count:
            raise Exception("There is not enough available product for this order")

        selected_order = Order.get(Order.id == order_id)
        selected_product = Product.get(Product.id == product_code)
        return OrderProduct.create(
            count=count, order=selected_order, product=selected_product
        )


class OrderProduct(BaseModel):
    count = IntegerField()
    product = ForeignKeyField(Product, backref="orders")
    order = ForeignKeyField(Order, backref="products")

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
    create_tables()
