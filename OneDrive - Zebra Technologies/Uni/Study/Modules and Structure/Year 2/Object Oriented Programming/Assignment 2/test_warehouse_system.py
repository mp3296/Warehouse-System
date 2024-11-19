import unittest
from warehouse_system import DatabaseManager, Warehouse, ConcreteStockItem

class TestWarehouseSystem(unittest.TestCase):
    @classmethod
    def setUpClass(cls):
        """Set up a test database for all tests."""
        print("Setting up test database...")
        cls.db_manager = DatabaseManager(db_name="test_warehouse.db")
        cls.warehouse = Warehouse(cls.db_manager)

    @classmethod
    def tearDownClass(cls):
        """Clean up the test database after all tests."""
        print("Tearing down test database...")
        cls.db_manager.cursor.execute("DROP TABLE IF EXISTS stock_items")
        cls.db_manager.connection.close()

    def setUp(self):
        """Clear the warehouse and database before each test."""
        print("Clearing database and resetting warehouse state...")
        self.db_manager.cursor.execute("DELETE FROM stock_items")
        self.db_manager.connection.commit()
        self.warehouse.stock_items = []

    def test_add_item(self):
        print("Running test_add_item...")
        item = ConcreteStockItem(None, "Box", 15, "Packaging")
        self.warehouse.add_item(item)
        print(f"Items in warehouse after add: {self.warehouse.list_items()}")
        self.assertEqual(len(self.warehouse.stock_items), 1)
        self.assertEqual(self.warehouse.stock_items[0].name, "Box")

    def test_remove_item(self):
        print("Running test_remove_item...")
        item = ConcreteStockItem(None, "Core", 20, "Materials")
        self.warehouse.add_item(item)
        print(f"Items in warehouse before remove: {self.warehouse.list_items()}")
        self.warehouse.remove_item(item.item_id)
        print(f"Items in warehouse after remove: {self.warehouse.list_items()}")
        self.assertEqual(len(self.warehouse.stock_items), 0)

    def test_list_items(self):
        print("Running test_list_items...")
        item1 = ConcreteStockItem(None, "Material", 30, "Raw")
        item2 = ConcreteStockItem(None, "Toolbox", 5, "Tools")
        self.warehouse.add_item(item1)
        self.warehouse.add_item(item2)
        items = self.warehouse.list_items()
        print(f"Listed items: {items}")
        self.assertEqual(len(items), 2)

    def test_update_quantity(self):
        print("Running test_update_quantity...")
        item = ConcreteStockItem(None, "Pallet", 10, "Logistics")
        self.warehouse.add_item(item)
        print(f"Initial item quantity: {item.quantity}")
        item.update_quantity(15)
        print(f"Item quantity after update: {item.quantity}")
        self.assertEqual(item.quantity, 25)
        print("Testing invalid quantity update...")
        with self.assertRaises(ValueError):
            item.update_quantity(-50)

    def test_database_integration(self):
        print("Running test_database_integration...")
        item = ConcreteStockItem(None, "Crate", 40, "Storage")
        self.warehouse.add_item(item)
        print(f"Items in database after add: {self.warehouse.list_items()}")

        print("Creating new Warehouse instance for integration test...")
        new_warehouse = Warehouse(self.db_manager)
        print(f"Items in new warehouse instance: {new_warehouse.list_items()}")
        self.assertEqual(len(new_warehouse.stock_items), 1)
        self.assertEqual(new_warehouse.stock_items[0].name, "Crate")


if __name__ == "__main__":
    unittest.main()
