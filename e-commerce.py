import tkinter as tk
from tkinter import messagebox, simpledialog, scrolledtext
import uuid

# --- Product Class ---
class Product:
    def __init__(self, name, price, product_id=None):
        # Validate product name
        if not isinstance(name, str) or not name:
            raise ValueError("Product name must be a non-empty string.")
        # Validate product price
        if not isinstance(price, (int, float)) or price <= 0:
            raise ValueError("Product price must be a positive number.")

        self.name = name
        self.price = float(price)
        # Generate a unique product ID if not provided
        self.product_id = product_id if product_id else str(uuid.uuid4())

    def __str__(self):
        """Returns a user-friendly string representation of the product."""
        return f"{self.name} (${self.price:.2f}) [ID: {self.product_id[:8]}...]"

    def __repr__(self):
        """Returns a string representation for developers (reconstructible)."""
        return f"Product(name='{self.name}', price={self.price}, product_id='{self.product_id}')"

# --- ShoppingCart Class ---
class ShoppingCart:
    """Manages the items in a shopping cart."""
    def __init__(self):
        """Initializes an empty shopping cart."""
        self.items = {} # Dictionary to store products: {product_id: {'product': Product, 'quantity': int}}

    def add_item(self, product, quantity=1):
        """
        Adds a product to the cart or increases its quantity if already present.
        Args:
            product (Product): The product object to add.
            quantity (int): The quantity to add (must be positive).
        Raises:
            TypeError: If the product is not a Product object.
            ValueError: If the quantity is not a positive integer.
        """
        if not isinstance(product, Product):
            raise TypeError("Only Product objects can be added to the cart.")
        if not isinstance(quantity, int) or quantity <= 0:
            raise ValueError("Quantity must be a positive integer.")

        product_id = product.product_id
        if product_id in self.items:
            self.items[product_id]['quantity'] += quantity
            messagebox.showinfo("Cart Update", f"Added {quantity} more of '{product.name}' to the cart. Total quantity: {self.items[product_id]['quantity']}.")
        else:
            self.items[product_id] = {'product': product, 'quantity': quantity}
            messagebox.showinfo("Cart Update", f"Added '{product.name}' (x{quantity}) to the cart.")
        return True # Indicate success

    def remove_item(self, product_id, quantity=None):
        """
        Removes a specified quantity of a product from the cart.
        If quantity is None or greater than/equal to current quantity, all instances are removed.
        Args:
            product_id (str): The ID of the product to remove.
            quantity (int, optional): The quantity to remove. Defaults to None.
        Raises:
            TypeError: If product_id is not a string.
        """
        if not isinstance(product_id, str):
            raise TypeError("Product ID must be a string.")

        if product_id not in self.items:
            messagebox.showinfo("Removal Failed", f"Product with ID '{product_id[:8]}...' not found in the cart.")
            return False # Indicate failure

        current_item = self.items[product_id]
        current_quantity = current_item['quantity']
        product_name = current_item['product'].name

        if quantity is None or quantity >= current_quantity:
            del self.items[product_id]
            messagebox.showinfo("Cart Update", f"Removed all instances of '{product_name}' from the cart.")
        elif isinstance(quantity, int) and 0 < quantity < current_quantity:
            self.items[product_id]['quantity'] -= quantity
            messagebox.showinfo("Cart Update", f"Removed {quantity} of '{product_name}'. Remaining: {self.items[product_id]['quantity']}.")
        else:
            messagebox.showwarning("Invalid Input", "Invalid quantity for removal. Quantity must be a positive integer or 'all'.")
            return False # Indicate failure
        return True # Indicate success

    def get_total(self):
        """Calculates and returns the total price of all items in the cart."""
        total = 0
        for item_data in self.items.values():
            total += item_data['product'].price * item_data['quantity']
        return total

    def clear_cart(self):
        """Removes all items from the shopping cart."""
        self.items = {}
        messagebox.showinfo("Cart Update", "Shopping cart has been cleared.")

