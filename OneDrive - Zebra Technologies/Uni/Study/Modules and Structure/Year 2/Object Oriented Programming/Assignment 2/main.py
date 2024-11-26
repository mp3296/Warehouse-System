# main.py is a console-based application that uses the Warehouse class to manage inventory items.
# The user can add, remove, update, and view items in the inventory.
# The application uses the DatabaseManager class to interact with the SQLite database.

from warehouse_system import DatabaseManager, Warehouse, ConcreteStockItem

if __name__ == "__main__":
    db_manager = DatabaseManager()
    warehouse = Warehouse(db_manager)

    print("Welcome to the Inventory Management System")

    while True:
        print("\nMenu:")
        print("1. Add Item")
        print("2. Remove Item")
        print("3. View Inventory")
        print("4. Update Item")
        print("5. Exit")
        choice = input("Enter your choice: ")

        if choice == '1':
            # Add a new item to the inventory
            name = input("Enter item name: ").strip()
            if not name:
                print("Item name cannot be empty.")
                continue

            try:
                quantity_str = input("Enter item quantity: ").strip()
                quantity = int(quantity_str)
                if quantity < 0:
                    raise ValueError("Quantity cannot be negative.")
            except ValueError:
                print("Invalid quantity. Please enter a non-negative integer.")
                continue

            category = input("Enter item category: ").strip()
            if not category:
                print("Item category cannot be empty.")
                continue

            item = ConcreteStockItem(None, name, quantity, category)
            warehouse.add_item(item)
            print("Item added successfully!")

        elif choice == '2':
            # Remove an item from the inventory
            try:
                item_id = int(input("Enter item ID to remove: "))
                item = warehouse.get_item(item_id)
                if item is None:
                    print("Item with the specified ID does not exist.")
                    continue

                warehouse.remove_item(item_id)
                print("Item removed successfully!")

            except ValueError:
                print("Invalid ID. Please enter a valid integer.")

        elif choice == '3':
            # View the current inventory
            print("\nCurrent Inventory:")
            items = warehouse.list_items()
            if not items:
                print("No items in inventory.")
            else:
                for item in items:
                    print(item)

        elif choice == '4':
            # Update an existing item in the inventory
            try:
                item_id = int(input("Enter item ID to update: "))
                name = input("Enter new item name (leave blank to keep current): ").strip()
                quantity_str = input("Enter new item quantity (leave blank to keep current): ").strip()
                category = input("Enter new item category (leave blank to keep current): ").strip()

                current_item = warehouse.get_item(item_id)
                if not current_item:
                    print("Item not found.")
                    continue

                new_name = name if name else current_item.name
                new_quantity = int(quantity_str) if quantity_str else current_item.quantity
                if quantity_str and new_quantity < 0:
                    print("Quantity cannot be negative.")
                    continue
                new_category = category if category else current_item.category

                updated_item = ConcreteStockItem(item_id, new_name, new_quantity, new_category)
                warehouse.update_item(updated_item)
                print("Item updated successfully!")

            except ValueError:
                print("Invalid input. Please enter a valid item ID and quantity.")

        elif choice == '5':
            # Exit the application
            print("Exiting the system. Goodbye!")
            break

        else:
            print("Invalid choice. Please try again.")

    db_manager.close()
