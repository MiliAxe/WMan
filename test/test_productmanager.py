from unittest.mock import patch, Mock, MagicMock
import unittest.mock
import tempfile

from WMan.database import Product, ProductInfo
from WMan.ProductManager import ProductManager, ColumnIndexes
from WMan.sheetutils.reader import SheetReader


class TestProductManager(unittest.TestCase):
    def setUp(self):
        self.sample_product_infos = [
            ProductInfo(
                code="P001",
                description="Product 1",
                brand="BrandA",
                price=1000,
                count_in_carton=10
            ),
            ProductInfo(
                code="P002",
                description="Product 2",
                brand="BrandB",
                price=1234567890,
                count_in_carton=20
            ),
            ProductInfo(
                code="P003",
                description="Product 3",
                brand="BrandC",
                price=10000,
                count_in_carton=100
            )
        ]
        
        self.sample_product_list = [
            ["P001", "Product 1", "BrandA",  10, 1000],
            ["P002", "Product 2", "BrandB",  20, 1234567890],
            ["P003", "Product 3", "BrandC",  100, 10000]
        ]    
    

    @patch.object(Product, "get")
    def test_product_update(self, mock_get):
        mock_get.return_value = Product(
            id="123",
            description="Test Product",
            brand="Test Brand",
            price=10.0,
            count_in_carton=5,
        )

        updated_product = ProductInfo(
            code="123",
            description="Updated Product",
            brand="Updated Brand",
            price=15.0,
            count_in_carton=10,
        )

        ProductManager.update(updated_product)

        self.assertEqual(mock_get.call_count, 1)
        self.assertEqual(mock_get.call_args[0][0], "123")
        self.assertEqual(mock_get.return_value.description, "Updated Product")
        self.assertEqual(mock_get.return_value.brand, "Updated Brand")
        self.assertEqual(mock_get.return_value.price, 15.0)
        self.assertEqual(mock_get.return_value.count_in_carton, 10)

    @patch.object(Product, "add")
    def test_product_add(self, mock_add: Mock):
        new_product = ProductInfo(
            code="testProduct",
            description="This is a test product",
            brand="testBrand",
            count_in_carton=69,
            price=69420,
        )

        ProductManager.add(new_product)

        self.assertEqual(mock_add.call_args.args[0].code, "testProduct")
        self.assertEqual(
            mock_add.call_args.args[0].description, "This is a test product"
        )
        self.assertEqual(mock_add.call_args.args[0].brand, "testBrand")
        self.assertEqual(mock_add.call_args.args[0].count_in_carton, 69)
        self.assertEqual(mock_add.call_args.args[0].price, 69420)

    def test_product_from_indexes(self):
        product_list = [
            "This is a cool product",
            "CoolProduct",
            69420,
            420,
            "CoolestBrand",
        ]

        indexes = ColumnIndexes(
            code_column=1,
            description_column=0,
            brand_column=4,
            price_column=2,
            count_in_carton_column=3,
        )

        new_product_info = ProductManager.get_product_from_indexes(
            product_list, indexes
        )

        self.assertEqual(new_product_info.code, "CoolProduct")
        self.assertEqual(new_product_info.description, "This is a cool product")
        self.assertEqual(new_product_info.brand, "CoolestBrand")
        self.assertEqual(new_product_info.price, 69420)
        self.assertEqual(new_product_info.count_in_carton, 420)

    @patch.object(SheetReader, "__init__")
    @patch.object(SheetReader, "get_data")
    def test_batch_apply(self, mock_get_data: Mock, mock_init: Mock):
        mock_init.return_value = None
        mock_get_data.return_value = self.sample_product_list

        indexes = ColumnIndexes(
            code_column=0,
            description_column=1,
            brand_column=2,
            price_column=4,
            count_in_carton_column=3,
        )

        mock_method = MagicMock()

        ProductManager.batch_apply("dummy.xlsx", indexes, mock_method)

        mock_method.assert_called()
        mock_method.assert_any_call(self.sample_product_infos[0])
        mock_method.assert_any_call(self.sample_product_infos[1])
    

    @patch('rich.print')
    @patch('rich.table.Table.add_row')
    def test_print_products(self, mock_add_row: Mock, mock_print: Mock):
        ProductManager.print_products(self.sample_product_infos)
        
        mock_print.assert_called_once()
        mock_add_row.assert_any_call(self.sample_product_infos[0].code, self.sample_product_infos[0].description, self.sample_product_infos[0].brand, "10", "IRR 1,000")
        mock_add_row.assert_any_call(self.sample_product_infos[1].code, self.sample_product_infos[1].description, self.sample_product_infos[1].brand, "20", "IRR 1,234,567,890")
        
    
    def test_save_products(self):
        with tempfile.NamedTemporaryFile() as tmpfile:
            filename = tmpfile.name + ".xlsx"
            ProductManager.save_products(filename, self.sample_product_infos)
            
            reader = SheetReader(filename)
            data = reader.get_data()
            
            self.assertEqual(data[0], ["1"] + self.sample_product_list[0])
            self.assertEqual(data[1], ["2"] + self.sample_product_list[1])
            self.assertEqual(data[2], ["3"] + self.sample_product_list[2])
        
        
    


if __name__ == "__main__":
    unittest.main()
