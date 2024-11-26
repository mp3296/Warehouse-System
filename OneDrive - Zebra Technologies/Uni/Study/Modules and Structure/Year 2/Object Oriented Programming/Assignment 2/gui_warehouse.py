# gui_warehouse.py is a GUI application that allows users to manage a warehouse inventory system.
# The application uses the tkinter library to create the GUI components and interacts with the
# warehouse_system module to manage the inventory data. The application allows users to add,
# update, and remove items from the inventory, as well as view the list of items in the warehouse.

import tkinter as tk
from tkinter import messagebox, ttk
from warehouse_system import DatabaseManager, Warehouse, ConcreteStockItem

class WarehouseGUI:
    """Class representing the GUI for the warehouse inventory system."""

    def __init__(self, root, warehouse):
        """Initialize the GUI with the root window and warehouse instance."""
        self.root = root
        self.warehouse = warehouse

        self.root.title("Inventory Management System")
        self.root.geometry("600x400")

        # Create the GUI components
        self.create_widgets()

    def create_widgets(self):
        """Create and layout GUI components."""
        # Title
        title_label = tk.Label(self.root, text="Inventory Management System", font=("Helvetica", 16))
        title_label.pack(pady=10)

        # Item List
        self.tree = ttk.Treeview(self.root, columns=("ID", "Name", "Quantity", "Category"), show="headings")
        self.tree.heading("ID", text="ID")
        self.tree.heading("Name", text="Name")
        self.tree.heading("Quantity", text="Quantity")
        self.tree.heading("Category", text="Category")
        self.tree.column("ID", width=50)
        self.tree.column("Name", width=150)
        self.tree.column("Quantity", width=100)
        self.tree.column("Category", width=150)
        self.tree.pack(pady=10, fill=tk.BOTH, expand=True)

        # Buttons
        button_frame = tk.Frame(self.root)
        button_frame.pack(pady=10)

        add_button = tk.Button(button_frame, text="Add Item", command=self.add_item_popup)
        add_button.grid(row=0, column=0, padx=10)

        remove_button = tk.Button(button_frame, text="Remove Item", command=self.remove_item)
        remove_button.grid(row=0, column=1, padx=10)

        update_button = tk.Button(button_frame, text="Update Item", command=self.update_item_popup)
        update_button.grid(row=0, column=2, padx=10)

        refresh_button = tk.Button(button_frame, text="Refresh List", command=self.load_items)
        refresh_button.grid(row=0, column=3, padx=10)

        exit_button = tk.Button(button_frame, text="Exit", command=self.root.quit)
        exit_button.grid(row=0, column=4, padx=10)

        # Load items into the treeview
        self.load_items()

    def load_items(self):
        """Load items from the warehouse into the Treeview."""
        for row in self.tree.get_children():
            self.tree.delete(row)

        for item in self.warehouse.list_items():
            self.tree.insert("", tk.END, values=(item.item_id, item.name, item.quantity, item.category))

    def add_item_popup(self):
        """Open a popup window to add a new item."""
        popup = tk.Toplevel(self.root)
        popup.title("Add Item")
        popup.geometry("300x250")

        tk.Label(popup, text="Name:").pack(pady=5)
        name_entry = tk.Entry(popup)
        name_entry.pack(pady=5)

        tk.Label(popup, text="Quantity:").pack(pady=5)
        quantity_entry = tk.Entry(popup)
        quantity_entry.pack(pady=5)

        tk.Label(popup, text="Category:").pack(pady=5)
        category_entry = tk.Entry(popup)
        category_entry.pack(pady=5)

        def add_item_action():
            try:
                name = name_entry.get().strip()
                quantity_str = quantity_entry.get().strip()
                quantity = int(quantity_str)
                if quantity < 0:
                    raise ValueError("Quantity cannot be negative.")
                category = category_entry.get().strip()

                if not name or not category:
                    raise ValueError("Name and category cannot be empty.")

                item = ConcreteStockItem(None, name, quantity, category)
                self.warehouse.add_item(item)
                self.load_items()
                messagebox.showinfo("Success", "Item added successfully!")
                popup.destroy()
            except ValueError as e:
                messagebox.showerror("Error", f"Invalid input: {e}")

        add_button = tk.Button(popup, text="Add", command=add_item_action)
        add_button.pack(pady=10)

    def update_item_popup(self):
        """Open a popup window to update an existing item."""
        selected = self.tree.focus()
        if not selected:
            messagebox.showerror("Error", "No item selected.")
            return

        item_values = self.tree.item(selected, "values")
        item_id = int(item_values[0])

        popup = tk.Toplevel(self.root)
        popup.title("Update Item")
        popup.geometry("300x250")

        tk.Label(popup, text="Name:").pack(pady=5)
        name_entry = tk.Entry(popup)
        name_entry.insert(0, item_values[1])
        name_entry.pack(pady=5)

        tk.Label(popup, text="Quantity:").pack(pady=5)
        quantity_entry = tk.Entry(popup)
        quantity_entry.insert(0, item_values[2])
        quantity_entry.pack(pady=5)

        tk.Label(popup, text="Category:").pack(pady=5)
        category_entry = tk.Entry(popup)
        category_entry.insert(0, item_values[3])
        category_entry.pack(pady=5)

        def update_item_action():
            try:
                name = name_entry.get().strip()
                quantity_str = quantity_entry.get().strip()
                quantity = int(quantity_str)
                if quantity < 0:
                    raise ValueError("Quantity cannot be negative.")
                category = category_entry.get().strip()

                if not name or not category:
                    raise ValueError("Name and category cannot be empty.")

                updated_item = ConcreteStockItem(item_id, name, quantity, category)
                self.warehouse.update_item(updated_item)
                self.load_items()
                messagebox.showinfo("Success", "Item updated successfully!")
                popup.destroy()
            except ValueError as e:
                messagebox.showerror("Error", f"Invalid input: {e}")

        update_button = tk.Button(popup, text="Update", command=update_item_action)
        update_button.pack(pady=10)

    def remove_item(self):
        """Remove the selected item from the inventory."""
        selected = self.tree.focus()
        if not selected:
            messagebox.showerror("Error", "No item selected.")
            return

        item_id = self.tree.item(selected, "values")[0]
        try:
            self.warehouse.remove_item(int(item_id))
            self.load_items()
            messagebox.showinfo("Success", "Item removed successfully!")
        except ValueError as e:
            messagebox.showerror("Error", f"Unable to remove item: {e}")

if __name__ == "__main__":
    db_manager = DatabaseManager()
    warehouse = Warehouse(db_manager)

    root = tk.Tk()
    app = WarehouseGUI(root, warehouse)
    root.mainloop()

    db_manager.close()
