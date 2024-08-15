import os
import sys
import unittest

from WMan.sheetutils.reader import SheetReader

sys.path.insert(0, os.path.abspath(os.path.join(os.path.dirname(__file__), '../../')))


class TestSheetReader(unittest.TestCase):
    def test_cars(self):
        current_path = os.path.dirname(__file__)
        asset_path = current_path + "/assets/reader_cars.xlsx"
        reader = SheetReader(asset_path)
        data = reader.get_data()

        self.assertEqual(data[0], [1, "Lamborghini", 400000])
        self.assertEqual(data[1], [2, "BMW", 200000])
        self.assertEqual(data[2], [3, "Mercedes", 300000])


if __name__ == '__main__':
    unittest.main()