# --- Tkinter GUI Application ---
class ShoppingCartApp:
    def __init__(self, master):
        self.master = master
        master.title("Simple E-commerce Shopping Cart")
        master.geometry("1000x700") # Set initial window size
        master.resizable(True, True) # Allow window resizing

        # Configure styles
        self.master.option_add('*Font', 'Inter 10')
        self.master.option_add('*Button.Background', '#4A90E2') # Blue
        self.master.option_add('*Button.Foreground', 'white')
        self.master.option_add('*Button.Relief', 'raised')
        self.master.option_add('*Button.Borderwidth', 2)

        # Initialize shopping cart and product data
        self.my_cart = ShoppingCart()
        self.products = [
            Product("Laptop", 1200.00, "prod-001"),
            Product("Wireless Mouse", 25.50, "prod-002"),
            Product("Mechanical Keyboard", 80.00, "prod-003"),
            Product("Monitor", 300.00, "prod-004"),
            Product("USB-C Hub", 45.00, "prod-005"),
            Product("Webcam", 50.00, "prod-006"),
            Product("External SSD", 150.00, "prod-007"),
            Product("Noise-Cancelling Headphones", 200.00, "prod-008"),
        ]

        # --- Main Layout (PanedWindow for resizable sections) ---
        self.main_pane = tk.PanedWindow(master, orient=tk.HORIZONTAL, sashrelief=tk.RAISED, sashwidth=5, bg='#E0E0E0')
        self.main_pane.pack(fill=tk.BOTH, expand=1, padx=10, pady=10)

        # --- Products Frame ---
        self.products_frame = tk.LabelFrame(self.main_pane, text="Available Products", padx=10, pady=10, bg='#F3F4F6', bd=2, relief=tk.GROOVE, font=('Inter', 14, 'bold'))
        self.main_pane.add(self.products_frame, width=600) # Initial width

        self.product_list_text = scrolledtext.ScrolledText(self.products_frame, width=50, height=20, wrap=tk.WORD, state=tk.DISABLED, bg='#FFFFFF', fg='#333333', font=('Inter', 11))
        self.product_list_text.pack(pady=10, padx=5, fill=tk.BOTH, expand=True)

        self.add_frame = tk.Frame(self.products_frame, bg='#F3F4F6')
        self.add_frame.pack(pady=10, fill=tk.X)

        tk.Label(self.add_frame, text="Product ID:", bg='#F3F4F6', fg='#333333').pack(side=tk.LEFT, padx=5)
        self.product_id_entry = tk.Entry(self.add_frame, width=15, bd=2, relief=tk.SUNKEN)
        self.product_id_entry.pack(side=tk.LEFT, padx=5)
        self.product_id_entry.bind('<Return>', lambda event: self.add_selected_product())

        tk.Label(self.add_frame, text="Quantity:", bg='#F3F4F6', fg='#333333').pack(side=tk.LEFT, padx=5)
        self.quantity_entry = tk.Entry(self.add_frame, width=5, bd=2, relief=tk.SUNKEN)
        self.quantity_entry.insert(0, "1")
        self.quantity_entry.pack(side=tk.LEFT, padx=5)
        self.quantity_entry.bind('<Return>', lambda event: self.add_selected_product())

        tk.Button(self.add_frame, text="Add to Cart", command=self.add_selected_product, font=('Inter', 10, 'bold')).pack(side=tk.RIGHT, padx=5)

        # --- Cart Frame ---
        self.cart_frame = tk.LabelFrame(self.main_pane, text="Your Shopping Cart", padx=10, pady=10, bg='#EBF8FF', bd=2, relief=tk.GROOVE, font=('Inter', 14, 'bold'))
        self.main_pane.add(self.cart_frame, width=400) # Initial width

        self.cart_list_text = scrolledtext.ScrolledText(self.cart_frame, width=40, height=15, wrap=tk.WORD, state=tk.DISABLED, bg='#FFFFFF', fg='#333333', font=('Inter', 11))
        self.cart_list_text.pack(pady=10, padx=5, fill=tk.BOTH, expand=True)

        self.total_label = tk.Label(self.cart_frame, text="Total: $0.00", font=('Inter', 16, 'bold'), bg='#EBF8FF', fg='#005B96')
        self.total_label.pack(pady=10)

        # Cart Action Buttons
        self.cart_buttons_frame = tk.Frame(self.cart_frame, bg='#EBF8FF')
        self.cart_buttons_frame.pack(pady=5)

        tk.Button(self.cart_buttons_frame, text="Remove Item", command=self.remove_selected_item, bg='#E53E3E', font=('Inter', 10, 'bold')).pack(side=tk.LEFT, padx=5, pady=5)
        tk.Button(self.cart_buttons_frame, text="Clear Cart", command=self.clear_cart_action, bg='#FFC107', font=('Inter', 10, 'bold')).pack(side=tk.LEFT, padx=5, pady=5)
        tk.Button(self.cart_buttons_frame, text="Checkout", command=self.checkout_action, bg='#38A169', font=('Inter', 10, 'bold')).pack(side=tk.LEFT, padx=5, pady=5)

        # Initial rendering
        self.update_product_list()
        self.update_cart_display()

    def update_product_list(self):
        """Refreshes the display of available products."""
        self.product_list_text.config(state=tk.NORMAL)
        self.product_list_text.delete(1.0, tk.END)
        if not self.products:
            self.product_list_text.insert(tk.END, "No products currently available.")
        else:
            for i, prod in enumerate(self.products):
                self.product_list_text.insert(tk.END, f"{i+1}. {prod}\n")
        self.product_list_text.config(state=tk.DISABLED)

    def update_cart_display(self):
        """Refreshes the display of items in the shopping cart."""
        self.cart_list_text.config(state=tk.NORMAL)
        self.cart_list_text.delete(1.0, tk.END)
        if not self.my_cart.items:
            self.cart_list_text.insert(tk.END, "Your shopping cart is empty.")
        else:
            for product_id, item_data in self.my_cart.items.items():
                product = item_data['product']
                quantity = item_data['quantity']
                item_subtotal = product.price * quantity
                self.cart_list_text.insert(tk.END, f"- {product.name} (x{quantity}) @ ${product.price:.2f} each | Subtotal: ${item_subtotal:.2f}\n")
        self.cart_list_text.config(state=tk.DISABLED)
        self.total_label.config(text=f"Total: ${self.my_cart.get_total():.2f}")

    def add_selected_product(self):
        """Handles adding a product to the cart based on user input."""
        product_id_input = self.product_id_entry.get().strip()
        quantity_input = self.quantity_entry.get().strip()

        if not product_id_input:
            messagebox.showwarning("Input Error", "Please enter a Product ID.")
            return

        try:
            quantity = int(quantity_input) if quantity_input else 1
            if quantity <= 0:
                raise ValueError("Quantity must be a positive integer.")
        except ValueError:
            messagebox.showwarning("Input Error", "Invalid quantity. Please enter a positive integer.")
            return

        found_product = next((p for p in self.products if p.product_id == product_id_input), None)

        if found_product:
            try:
                self.my_cart.add_item(found_product, quantity)
                self.update_cart_display()
                self.product_id_entry.delete(0, tk.END) # Clear input after successful add
                self.quantity_entry.delete(0, tk.END)
                self.quantity_entry.insert(0, "1")
            except (TypeError, ValueError) as e:
                messagebox.showerror("Error Adding Item", str(e))
        else:
            messagebox.showwarning("Product Not Found", "Product not found. Please enter a valid Product ID.")

    def remove_selected_item(self):
        """Handles removing a product from the cart based on user input."""
        if not self.my_cart.items:
            messagebox.showinfo("Cart Empty", "Your cart is empty. Nothing to remove.")
            return

        # Create a list of product IDs currently in the cart for the simpledialog dropdown
        cart_product_ids = [item_data['product'].product_id for item_data in self.my_cart.items.values()]

        # Allow user to select a product ID from those in the cart
        product_id_to_remove = simpledialog.askstring(
            "Remove Product",
            "Enter Product ID to remove (e.g., 'prod-001') or pick one from your cart:\n" +
            "\n".join([f"{item_data['product'].name} (ID: {item_id[:8]}...)" for item_id, item_data in self.my_cart.items.items()]),
            parent=self.master
        )

        if product_id_to_remove is None: # User cancelled
            return

        if product_id_to_remove not in self.my_cart.items:
            messagebox.showwarning("Not in Cart", "The entered Product ID is not in your cart.")
            return

        current_item = self.my_cart.items[product_id_to_remove]
        current_quantity = current_item['quantity']
        product_name = current_item['product'].name

        if current_quantity > 1:
            choice = messagebox.askyesno(
                "Remove Quantity",
                f"You have {current_quantity} of '{product_name}'.\n"
                "Do you want to remove ALL instances of this product?",
                icon='question'
            )
            if choice: # User chose YES to remove all
                self.my_cart.remove_item(product_id_to_remove)
            else: # User chose NO, ask for specific quantity
                quantity_to_remove_input = simpledialog.askinteger(
                    "Remove Quantity",
                    f"Enter quantity to remove for '{product_name}' (1 to {current_quantity}):",
                    minvalue=1, maxvalue=current_quantity,
                    parent=self.master
                )
                if quantity_to_remove_input is not None: # User entered a quantity
                    self.my_cart.remove_item(product_id_to_remove, quantity_to_remove_input)
                else: # User cancelled simpledialog
                    return
        else: # Only 1 item, so just remove it
            confirm = messagebox.askyesno(
                "Remove Item",
                f"Are you sure you want to remove '{product_name}' from the cart?",
                icon='warning'
            )
            if confirm:
                self.my_cart.remove_item(product_id_to_remove)
            else:
                messagebox.showinfo("Cancelled", "Item removal cancelled.")
                return

        self.update_cart_display()


    def clear_cart_action(self):
        """Handles clearing the entire shopping cart."""
        if not self.my_cart.items:
            messagebox.showinfo("Cart Empty", "Your cart is already empty.")
            return

        confirm = messagebox.askyesno(
            "Clear Cart",
            "Are you sure you want to clear your entire cart?",
            icon='warning'
        )
        if confirm:
            self.my_cart.clear_cart()
            self.update_cart_display()
        else:
            messagebox.showinfo("Cancelled", "Cart clear cancelled.")

    def checkout_action(self):
        """Simulates the checkout process."""
        if self.my_cart.get_total() <= 0:
            messagebox.showwarning("Cart Empty", "Your cart is empty. Please add items before checking out.")
            return

        confirm_payment = messagebox.askyesno(
            "Proceed to Checkout",
            f"Your total is: ${self.my_cart.get_total():.2f}.\nProceed with payment simulation?",
            icon='question'
        )

        if confirm_payment:
            messagebox.showinfo("Payment Processing", "Processing payment...")
            # Simulate a delay for payment processing
            self.master.after(1500, self._complete_checkout) # Call _complete_checkout after 1.5 seconds
        else:
            messagebox.showinfo("Payment Cancelled", "Payment cancelled. You can continue shopping.")

    def _complete_checkout(self):
        """Completes the simulated checkout process."""
        messagebox.showinfo("Payment Successful", "Payment successful! Your order has been placed.\nThank you for your purchase!")
        self.my_cart.clear_cart()
        self.update_cart_display()

# --- Main Application Entry Point ---
if __name__ == "__main__":
    root = tk.Tk()
    app = ShoppingCartApp(root)
    root.mainloop()
