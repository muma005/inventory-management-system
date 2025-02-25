import tkinter as tk
from tkinter import messagebox, ttk
from inventory import Product, Order
import json

class InventoryGUI:
    def __init__(self, master):
        self.master = master
        master.title("Retail Inventory System")

        # Tab Control
        self.tab_control = ttk.Notebook(master)
        
        self.admin_tab = ttk.Frame(self.tab_control)
        self.buyer_tab = ttk.Frame(self.tab_control)

        self.tab_control.add(self.admin_tab, text="Admin")
        self.tab_control.add(self.buyer_tab, text="Buyer")
        self.tab_control.pack(expand=1, fill="both")

        self.create_admin_interface()
        self.create_buyer_interface()
        self.update_display()

    def create_admin_interface(self):
        # --- Product Management ---
        product_frame = tk.LabelFrame(self.admin_tab, text="Product Management")
        product_frame.grid(row=0, column=0, padx=10, pady=10, sticky="nsew")

        tk.Label(product_frame, text="Name:").grid(row=0, column=0, sticky="w")
        self.product_name_entry = tk.Entry(product_frame)
        self.product_name_entry.grid(row=0, column=1, sticky="ew")

        tk.Label(product_frame, text="Category:").grid(row=1, column=0, sticky="w")
        self.product_category_entry = tk.Entry(product_frame)
        self.product_category_entry.grid(row=1, column=1, sticky="ew")

        tk.Label(product_frame, text="Quantity:").grid(row=2, column=0, sticky="w")
        self.product_quantity_entry = tk.Entry(product_frame)
        self.product_quantity_entry.grid(row=2, column=1, sticky="ew")

        tk.Label(product_frame, text="Price:").grid(row=3, column=0, sticky="w")
        self.product_price_entry = tk.Entry(product_frame)
        self.product_price_entry.grid(row=3, column=1, sticky="ew")

        tk.Label(product_frame, text="Supplier:").grid(row=4, column=0, sticky="w")
        self.product_supplier_entry = tk.Entry(product_frame)
        self.product_supplier_entry.grid(row=4, column=1, sticky="ew")

        add_product_button = tk.Button(product_frame, text="Add Product", command=self.add_product)
        add_product_button.grid(row=5, column=0, columnspan=2, pady=(5,0))

        update_product_button = tk.Button(product_frame, text="Update Product", command=self.update_product)
        update_product_button.grid(row=6, column=0, columnspan=2, pady=(5,0))

        delete_product_button = tk.Button(product_frame, text="Delete Product", command=self.delete_product)
        delete_product_button.grid(row=7, column=0, columnspan=2, pady=(5,0))

        load_inventory_button = tk.Button(product_frame, text="Load Inventory", command=self.load_inventory)
        load_inventory_button.grid(row=8, column=0, columnspan=2, pady=(5,0))

        save_inventory_button = tk.Button(product_frame, text="Save Inventory", command=self.save_inventory)
        save_inventory_button.grid(row=9, column=0, columnspan=2, pady=(5,0))

        # --- Order Management ---
        order_frame = tk.LabelFrame(self.admin_tab, text="Order Management")
        order_frame.grid(row=1, column=0, padx=10, pady=10, sticky="nsew")

        tk.Label(order_frame, text="Product ID:").grid(row=0, column=0, sticky="w")
        self.order_product_id_entry = tk.Entry(order_frame)
        self.order_product_id_entry.grid(row=0, column=1, sticky="ew")

        tk.Label(order_frame, text="Quantity:").grid(row=1, column=0, sticky="w")
        self.order_quantity_entry = tk.Entry(order_frame)
        self.order_quantity_entry.grid(row=1, column=1, sticky="ew")

        tk.Label(order_frame, text="Customer Info:").grid(row=2, column=0, sticky="w")
        self.order_customer_info_entry = tk.Entry(order_frame)
        self.order_customer_info_entry.grid(row=2, column=1, sticky="ew")

        place_order_button = tk.Button(order_frame, text="Place Order", command=self.place_order)
        place_order_button.grid(row=3, column=0, columnspan=2, pady=(5,0))

        # --- Display Area ---
        self.display_area = tk.Text(self.admin_tab, height=10, width=50)
        self.display_area.grid(row=2, column=0, padx=10, pady=10, sticky="nsew")

    def create_buyer_interface(self):
        # --- Buyer's Interface ---
        buyer_frame = tk.LabelFrame(self.buyer_tab, text="Products Available")
        buyer_frame.grid(row=0, column=0, padx=10, pady=10, sticky="nsew")

        self.product_listbox = tk.Listbox(buyer_frame)
        self.product_listbox.grid(row=0, column=0, columnspan=2, sticky="nsew")

        tk.Label(buyer_frame, text="Product ID:").grid(row=1, column=0, sticky="w")
        self.buyer_product_id_entry = tk.Entry(buyer_frame)
        self.buyer_product_id_entry.grid(row=1, column=1, sticky="ew")

        tk.Label(buyer_frame, text="Quantity:").grid(row=2, column=0, sticky="w")
        self.buyer_quantity_entry = tk.Entry(buyer_frame)
        self.buyer_quantity_entry.grid(row=2, column=1, sticky="ew")

        tk.Label(buyer_frame, text="Customer Info:").grid(row=3, column=0, sticky="w")
        self.buyer_customer_info_entry = tk.Entry(buyer_frame)
        self.buyer_customer_info_entry.grid(row=3, column=1, sticky="ew")

        add_to_cart_button = tk.Button(buyer_frame, text="Add to Cart", command=self.add_to_cart)
        add_to_cart_button.grid(row=4, column=0, columnspan=2, pady=(5,0))

        self.cart_area = tk.Text(self.buyer_tab, height=10, width=50)
        self.cart_area.grid(row=5, column=0, padx=10, pady=10, sticky="nsew")

        self.total_price_label = tk.Label(self.buyer_tab, text="Total Price: $0.00")
        self.total_price_label.grid(row=6, column=0, padx=10, pady=10, sticky="nsew")

    def add_product(self):
        try:
            name = self.product_name_entry.get()
            category = self.product_category_entry.get()
            quantity = int(self.product_quantity_entry.get())
            price = float(self.product_price_entry.get())
            supplier = self.product_supplier_entry.get()

            Product.add_product(name, category, quantity, price, supplier)
            messagebox.showinfo("Success", "Product added successfully!")
            self.clear_product_fields()
            self.update_display()
        except ValueError:
            messagebox.showerror("Error", "Invalid input. Please check your data.")
        except Exception as e:
            messagebox.showerror("Error", f"An error occurred: {e}")

    def update_product(self):
        try:
            product_id_str = self.product_name_entry.get() #we are using the name field to search for the product_id
            product_id = None
            for product in Product.inventory:
                if product.name == product_id_str:
                    product_id = product.product_id
                    break
            if product_id is None:
                raise ValueError("Product not found")

            quantity = self.product_quantity_entry.get()
            quantity = int(quantity) if quantity else None
            price = self.product_price_entry.get()
            price = float(price) if price else None
            supplier = self.product_supplier_entry.get()

            Product.update_product(product_id, quantity, price, supplier)
            messagebox.showinfo("Success", "Product updated successfully!")
            self.clear_product_fields()
            self.update_display()
        except ValueError as e:
            messagebox.showerror("Error", f"Invalid input or {e}")
        except Exception as e:
            messagebox.showerror("Error", f"An error occurred: {e}")

    def delete_product(self):
        try:
            product_id_str = self.product_name_entry.get() #we are using the name field to search for the product_id
            product_id = None
            for product in Product.inventory:
                if product.name == product_id_str:
                    product_id = product.product_id
                    break
            if product_id is None:
                raise ValueError("Product not found")

            Product.delete_product(product_id)
            messagebox.showinfo("Success", "Product deleted successfully!")
            self.clear_product_fields()
            self.update_display()
        except ValueError as e:
            messagebox.showerror("Error", f"Invalid input or {e}")
        except Exception as e:
            messagebox.showerror("Error", f"An error occurred: {e}")

    def place_order(self):
        try:
            product_id = int(self.order_product_id_entry.get())
            quantity = int(self.order_quantity_entry.get())
            customer_info = self.order_customer_info_entry.get()

            order = Order(order_id=len(Order.orders) + 1)
            result = order.place_order(product_id, quantity, customer_info)
            if "successfully" in result:
                messagebox.showinfo("Success", result)
            else:
                messagebox.showerror("Error", result)
            self.clear_order_fields()
            self.update_display()
        except ValueError:
            messagebox.showerror("Error", "Invalid input. Please check your data.")
        except Exception as e:
            messagebox.showerror("Error", f"An error occurred: {e}")

    def add_to_cart(self):
        try:
            product_id = int(self.buyer_product_id_entry.get())
            quantity = int(self.buyer_quantity_entry.get())
            customer_info = self.buyer_customer_info_entry.get()

            product_found = None
            for product in Product.inventory:
                if product.product_id == product_id:
                    product_found = product
                    break
            if product_found is None or product_found.quantity < quantity:
                raise ValueError("Product not found or insufficient quantity")

            product_found.quantity -= quantity
            self.cart_area.insert(tk.END, f"Product ID: {product_id}, Quantity: {quantity}, Price: ${product_found.price * quantity}\n")
            self.update_total_price()
            self.clear_buyer_fields()
        except ValueError as e:
            messagebox.showerror("Error", f"Invalid input or {e}")
        except Exception as e:
            messagebox.showerror("Error", f"An error occurred: {e}")

    def update_total_price(self):
        total_price = 0.0
        cart_content = self.cart_area.get("1.0", tk.END).strip().split("\n")
        for item in cart_content:
            if item:
                price = float(item.split("Price: $")[1])
                total_price += price
        self.total_price_label.config(text=f"Total Price: ${total_price:.2f}")

    def load_inventory(self):
        try:
            file_path = "inventory.json"
            Product.load_inventory(file_path)
            messagebox.showinfo("Success", "Inventory loaded successfully!")
            self.update_display()
        except Exception as e:
            messagebox.showerror("Error", f"An error occurred while loading inventory: {e}")

    def save_inventory(self):
        try:
            file_path = "inventory.json"
            Product.save_inventory(file_path)
            messagebox.showinfo("Success", "Inventory saved successfully!")
        except Exception as e:
            messagebox.showerror("Error", f"An error occurred while saving inventory: {e}")

    def clear_product_fields(self):
        self.product_name_entry.delete(0, tk.END)
        self.product_category_entry.delete(0, tk.END)
        self.product_quantity_entry.delete(0, tk.END)
        self.product_price_entry.delete(0, tk.END)
        self.product_supplier_entry.delete(0, tk.END)

    def clear_order_fields(self):
        self.order_product_id_entry.delete(0, tk.END)
        self.order_quantity_entry.delete(0, tk.END)
        self.order_customer_info_entry.delete(0, tk.END)

    def clear_buyer_fields(self):
        self.buyer_product_id_entry.delete(0, tk.END)
        self.buyer_quantity_entry.delete(0, tk.END)
        self.buyer_customer_info_entry.delete(0, tk.END)

    def update_display(self):
        self.display_area.delete("1.0", tk.END)
        for product in Product.inventory:
            self.display_area.insert(tk.END, f"ID: {product.product_id}, Name: {product.name}, Category: {product.category}, Quantity: {product.quantity}, Price: {product.price}, Supplier: {product.supplier}\n")

        self.product_listbox.delete(0, tk.END)
        for product in Product.inventory:
            self.product_listbox.insert(tk.END, f"{product.product_id}: {product.name} - {product.category} - {product.quantity} in stock - ${product.price}")