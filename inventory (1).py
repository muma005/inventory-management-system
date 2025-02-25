import json
import datetime
import smtplib
from email.mime.text import MIMEText
from email.mime.multipart import MIMEMultipart

class Product:
    inventory = []

    def __init__(self, product_id, name, category, quantity, price, supplier):
        self.product_id = product_id
        self.name = name
        self.category = category
        self.quantity = quantity
        self.price = price
        self.supplier = supplier
        Product.inventory.append(self)

    @classmethod
    def add_product(cls, name, category, quantity, price, supplier):
        product_id = cls.inventory[-1].product_id + 1 if cls.inventory else 1
        new_product = cls(product_id, name, category, quantity, price, supplier)
        cls.audit_trail('add_product', new_product.__dict__)
        return "Product added successfully"

    @classmethod
    def update_product(cls, product_id, quantity=None, price=None, supplier=None):
        for product in cls.inventory:
            if product.product_id == product_id:
                product.quantity = quantity if quantity is not None else product.quantity
                product.price = price if price is not None else product.price
                product.supplier = supplier if supplier is not None else product.supplier
                cls.audit_trail('update_product', product.__dict__)
                return "Product information updated successfully"
        return "Product not found"

    @classmethod
    def delete_product(cls, product_id):
        for i, product in enumerate(cls.inventory):
            if product.product_id == product_id:
                cls.audit_trail('delete_product', product.__dict__)
                del cls.inventory[i]
                return "Product deleted successfully"
        return "Product not found"

    @classmethod
    def audit_trail(cls, action, details):
        with open('audit_log.txt', 'a') as log_file:
            log_entry = f"{datetime.datetime.now()} - ACTION: {action} - DETAILS: {json.dumps(details)}\n"
            log_file.write(log_entry)

    @classmethod
    def load_inventory(cls, file_path):
        with open(file_path, 'r') as file:
            data = json.load(file)
            for item in data:
                cls(item['product_id'], item['name'], item['category'], item['quantity'], item['price'], item['supplier'])

    @classmethod
    def save_inventory(cls, file_path):
        with open(file_path, 'w') as file:
            data = [product.__dict__ for product in cls.inventory]
            json.dump(data, file)

    @classmethod
    def send_notification(cls, subject, body):
        sender_email = "youremail@example.com"
        receiver_email = "receiver@example.com"
        password = "yourpassword"

        msg = MIMEMultipart()
        msg['From'] = sender_email
        msg['To'] = receiver_email
        msg['Subject'] = subject

        msg.attach(MIMEText(body, 'plain'))

        try:
            server = smtplib.SMTP('smtp.example.com', 587)
            server.starttls()
            server.login(sender_email, password)
            text = msg.as_string()
            server.sendmail(sender_email, receiver_email, text)
            server.quit()
        except Exception as e:
            print(f"Failed to send email: {e}")

class Order:
    orders = []

    def __init__(self, order_id, products=None, customer_info=None):
        self.order_id = order_id
        self.products = products if products is not None else []
        self.customer_info = customer_info
        Order.orders.append(self)

    def place_order(self, product_id, quantity, customer_info=None):
        for product in Product.inventory:
            if product.product_id == product_id and product.quantity >= quantity:
                product.quantity -= quantity
                self.products.append((product_id, quantity))
                self.customer_info = customer_info
                Order.audit_trail('place_order', self.__dict__)
                Order.send_notification("Order Placed", f"Order ID: {self.order_id} has been placed.")
                return f"Order placed successfully. Order ID: {self.order_id}"
        return "Order could not be placed. Product not found or insufficient quantity."

    @classmethod
    def audit_trail(cls, action, details):
        with open('audit_log.txt', 'a') as log_file:
            log_entry = f"{datetime.datetime.now()} - ACTION: {action} - DETAILS: {json.dumps(details)}\n"
            log_file.write(log_entry)

    @classmethod
    def send_notification(cls, subject, body):
        sender_email = "youremail@example.com"
        receiver_email = "receiver@example.com"
        password = "yourpassword"

        msg = MIMEMultipart()
        msg['From'] = sender_email
        msg['To'] = receiver_email
        msg['Subject'] = subject

        msg.attach(MIMEText(body, 'plain'))

        try:
            server = smtplib.SMTP('smtp.example.com', 587)
            server.starttls()
            server.login(sender_email, password)
            text = msg.as_string()
            server.sendmail(sender_email, receiver_email, text)
            server.quit()
        except Exception as e:
            print(f"Failed to send email: {e}")