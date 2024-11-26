# warehouse_system.py is a module that contains classes for managing a warehouse inventory system.
# The module includes a DatabaseManager class for interacting with an SQLite database, a StockItem
# abstract class, a ConcreteStockItem class that implements the StockItem interface, and a Warehouse
# class that uses the DatabaseManager to manage inventory items. The Warehouse class provides methods
# for adding, removing, updating, and listing items in the inventory.

import sqlite3
from abc import ABC, abstractmethod

class DatabaseManager:
    """Class to manage database operations with SQLite."""

    def __init__(self, db_name="warehouse.db"):
        """Initialize the database manager with a database name."""
        self.db_name = db_name
        self.connection = sqlite3.connect(self.db_name)
        self.cursor = self.connection.cursor()
        self.create_table()

    def create_table(self):
        """Create the stock_items table if it doesn't exist."""
        self.cursor.execute('''CREATE TABLE IF NOT EXISTS stock_items (
                               item_id INTEGER PRIMARY KEY AUTOINCREMENT,
                               name TEXT,
                               quantity INTEGER,
                               category TEXT)''')
        self.connection.commit()

    def add_item_to_db(self, item):
        """Add an item to the database."""
        self.cursor.execute('''INSERT INTO stock_items (name, quantity, category) 
                               VALUES (?, ?, ?)''', (item.name, item.quantity, item.category))
        self.connection.commit()
        item.item_id = self.cursor.lastrowid

    def remove_item_from_db(self, item_id):
        """Remove an item from the database by its ID."""
        self.cursor.execute('DELETE FROM stock_items WHERE item_id = ?', (item_id,))
        self.connection.commit()

    def get_items_from_db(self):
        """Retrieve all items from the database."""
        self.cursor.execute('SELECT * FROM stock_items')
        rows = self.cursor.fetchall()
        return [ConcreteStockItem(row[0], row[1], row[2], row[3]) for row in rows]

    def update_item_in_db(self, item):
        """Update an existing item in the database."""
        self.cursor.execute('''
            UPDATE stock_items
            SET name = ?, quantity = ?, category = ?
            WHERE item_id = ?
        ''', (item.name, item.quantity, item.category, item.item_id))
        self.connection.commit()

    def close(self):
        """Close the database connection."""
        self.connection.close()

class StockItem(ABC):
    """Abstract base class representing a stock item."""

    def __init__(self, item_id, name, quantity, category):
        """Initialize a stock item with ID, name, quantity, and category."""
        self.item_id = item_id
        self.name = name
        self.quantity = quantity
        self.category = category

    @abstractmethod
    def update_quantity(self, amount):
        """Abstract method to update the quantity of the stock item."""
        pass

    def __str__(self):
        """Return a string representation of the stock item."""
        return f"Item ID: {self.item_id}, Name: {self.name}, Quantity: {self.quantity}, Category: {self.category}"

class ConcreteStockItem(StockItem):
    """Concrete implementation of a stock item."""

    def update_quantity(self, amount):
        """Update the quantity of the stock item, ensuring it does not become negative."""
        if amount < 0 and self.quantity + amount < 0:
            raise ValueError("Quantity cannot be negative.")
        self.quantity += amount

class Warehouse:
    """Class to manage inventory operations."""

    def __init__(self, db_manager):
        """Initialize the warehouse with a database manager."""
        self.db_manager = db_manager

    def add_item(self, item):
        """Add an item to the inventory."""
        self.db_manager.add_item_to_db(item)

    def remove_item(self, item_id):
        """Remove an item from the inventory by its ID."""
        self.db_manager.remove_item_from_db(item_id)

    def list_items(self):
        """List all items in the inventory."""
        return self.db_manager.get_items_from_db()

    def get_item(self, item_id):
        """Get a specific item from the inventory by its ID."""
        items = self.db_manager.get_items_from_db()
        for item in items:
            if item.item_id == item_id:
                return item
        return None

    def update_item(self, updated_item):
        """Update an existing item in the inventory."""
        self.db_manager.update_item_in_db(updated_item)
