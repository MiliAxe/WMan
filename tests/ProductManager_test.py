import os
import sys
from unittest.mock import patch
import unittest
# from WMan.ProductManager import ProductManager, ColumnIndexes, ProductInfo, Product
from WMan.ProductManager import ProductManager, ProductInfo, Product

# sys.path.insert(0, os.path.abspath(os.path.join(os.path.dirname(__file__), '../')))

class TestProductManager(unittest.TestCase):
    @patch.object(Product, 'get')
    def test_update(self, mock_get):
        # Mock the get method to return a product
        mock_get.return_value = Product(id='123', description='Test Product', brand='Test Brand', price=10.0, count_in_carton=5)

        # Create a sample product info for update
        updated_product = ProductInfo(code='123', description='Updated Product', brand='Updated Brand', price=15.0, count_in_carton=10)

        # Call the update method
        ProductManager.update(updated_product)

        # Assert that the product attributes have been updated
        self.assertEqual(mock_get.call_count, 1)
        self.assertEqual(mock_get.call_args[0][0], '123')
        self.assertEqual(mock_get.return_value.description, 'Updated Product')
        self.assertEqual(mock_get.return_value.brand, 'Updated Brand')
        self.assertEqual(mock_get.return_value.price, 15.0)
        self.assertEqual(mock_get.return_value.count_in_carton, 10)
        # self.assertEqual(mock_get.return_value.count, 30)


if __name__ == '__main__':
    unittest.main()