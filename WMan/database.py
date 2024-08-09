import datetime
from typing import Type

from peewee import SqliteDatabase, Model, CharField, IntegerField, ForeignKeyField, DateField, CompositeKey, \
    DoesNotExist

db = SqliteDatabase("warehouse.db")


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


class Customer(BaseModel):
    name = CharField()


class Order(BaseModel):
    date = DateField(default=datetime.datetime.now)
    customer = ForeignKeyField(Customer, backref='orders')


class OrderProduct(BaseModel):
    count = IntegerField()
    product = ForeignKeyField(Product, backref='orders')
    order = ForeignKeyField(Order, backref='products')

    class Meta:
        primary_key = CompositeKey('product', 'order')


class ProductInfo:
    def __init__(self, code: str, description: str, brand: str, count_in_carton: int, price: int) -> None:
        self.code = code
        self.description = description
        self.brand = brand
        self.count_in_carton = count_in_carton
        self.price = price


class NotFoundException(Exception):
    def __init__(self, model_object: Type[Model], model_id: str):
        super().__init__(f"{model_object.__name__} with id {model_id} was not found")


def get_or_raise(model_object: Type[Model], model_identifier: str):
    try:
        selected_object = model_object.get(model_object.id == model_identifier)
    except DoesNotExist:
        raise NotFoundException(model_object, model_identifier)
    return selected_object


def add_product_to_database(product_info: ProductInfo) -> Product:
    new_product = Product.create(
        id=product_info.code,
        description=product_info.description,
        brand=product_info.brand,
        count_in_carton=product_info.count_in_carton,
        count=0,
        price=product_info.price
    )
    return new_product


def add_product_count(product_code: str, count: int) -> None:
    selected_product = get_or_raise(Product, product_code)

    selected_product.count += count
    selected_product.save()


def get_product_count(product_code: str) -> int:
    selected_product = get_or_raise(Product, product_code)

    return selected_product.count


def add_customer_to_database(name: str) -> Customer:
    customer = Customer.create(name=name)
    return customer


def get_customer_id(customer_name: str) -> int:
    selected_customer = Customer.get(Customer.name == customer_name)
    return selected_customer.id


def create_order(customer_id: int) -> Order:
    selected_customer = get_or_raise(Customer, str(customer_id))

    order = Order.create(customer=selected_customer)
    return order


def add_product_to_order(order_id: int, product_code: str, count: int):
    if get_product_count(product_code) < count:
        raise Exception("There is not enough available product for this order")

    selected_order = Order.get(Order.id == order_id)
    selected_product = Product.get(Product.id == product_code)
    return OrderProduct.create(
        count=count,
        order=selected_order,
        product=selected_product
    )


if __name__ == "__main__":
    db.create_tables([Product, Customer, Order, OrderProduct])