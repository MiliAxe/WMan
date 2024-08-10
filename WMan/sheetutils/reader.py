from openpyxl import load_workbook


class SheetReader:
    def __init__(self, filepath: str):
        self.workbook = load_workbook(filepath)
        self.headers = []
        if self.workbook.active:
            self.sheet = self.workbook.active

    def get_data(self):
        read_data = [list(row) for row in self.sheet.iter_rows(values_only=True)]
        self.headers = read_data[0]
        return read_data[1:]
