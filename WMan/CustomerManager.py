import rich
from rich.table import Table

from WMan.database import Customer


class CustomerManager:
    @staticmethod
    def create(name: str):
        Customer.add(name)

    @staticmethod
    def list(filters: dict[str, str | int | None]):
        table = Table(title="Customers")
        table.add_column("ID", justify="center", style="cyan")
        table.add_column("Name", justify="center", style="green")

        for customer in Customer.get_filtered(filters):
            table.add_row(str(customer.id), customer.name)

        rich.print(table)
