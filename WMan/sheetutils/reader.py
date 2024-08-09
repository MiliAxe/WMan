from typing import List

from openpyxl import load_workbook


class SheetReader:
    def __init__(self, filepath: str):
        self.workbook = load_workbook(filepath)
        self.sheet = self.workbook.active
        self.headers: List = []

    def get_data(self) -> List[List]:
        read_data = [list(row) for row in self.sheet.iter_rows(values_only=True)]
        self.headers = read_data[0]
        return read_data[1:]
