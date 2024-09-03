from babel.numbers import format_currency
import datetime
import jdatetime


def format_to_rials(number: int | str) -> str:
    if isinstance(number, int):
        number = str(number)

    return format_currency(number, currency="IRR", format="¤¤ #,##0", locale="en_US")


def get_local_date(date: datetime) -> str:
    jalali_date = jdatetime.datetime.fromgregorian(datetime=date)
    return jalali_date.strftime("%Y-%m-%d")


if __name__ == "__main__":
    print(get_local_date(datetime.datetime(2024, 1, 1)))
