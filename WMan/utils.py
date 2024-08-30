from babel.numbers import format_currency

def format_to_rials(number: int | str) -> str:
    if isinstance(number, int):
        number = str(number)

    return format_currency(number, currency="IRR", format="¤¤ #,##0", locale="en_US")