#main.py
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
        print("4. Exit")
        choice = input("Enter your choice: ")

        if choice == '1':
            name = input("Enter item name: ")
            quantity = int(input("Enter item quantity: "))
            category = input("Enter item category: ")
            item = ConcreteStockItem(None, name, quantity, category)
            warehouse.add_item(item)
            print("Item added successfully!")

        elif choice == '2':
            try:
                item_id = int(input("Enter item ID to remove: "))
                warehouse.remove_item(item_id)
                print("Item removed successfully!")
            except ValueError:
                print("Invalid ID. Please try again.")

        elif choice == '3':
            print("\nCurrent Inventory:")
            for item in warehouse.list_items():
                print(item)

        elif choice == '4':
            print("Exiting the system. Goodbye!")
            break

        else:
            print("Invalid choice. Please try again.")

    db_manager.close()

    
