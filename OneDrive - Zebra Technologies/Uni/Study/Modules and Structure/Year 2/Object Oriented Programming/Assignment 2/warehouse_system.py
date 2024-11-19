# warehouse_system.py
import sqlite3
from abc import ABC, abstractmethod

# Database Manager
class DatabaseManager:
    def __init__(self, db_name="warehouse.db"):
        self.db_name = db_name
        self.connection = sqlite3.connect(self.db_name)
        self.cursor = self.connection.cursor()
        self.create_table()

    def create_table(self):
        self.cursor.execute('''CREATE TABLE IF NOT EXISTS stock_items (
                               item_id INTEGER PRIMARY KEY AUTOINCREMENT,
                               name TEXT,
                               quantity INTEGER,
                               category TEXT)''')
        self.connection.commit()

    def add_item_to_db(self, item):
        self.cursor.execute('''INSERT INTO stock_items (name, quantity, category) 
                               VALUES (?, ?, ?)''', (item.name, item.quantity, item.category))
        self.connection.commit()
        item.item_id = self.cursor.lastrowid  # Update the item ID after insertion

    def remove_item_from_db(self, item_id):
        self.cursor.execute('DELETE FROM stock_items WHERE item_id = ?', (item_id,))
        self.connection.commit()

    def get_items_from_db(self):
        self.cursor.execute('SELECT * FROM stock_items')
        rows = self.cursor.fetchall()
        return [ConcreteStockItem(row[0], row[1], row[2], row[3]) for row in rows]

    def close(self):
        self.connection.close()

# Abstract StockItem Class (for abstraction)
class StockItem(ABC):
    def __init__(self, item_id, name, quantity, category):
        self.item_id = item_id
        self.name = name
        self.quantity = quantity
        self.category = category

    @abstractmethod
    def update_quantity(self, amount):
        pass

    def __str__(self):
        return f"Item ID: {self.item_id}, Name: {self.name}, Quantity: {self.quantity}, Category: {self.category}"

# Concrete StockItem Class
class ConcreteStockItem(StockItem):
    def update_quantity(self, amount):
        if amount < 0 and self.quantity + amount < 0:
            raise ValueError("Quantity cannot be negative.")
        self.quantity += amount

# Warehouse Class (for encapsulation)
class Warehouse:
    def __init__(self, db_manager):
        self.db_manager = db_manager
        self.stock_items = self.db_manager.get_items_from_db()

    def add_item(self, item):
        self.db_manager.add_item_to_db(item)  # Save to database first
        self.stock_items.append(item)

    def remove_item(self, item_id):
        self.db_manager.remove_item_from_db(item_id)
        self.stock_items = [item for item in self.stock_items if item.item_id != item_id]

    def list_items(self):
        return [str(item) for item in self.stock_items]
