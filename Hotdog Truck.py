import tkinter as tk
from tkinter import messagebox
import os

menu = {
    'Classic Hotdog': {'price': 2.50, 'toppings': []},
    'Cheese Hotdog': {'price': 3.00, 'toppings': []},
    'Chili Hotdog': {'price': 3.50, 'toppings': []},
    'Veggie Hotdog': {'price': 3.50, 'toppings': []},
    'Jumbo Hotdog': {'price': 4.00, 'toppings': []},
    'Custom Hotdog': {'price': 4.50, 'toppings': {}}
}

toppings = ['Ketchup', 'Mustard', 'Mayonnaise', 'Onions', 'Relish', 'Sauerkraut', 'Chili', 'Cheese']

order_history_file = "order_history.txt"


def calculate_total_cost(order):
    total_cost = 0.0

    for hotdog, details in order.items():
        hotdog_cost = menu[hotdog]['price']
        toppings_cost = sum([menu[hotdog]['toppings'][topping] for topping in details['toppings']])
        quantity = details['quantity']
        total_cost += (hotdog_cost + toppings_cost) * quantity

    return total_cost


def place_order():
    order = {}

    for i, hotdog in enumerate(menu.keys()):
        quantity = quantity_entries[i].get()
        if quantity != "":
            try:
                quantity = int(quantity)
                if quantity <= 0:
                    messagebox.showerror("Error", "Invalid quantity. Please enter a positive number.")
                    return
            except ValueError:
                messagebox.showerror("Error", "Invalid quantity. Please enter a number.")
                return
            order[hotdog] = {'quantity': quantity, 'toppings': menu[hotdog]['toppings']}

    if not order:
        messagebox.showerror("Error", "No items selected. Please place an order.")
        return

    total_cost = calculate_total_cost(order)

    order_summary = "Order Summary:\n"
    for hotdog, details in order.items():
        hotdog_cost = menu[hotdog]['price']
        toppings = ", ".join(details['toppings'])
        order_summary += f"{hotdog} ({toppings}): {details['quantity']} - ${hotdog_cost * details['quantity']:.2f}\n"
    order_summary += f"Total Cost: ${total_cost:.2f}"

    confirmation = messagebox.askyesno("Confirm Order", order_summary + "\n\nConfirm your order?")
    if confirmation:
        messagebox.showinfo("Order Placed", "Thank you for your order!")
        save_order_to_history(order)
        clear_order_form()
    else:
        messagebox.showinfo("Order Cancelled", "Your order has been cancelled.")


def save_order_to_history(order):
    with open(order_history_file, "a") as file:
        file.write("Order:\n")
        for hotdog, details in order.items():
            hotdog_cost = menu[hotdog]['price']
            toppings = ", ".join(details['toppings'])
            file.write(f"{hotdog} ({toppings}): {details['quantity']} - ${hotdog_cost * details['quantity']:.2f}\n")
        file.write("-----------\n")


def clear_order_form():
    for entry in quantity_entries:
        entry.delete(0, tk.END)


def create_custom_hotdog():
    custom_toppings = []

    def add_topping(topping):
        if topping not in custom_toppings:
            custom_toppings.append(topping)

    custom_root = tk.Toplevel()
    custom_root.title("Custom Hotdog")

    main_frame = tk.Frame(custom_root, padx=20, pady=20, bg="#ffffff")
    main_frame.pack()

    heading_label = tk.Label(main_frame, text="Custom Hotdog", font=("Helvetica", 16, "bold"), fg="#4e8d9c",
                             bg="#ffffff")
    heading_label.pack(pady=10)

    for topping in toppings:
        topping_checkbutton = tk.Checkbutton(main_frame, text=topping, command=lambda t=topping: add_topping(t),
                                             font=("Helvetica", 12), fg="#222222", bg="#ffffff",
                                             selectcolor="#4e8d9c")
        topping_checkbutton.pack(anchor="w")

        menu['Custom Hotdog']['toppings'][topping] = 0.50

    done_button = tk.Button(custom_root, text="Done", command=custom_root.destroy, width=10,
                            font=("Helvetica", 14, "bold"), fg="#ffffff", bg="#4e8d9c")
    done_button.pack(pady=10)


def show_order_history():
    if not os.path.exists(order_history_file):
        messagebox.showinfo("Order History", "No order history found.")
    else:
        with open(order_history_file, "r") as file:
            order_history = file.read()

        messagebox.showinfo("Order History", order_history)


def create_gui():
    root = tk.Tk()
    root.title("Hotdog Stand")
    root.configure(bg="#f2f2f2")

    main_frame = tk.Frame(root, padx=20, pady=20, bg="#f2f2f2")
    main_frame.pack()

    heading_label = tk.Label(main_frame, text="Hotdog Stand", font=("Helvetica", 24, "bold"), fg="#4e8d9c", bg="#f2f2f2")
    heading_label.pack(pady=10)

    for hotdog in menu.keys():
        frame = tk.Frame(main_frame, bg="#f2f2f2")
        frame.pack(pady=5)

        hotdog_label = tk.Label(frame, text=hotdog, width=15, anchor="w", font=("Helvetica", 14), fg="#222222",
                                bg="#f2f2f2")
        hotdog_label.pack(side=tk.LEFT)

        quantity_entry = tk.Entry(frame, width=10, font=("Helvetica", 14))
        quantity_entry.pack(side=tk.LEFT)

        quantity_entries.append(quantity_entry)

    custom_button = tk.Button(root, text="Custom Hotdog", command=create_custom_hotdog, width=15,
                              font=("Helvetica", 16, "bold"), fg="#ffffff", bg="#4e8d9c")
    custom_button.pack(pady=10)

    submit_button = tk.Button(root, text="Place Order", command=place_order, width=15,
                              font=("Helvetica", 16, "bold"), fg="#ffffff", bg="#4e8d9c")
    submit_button.pack(pady=10)

    clear_button = tk.Button(root, text="Clear Order Form", command=clear_order_form, width=15,
                             font=("Helvetica", 16, "bold"), fg="#ffffff", bg="#4e8d9c")
    clear_button.pack(pady=10)

    history_button = tk.Button(root, text="Order History", command=show_order_history, width=15,
                               font=("Helvetica", 16, "bold"), fg="#ffffff", bg="#4e8d9c")
    history_button.pack(pady=10)

    root.mainloop()


if __name__ == "__main__":
    quantity_entries = []
    create_gui()
