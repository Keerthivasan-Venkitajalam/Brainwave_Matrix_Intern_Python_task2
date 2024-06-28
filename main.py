import tkinter as tk
from tkinter import ttk, messagebox
from login import show_login_screen
import csv
import os
from datetime import datetime

def show_main_app():
    # Create main window
    root = tk.Tk()
    root.title("Tire Shop Inventory Management")
    root.geometry("800x600")
    root.columnconfigure(0, weight=1)
    root.rowconfigure(0, weight=1)

    # Scrollable frame class to add scrollbar
    class ScrollableFrame(ttk.Frame):
        def __init__(self, container, *args, **kwargs):
            super().__init__(container, *args, **kwargs)
            canvas = tk.Canvas(self)
            scrollbar = ttk.Scrollbar(self, orient="vertical", command=canvas.yview)
            self.scrollable_frame = ttk.Frame(canvas)
            self.scrollable_frame.bind(
                "<Configure>",
                lambda e: canvas.configure(
                    scrollregion=canvas.bbox("all")
                )
            )
            canvas.create_window((0, 0), window=self.scrollable_frame, anchor="nw")
            canvas.configure(yscrollcommand=scrollbar.set)
            canvas.pack(side="left", fill="both", expand=True)
            scrollbar.pack(side="right", fill="y")

            # Enable scrolling with mouse wheel
            self.bind_all("<MouseWheel>", lambda event: canvas.yview_scroll(int(-1*(event.delta / 120)), "units"))

    # Helper functions to handle CSV operations
    def validate_positive_integer(value):
        try:
            return int(value) > 0
        except ValueError:
            return False

    def add_inventory(tire_type, quantity, brand):
        if not validate_positive_integer(quantity):
            messagebox.showerror("Error", "Quantity must be a positive integer")
            return

        inventory = []
        updated = False
        if os.path.exists('inventory.csv'):
            with open('inventory.csv', mode='r') as file:
                reader = csv.reader(file)
                inventory = [row for row in reader]

        with open('inventory.csv', mode='w', newline='') as file:
            writer = csv.writer(file)
            if not inventory:
                writer.writerow(['Tire Type', 'Brand', 'Quantity'])
            for row in inventory:
                if row[0] == tire_type and row[1] == brand:
                    row[2] = str(int(row[2]) + int(quantity))
                    updated = True
                writer.writerow(row)
            if not updated:
                writer.writerow([tire_type, brand, quantity])

        messagebox.showinfo("Success", "Inventory added/updated successfully")

    def record_purchase(customer_name, tire_type, brand, quantity, price_per_tire):

        inventory = []
        purchase_successful = True

        if os.path.exists('inventory.csv'):
            with open('inventory.csv', mode='r') as file:
                reader = csv.reader(file)
                inventory = [row for row in reader]

        with open('inventory.csv', mode='w', newline='') as file:
            writer = csv.writer(file)
            for row in inventory:
                if row[0] == tire_type and row[2] == brand:
                    if int(row[1]) >= int(quantity):
                        row[1] = str(int(row[1]) - int(quantity))
                        purchase_successful = True
                writer.writerow(row)
            if not purchase_successful:
                messagebox.showerror("Error", "Insufficient inventory for purchase")
                return

        file_exists = os.path.isfile('sales.csv')
        with open('sales.csv', mode='a', newline='') as file:
            writer = csv.writer(file)
            if not file_exists:
                writer.writerow(['Customer Name', 'Tire Type', 'Brand', 'Quantity', 'Price per Tire', 'Date'])
            timestamp = datetime.now().strftime('%Y-%m-%d %H:%M:%S')
            print(f"Recording row: {[customer_name, tire_type, brand, quantity, price_per_tire, timestamp]}")
            writer.writerow([customer_name, tire_type, brand, quantity, price_per_tire, timestamp])

        messagebox.showinfo("Success", "Purchase recorded successfully")

                
    def display_table(data, headers, title):
        table_window = tk.Toplevel(root)
        table_window.title(title)
        table_window.geometry("600x400")
        table_window.columnconfigure(0, weight=1)
        table_window.rowconfigure(0, weight=1)
        
        tree = ttk.Treeview(table_window, columns=headers, show='headings')
        for header in headers:
            tree.heading(header, text=header)
            tree.column(header, anchor=tk.CENTER)

        for row in data:
            tree.insert('', tk.END, values=row)

        tree.pack(fill='both', expand=True)
        
        # Add double-click functionality for editing inventory
        if title == "Search Results (Double-click to edit)":
            tree.bind("<Double-1>", lambda event: on_double_click(event, tree))
            
    def display_inventory():
        if os.path.exists('inventory.csv'):
            with open('inventory.csv', mode='r') as file:
                reader = csv.reader(file)
                inventory = [row for row in reader]
                display_table(inventory[1:], inventory[0], "Inventory")

    def display_purchase_history():
        if os.path.exists('sales.csv'):
            with open('sales.csv', mode='r') as file:
                reader = csv.reader(file)
                sales = [row for row in reader]
                headers = ['Customer Name', 'Tire Type', 'Brand', 'Quantity', 'Price per Tire', 'Total', 'Date']
                display_table(sales[1:], headers, "Purchase History")

    def display_total_earnings():
        total_earnings = 0
        if os.path.exists('sales.csv'):
            with open('sales.csv', mode='r') as file:
                reader = csv.reader(file)
                next(reader)  # Skip header
                for row in reader:
                    total_earnings += int(row[5])
        messagebox.showinfo("Total Earnings", f"Total Earnings: ${total_earnings}")

    def display_total_tires_sold():
        total_tires_sold = 0
        if os.path.exists('sales.csv'):
            with open('sales.csv', mode='r') as file:
                reader = csv.reader(file)
                next(reader)  # Skip header
                for row in reader:
                    total_tires_sold += int(row[3])
        messagebox.showinfo("Total Tires Sold", f"Total Tires Sold: {total_tires_sold}")

    def search_inventory(tire_type, brand):
        if os.path.exists('inventory.csv'):
            with open('inventory.csv', mode='r') as file:
                reader = csv.reader(file)
                inventory = [row for row in reader]
                headers = inventory[0]
                search_results = [
                    row for row in inventory[1:]
                    if (tire_type == "" or tire_type.lower() == row[0].lower()) and 
                    (brand == "" or brand.lower() == row[1].lower())
                ]
                display_table(search_results, headers, "Search Results (Double-click to edit)")

    def search_purchases(customer_name_search, tire_type, brand):
        if os.path.exists('sales.csv'):
            with open('sales.csv', mode='r') as file:
                reader = csv.reader(file)
                sales = [row for row in reader]
                headers = sales[0]
                search_results = [
                    row for row in sales[1:]
                    if (customer_name_search == "" or customer_name_search.lower() in row[0].lower()) and
                    (tire_type == "" or tire_type.lower() == row[1].lower()) and
                    (brand == "" or brand.lower() == row[2].lower())
                ]
                display_table(search_results, headers, "Search Results")

    def edit_inventory(original_tire_type, original_brand, new_tire_type, new_quantity, new_brand):
        if not validate_positive_integer(new_quantity):
            messagebox.showerror("Error", "New quantity must be a positive integer")
            return

        inventory = []
        updated = False
        if os.path.exists('inventory.csv'):
            with open('inventory.csv', mode='r') as file:
                reader = csv.reader(file)
                inventory = [row for row in reader]

        with open('inventory.csv', mode='w', newline='') as file:
            writer = csv.writer(file)
            for row in inventory:
                if row[0] == original_tire_type and row[1] == original_brand:
                    row[0] = new_tire_type
                    row[1] = new_brand
                    row[2] = new_quantity
                    updated = True
                writer.writerow(row)

        if updated:
            messagebox.showinfo("Success", "Inventory updated successfully")
        else:
            messagebox.showerror("Error", "No matching tire type and brand found")

    def on_double_click(event, tree):
        selected_item = tree.selection()[0]
        item = tree.item(selected_item)
        values = item['values']
        edit_inventory_window(values[0], values[2], values[1])  # Reordered to Tire Type, Quantity, Brand

    def edit_inventory_window(tire_type, quantity, brand):
        edit_window = tk.Toplevel(root)
        edit_window.title("Edit Inventory")
        edit_window.geometry("400x300")

        ttk.Label(edit_window, text="Tire Type:").grid(row=0, column=0, padx=5, pady=5, sticky="e")
        tire_type_var = tk.StringVar(value=tire_type)
        tire_type_menu = ttk.Combobox(edit_window, textvariable=tire_type_var, values=sorted(tire_types))
        tire_type_menu.grid(row=0, column=1, padx=5, pady=5, sticky="ew")

        ttk.Label(edit_window, text="Brand:").grid(row=1, column=0, padx=5, pady=5, sticky="e")
        brand_var = tk.StringVar(value=brand)
        brand_menu = ttk.Combobox(edit_window, textvariable=brand_var, values=sorted(brands))
        brand_menu.grid(row=1, column=1, padx=5, pady=5, sticky="ew")

        ttk.Label(edit_window, text="Quantity:").grid(row=2, column=0, padx=5, pady=5, sticky="e")
        quantity_var = tk.StringVar(value=quantity)
        ttk.Entry(edit_window, textvariable=quantity_var).grid(row=2, column=1, padx=5, pady=5, sticky="ew")

        ttk.Button(edit_window, text="Save Changes", command=lambda: [edit_inventory(tire_type, brand, tire_type_var.get(), quantity_var.get(), brand_var.get()), edit_window.destroy()]).grid(row=3, columnspan=2, pady=10)

    def add_customer(name, email, phone):
        if not name or not email or not phone:
            messagebox.showerror("Error", "All fields must be filled out")
            return

        customers = []
        if os.path.exists('customers.csv'):
            with open('customers.csv', mode='r') as file:
                reader = csv.reader(file)
                customers = [row for row in reader]

        with open('customers.csv', mode='a', newline='') as file:
            writer = csv.writer(file)
            if not customers:
                writer.writerow(['Name', 'Email', 'Phone'])
            writer.writerow([name, email, phone])

        messagebox.showinfo("Success", "Customer added successfully")

    def search_customers(name, email, phone):
        if not os.path.exists('customers.csv'):
            messagebox.showinfo("Information", "No customer data available")
            return []

        with open('customers.csv', mode='r') as file:
            reader = csv.reader(file)
            customers = [row for row in reader]

        search_results = []
        for customer in customers:
            if (name and name.lower() in customer[0].lower()) or \
            (email and email.lower() in customer[1].lower()) or \
            (phone and phone in customer[2]):
                search_results.append(customer)

        return search_results

    def display_customer_search_results(results):
        if not results:
            messagebox.showinfo("Information", "No matching customers found")
            return

        popup = tk.Toplevel()
        popup.title("Search Results")
        popup.geometry("400x300")

        columns = ['Name', 'Email', 'Phone']
        tree = ttk.Treeview(popup, columns=columns, show='headings')
        for col in columns:
            tree.heading(col, text=col)

        for row in results:
            tree.insert('', 'end', values=row)

        tree.pack(fill='both', expand=True)

    # Main layout
    frame_main = ScrollableFrame(root)
    frame_main.grid(row=0, column=0, sticky="nsew")

    # Inventory management section
    ttk.Label(frame_main.scrollable_frame, text="Inventory Management", font=("Helvetica", 16)).pack(pady=10)
    frame_inventory = ttk.Frame(frame_main.scrollable_frame)
    frame_inventory.pack(pady=10)

    tire_types = ["Car", "Truck", "Motorcycle", "SUV"]
    brands = ["Bridgestone", "Continental", "Cooper", "Dunlop", "Goodyear", "Hankook", "Michelin", "Pirelli", "Toyo", "Yokohama"]

    ttk.Label(frame_inventory, text="Tire Type:").grid(row=0, column=0, padx=5, pady=5, sticky="e")
    tire_type_var = tk.StringVar()
    tire_type_menu = ttk.Combobox(frame_inventory, textvariable=tire_type_var, values=sorted(tire_types))
    tire_type_menu.grid(row=0, column=1, padx=5, pady=5, sticky="ew")

    ttk.Label(frame_inventory, text="Brand:").grid(row=1, column=0, padx=5, pady=5, sticky="e")
    brand_var = tk.StringVar()
    brand_menu = ttk.Combobox(frame_inventory, textvariable=brand_var, values=sorted(brands))
    brand_menu.grid(row=1, column=1, padx=5, pady=5, sticky="ew")

    ttk.Label(frame_inventory, text="Quantity:").grid(row=2, column=0, padx=5, pady=5, sticky="e")
    quantity_var = tk.StringVar()
    ttk.Entry(frame_inventory, textvariable=quantity_var).grid(row=2, column=1, padx=5, pady=5, sticky="ew")

    ttk.Button(frame_inventory, text="Add/Update Inventory", command=lambda: add_inventory(tire_type_var.get(), quantity_var.get(), brand_var.get())).grid(row=3, columnspan=2, pady=10)

    # Search and edit inventory section
    ttk.Label(frame_main.scrollable_frame, text="Search and Edit Inventory", font=("Helvetica", 16)).pack(pady=10)
    frame_search_edit = ttk.Frame(frame_main.scrollable_frame)
    frame_search_edit.pack(pady=10)

    ttk.Label(frame_search_edit, text="Tire Type:").grid(row=0, column=0, padx=5, pady=5, sticky="e")
    search_tire_type_var = tk.StringVar()
    search_tire_type_menu = ttk.Combobox(frame_search_edit, textvariable=search_tire_type_var, values=[""] + sorted(tire_types))
    search_tire_type_menu.grid(row=0, column=1, padx=5, pady=5, sticky="ew")

    ttk.Label(frame_search_edit, text="Brand:").grid(row=1, column=0, padx=5, pady=5, sticky="e")
    search_brand_var = tk.StringVar()
    search_brand_menu = ttk.Combobox(frame_search_edit, textvariable=search_brand_var, values=[""] + sorted(brands))
    search_brand_menu.grid(row=1, column=1, padx=5, pady=5, sticky="ew")

    ttk.Button(frame_search_edit, text="Search Inventory", command=lambda: search_inventory(search_tire_type_var.get(), search_brand_var.get())).grid(row=2, columnspan=2, pady=10)

    # Purchase recording section
    ttk.Label(frame_main.scrollable_frame, text="Record Purchase", font=("Helvetica", 16)).pack(pady=10)
    frame_purchase = ttk.Frame(frame_main.scrollable_frame)
    frame_purchase.pack(pady=10)

    ttk.Label(frame_purchase, text="Customer Name:").grid(row=0, column=0, padx=5, pady=5, sticky="e")
    customer_name_var = tk.StringVar()
    ttk.Entry(frame_purchase, textvariable=customer_name_var).grid(row=0, column=1, padx=5, pady=5)
    
    ttk.Label(frame_purchase, text="Tire Type:").grid(row=1, column=0, padx=5, pady=5, sticky="e")
    purchase_tire_type_var = tk.StringVar()
    purchase_tire_type_menu = ttk.Combobox(frame_purchase, textvariable=purchase_tire_type_var, values=sorted(['Car', 'Truck', 'Motorcycle', 'SUV']))
    purchase_tire_type_menu.grid(row=1, column=1, padx=5, pady=5, sticky="ew")

    ttk.Label(frame_purchase, text="Brand:").grid(row=2, column=0, padx=5, pady=5, sticky="e")
    purchase_brand_var = tk.StringVar()
    purchase_brand_menu = ttk.Combobox(frame_purchase, textvariable=purchase_brand_var, values=sorted(['Michelin', 'Goodyear', 'Continental', 'Pirelli', 'Bridgestone', 'Dunlop', 'Yokohama', 'Toyo', 'Hankook', 'Cooper']))
    purchase_brand_menu.grid(row=2, column=1, padx=5, pady=5, sticky="ew")

    ttk.Label(frame_purchase, text="Quantity:").grid(row=3, column=0, padx=5, pady=5, sticky="e")
    purchase_quantity_var = tk.StringVar()
    ttk.Entry(frame_purchase, textvariable=purchase_quantity_var).grid(row=3, column=1, padx=5, pady=5, sticky="ew")

    ttk.Label(frame_purchase, text="Price per Tire:").grid(row=4, column=0, padx=5, pady=5, sticky="e")
    price_per_tire_var = tk.StringVar()
    ttk.Entry(frame_purchase, textvariable=price_per_tire_var).grid(row=4, column=1, padx=5, pady=5, sticky="ew")

    ttk.Button(frame_purchase, text="Record Purchase", command=lambda: record_purchase(customer_name_var.get(), purchase_tire_type_var.get(), purchase_brand_var.get(), purchase_quantity_var.get(), price_per_tire_var.get())).grid(row=5, columnspan=2, pady=10)


    # Search purchase section
    ttk.Label(frame_main.scrollable_frame, text="Search Purchases", font=("Helvetica", 16)).pack(pady=10)
    frame_search_purchase = ttk.Frame(frame_main.scrollable_frame)
    frame_search_purchase.pack(pady=10)

    ttk.Label(frame_search_purchase, text="Customer Name:").grid(row=0, column=0, padx=5, pady=5, sticky="e")
    search_customer_name_var = tk.StringVar()
    ttk.Entry(frame_search_purchase, textvariable=search_customer_name_var).grid(row=0, column=1, padx=5, pady=5, sticky="ew")

    ttk.Label(frame_search_purchase, text="Tire Type:").grid(row=1, column=0, padx=5, pady=5, sticky="e")
    search_purchase_tire_type_var = tk.StringVar()
    search_purchase_tire_type_menu = ttk.Combobox(frame_search_purchase, textvariable=search_purchase_tire_type_var, values=[""] + sorted(tire_types))
    search_purchase_tire_type_menu.grid(row=1, column=1, padx=5, pady=5, sticky="ew")

    ttk.Label(frame_search_purchase, text="Brand:").grid(row=2, column=0, padx=5, pady=5, sticky="e")
    search_purchase_brand_var = tk.StringVar()
    search_purchase_brand_menu = ttk.Combobox(frame_search_purchase, textvariable=search_purchase_brand_var, values=[""] + sorted(brands))
    search_purchase_brand_menu.grid(row=2, column=1, padx=5, pady=5, sticky="ew")

    ttk.Button(frame_search_purchase, text="Search Purchases", command=lambda: search_purchases(search_customer_name_var.get(), search_purchase_tire_type_var.get(), search_purchase_brand_var.get())).grid(row=3, columnspan=2, pady=10)

    # Display data section
    ttk.Label(frame_main.scrollable_frame, text="Display Data", font=("Helvetica", 16)).pack(pady=10)
    frame_display_buttons = ttk.Frame(frame_main.scrollable_frame)
    frame_display_buttons.pack(pady=10)

    ttk.Button(frame_display_buttons, text="Display Inventory", command=display_inventory).grid(row=0, column=0, padx=5, pady=5)
    ttk.Button(frame_display_buttons, text="Display Purchase History", command=display_purchase_history).grid(row=0, column=1, padx=5, pady=5)
    ttk.Button(frame_display_buttons, text="Display Total Earnings", command=display_total_earnings).grid(row=1, column=0, padx=5, pady=5)
    ttk.Button(frame_display_buttons, text="Display Total Tires Sold", command=display_total_tires_sold).grid(row=1, column=1, padx=5, pady=5)

    # Frame for displaying data
    frame_display = ttk.Frame(frame_main.scrollable_frame)
    frame_display.pack(fill='both', expand=True, padx=10, pady=10)

    # Add customer section
    ttk.Label(frame_main.scrollable_frame, text="Add Customer", font=("Helvetica", 16)).pack(pady=10)
    frame_add_customer = ttk.Frame(frame_main.scrollable_frame)
    frame_add_customer.pack(pady=10)

    ttk.Label(frame_add_customer, text="Name:").grid(row=0, column=0, padx=5, pady=5, sticky="e")
    customer_name_add_var = tk.StringVar()
    customer_name_add_entry = ttk.Entry(frame_add_customer, textvariable=customer_name_add_var)
    customer_name_add_entry.grid(row=0, column=1, padx=5, pady=5, sticky="ew")

    ttk.Label(frame_add_customer, text="Email:").grid(row=1, column=0, padx=5, pady=5, sticky="e")
    customer_email_var = tk.StringVar()
    customer_email_entry = ttk.Entry(frame_add_customer, textvariable=customer_email_var)
    customer_email_entry.grid(row=1, column=1, padx=5, pady=5, sticky="ew")

    ttk.Label(frame_add_customer, text="Phone:").grid(row=2, column=0, padx=5, pady=5, sticky="e")
    customer_phone_var = tk.StringVar()
    customer_phone_entry = ttk.Entry(frame_add_customer, textvariable=customer_phone_var)
    customer_phone_entry.grid(row=2, column=1, padx=5, pady=5, sticky="ew")

    ttk.Button(frame_add_customer, text="Add Customer", command=lambda: add_customer(customer_name_add_var.get(), customer_email_var.get(), customer_phone_var.get())).grid(row=3, columnspan=2, pady=10)

    # Search customer section
    ttk.Label(frame_main.scrollable_frame, text="Search Customer", font=("Helvetica", 16)).pack(pady=10)
    frame_search_customer = ttk.Frame(frame_main.scrollable_frame)
    frame_search_customer.pack(pady=10)

    ttk.Label(frame_search_customer, text="Name:").grid(row=0, column=0, padx=5, pady=5)
    search_customer_name_var = tk.StringVar()
    search_customer_name_entry = ttk.Entry(frame_search_customer, textvariable=search_customer_name_var)
    search_customer_name_entry.grid(row=0, column=1, padx=5, pady=5, sticky="ew")

    ttk.Label(frame_search_customer, text="Email:").grid(row=1, column=0, padx=5, pady=5)
    search_customer_email_var = tk.StringVar()
    search_customer_email_entry = ttk.Entry(frame_search_customer, textvariable=search_customer_email_var)
    search_customer_email_entry.grid(row=1, column=1, padx=5, pady=5, sticky="ew")

    ttk.Label(frame_search_customer, text="Phone:").grid(row=2, column=0, padx=5, pady=5)
    search_customer_phone_var = tk.StringVar()
    search_customer_phone_entry = ttk.Entry(frame_search_customer, textvariable=search_customer_phone_var)
    search_customer_phone_entry.grid(row=2, column=1, padx=5, pady=5)

    ttk.Button(frame_search_customer, text="Search Customers", command=lambda: display_customer_search_results(search_customers(search_customer_name_var.get(), search_customer_email_var.get(), search_customer_phone_var.get()))).grid(row=3, columnspan=2, pady=10)

    # Run the main loop
    root.mainloop()

show_login_screen(show_main_app)