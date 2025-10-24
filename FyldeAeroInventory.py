import sqlite3 
import tkinter as tk 
from tkinter import ttk, messagebox 


# --------------- DATABASE ------------------

# Connect / create a database
conn   = sqlite3.connect('inventory.db')
cursor = conn.cursor  ()

# User table 
cursor.execute('''
CREATE TABLE IF NOT EXISTS users (
    id INTEGER PRIMARY KEY AUTOINCREMENT,
    username TEXT NOT NULL UNIQUE,
    password TEXT NOT NULL
)
''')

# Inventory table
cursor.execute('''
CREATE TABLE IF NOT EXISTS inventory (
    id INTEGER PRIMARY KEY AUTOINCREMENT,
    itemName TEXT NOT NULL,
    quantity INTEGER NOT NULL,
    BatchNumber TEXT NOT NULL,
    location TEXT NOT NULL
)
''')

# Test Data    ----------------------------------------- DELTE WHENEVER PROGRAM IS PUT TO USE
cursor.execute("INSERT OR IGNORE INTO inventory (itemName, quantity, BatchNumber, location) VALUES (?, ?, ?, ?)", ('Widget A', 100, 'BATCH001', 'Warehouse 1'))
cursor.execute("INSERT OR IGNORE INTO inventory (itemName, quantity, BatchNumber, location) VALUES (?, ?, ?, ?)", ('Widget B', 200, 'BATCH002', 'Warehouse 2'))
cursor.execute("INSERT OR IGNORE INTO inventory (itemName, quantity, BatchNumber, location) VALUES (?, ?, ?, ?)", ('Widget C', 300, 'BATCH003', 'Warehouse 3'))

# Admin user 
cursor.execute("INSERT OR IGNORE INTO users (username, password) VALUES (?, ?)", ('admin', '123')) 
conn.commit()


# --------------- APPLICATION ------------------

# Functions 

def login(username, credential):
    cursor.execute("SELECT * FROM users WHERE username=? AND password=?", (username, credential))
    return cursor.fetchone() is not None

def loadInv():
    cursor.execute("SELECT * FROM inventory")
    return cursor.fetchall()

def addItem(itemName, quantity, BatchNumber, location):
    cursor.execute("INSERT INTO inventory (itemName, quantity, BatchNumber, location) VALUES (?, ?, ?, ?)", 
                   (itemName, quantity, BatchNumber, location))
    conn.commit()

def deleteItem(item_id):
    cursor.execute("DELETE FROM inventory WHERE id=?", (item_id,))
    conn.commit()

def search(term):
    cursor.execute("SELECT * FROM inventory WHERE itemName LIKE ? or BatchNumber LIKE ?", ('%' + term + '%', '%' + term + '%'))
    return cursor.fetchall()

def updateItem(item_id, itemName, quantity, BatchNumber, location):
    cursor.execute("""
        UPDATE inventory 
        SET itemName=?, quantity=?, BatchNumber=?, location=? 
        WHERE id=?
    """, (itemName, quantity, BatchNumber, location, item_id))
    conn.commit()

def centreWindow(window, width, height):    # Fix found for ".eval('tk::PlaceWindow . center')" not centreing properly on modern tkinter
    window.update_idletasks()
    screen_width = window.winfo_screenwidth()
    screen_height = window.winfo_screenheight()
    x = (screen_width // 2) - (width // 2)
    y = (screen_height // 2) - (height // 2)
    window.geometry(f'{width}x{height}+{x}+{y}')

# Login ----------

def LoginWindow():
    login_window = tk.Tk()  
    login_window.title("Login")
    centreWindow(login_window, 300, 260)
    login_window.resizable(False, False)

    header = tk.Label(
        login_window,
        text="Welcome to Aero Inventory",
        bg="#0078D7",
        fg="white",
        font=("Arial", 16, "bold"),
        pady=15
    )
    header.pack(fill=tk.X)

    tk.Label(login_window, text="Username:", font=("Arial", 12)).pack(pady=(20,5))
    username_entry = tk.Entry(login_window, font=("Arial", 12))
    username_entry.pack(padx=50, fill=tk.X)

    tk.Label(login_window, text="Password:", font=("Arial", 12)).pack(pady=(10,5))
    credential_entry = tk.Entry(login_window, show="*", font=("Arial", 12))
    credential_entry.pack(padx=50, fill=tk.X)

    def loginTry():
        username = username_entry.get()
        credential = credential_entry.get()
        if login(username, credential):
            messagebox.showinfo("Login Successful", "Welcome to Fylde Aero Inventory System")
            login_window.destroy()
            InventoryWindow(username) 
        else:
            messagebox.showerror("Login Failed", "Invalid credentials")

    

    login_btn = tk.Button(
        login_window,
        text="Login",
        command=loginTry,
        bg="#0078D7",
        fg="white",
        font=("Arial", 10, "bold")
    )
    login_btn.pack(pady=17, padx=100, fill=tk.X)

    login_window.mainloop()


# Inventory ----------

def InventoryWindow(username):
    inv_window = tk.Tk()
    inv_window.title("Fylde Aero Inventory System")
    centreWindow(inv_window, 800, 550)

    header_frame = tk.Frame(inv_window, bg="#0078D7", pady=15)
    header_frame.pack(fill=tk.X)

    
    header_label = tk.Label(
        header_frame,
        text="Fylde Aero Inventory System - Hello " + username,
        bg="#0078D7",
        fg="white",
        font=("Arial", 16, "bold")
    )
    header_label.pack(side=tk.LEFT, padx=10) # ensures header is on left

    # search bar on the right
    search_entry = tk.Entry(header_frame, font=("Arial", 12))
    search_entry.pack(side=tk.RIGHT, padx=(0,5))

    # Search Functionality
    def do_search():
        term = search_entry.get()
        for row in tree.get_children():
            tree.delete(row)
        for item in search(term):
            tree.insert('', tk.END, values=item)

    search_btn = tk.Button(
        header_frame, 
        text="Go", 
        command=do_search,
        bg="white", 
        fg="#0078D7", 
        font=("Arial", 10, "bold")
    )
    search_btn.pack(side=tk.RIGHT, padx=(5,10))

    # Treeview for inventory table
    columns = ("ID", "Item Name", "Quantity", "Batch Number", "Location")
    tree = ttk.Treeview(inv_window, columns=columns, show='headings')
    for col in columns:
        tree.heading(col, text=col, anchor=tk.CENTER)
        tree.column(col, width=150, anchor=tk.CENTER)
    tree.pack(fill=tk.X, expand=False)
    tree.config(height=20)  # sets visible rows, tweak this number as needed

    def refresh_tree():
        for row in tree.get_children():
            tree.delete(row)
        for item in loadInv():
            tree.insert('', tk.END, values=item)

    refresh_tree()


    # Add Functionality 

    def add_item():
        add_window = tk.Toplevel(inv_window)
        add_window.title("Add Item")
        centreWindow(add_window, 300, 400)
        add_window.resizable(False, False)

        header = tk.Label(   # I reused header from login window  
            add_window,
            text="Welcome to Aero Inventory",
            bg="#0078D7",
            fg="white",
            font=("Arial", 16, "bold"),
            pady=15
        )
        header.pack(fill=tk.X)

        tk.Label(add_window, text="Item Name:", font=("Arial", 12)).pack(pady=(20,5))
        itemName_entry = tk.Entry(add_window, font=("Arial", 12))
        itemName_entry.pack(padx=50, fill=tk.X)

        tk.Label(add_window, text="Quantity:", font=("Arial", 12)).pack(pady=(10,5))
        quantity_entry = tk.Entry(add_window, font=("Arial", 12))
        quantity_entry.pack(padx=50, fill=tk.X)

        tk.Label(add_window, text="Batch Number:", font=("Arial", 12)).pack(pady=(10,5))
        BatchNumber_entry = tk.Entry(add_window, font=("Arial", 12))
        BatchNumber_entry.pack(padx=50, fill=tk.X)

        tk.Label(add_window, text="Location:", font=("Arial", 12)).pack(pady=(10,5))
        location_entry = tk.Entry(add_window, font=("Arial", 12))
        location_entry.pack(padx=50, fill=tk.X)

        def save_item():
            itemName = itemName_entry.get()
            quantity = quantity_entry.get()
            BatchNumber = BatchNumber_entry.get()
            location = location_entry.get()
            addItem(itemName, quantity, BatchNumber, location)
            refresh_tree()
            add_window.destroy()

        save_btn = tk.Button(
            add_window,
            text="Save",
            command=save_item,
            bg="#0078D7",
            fg="white",
            font=("Arial", 10, "bold")
        )
        save_btn.pack(pady=20, padx=100, fill=tk.X)


    # Delete Functionality

    def deleteSelected():
        selected = tree.selection()
        if not selected:
            messagebox.showwarning("Warning", "You have not selected item to delete.")
            return
        item = tree.item(selected[0])
        item_id = item['values'][0]  # should select id 
        deleteItem(item_id)
        refresh_tree()
        messagebox.showinfo("Deleted", "Item deleted successfully.")

    def edit_item():
        selected = tree.selection()
        if not selected:
            messagebox.showwarning("Warning", "You need to select an item to edit.")
            return

        item = tree.item(selected[0])
        item_id, itemName, quantity, BatchNumber, location = item['values']

        edit_window = tk.Toplevel(inv_window)
        edit_window.title("Edit Item")
        centreWindow(edit_window, 300, 400)
        edit_window.resizable(False, False)

        header = tk.Label(
            edit_window,
            text="Edit Inventory Item",
            bg="#0078D7",
            fg="white",
            font=("Arial", 16, "bold"),
            pady=15
        )
        header.pack(fill=tk.X)

        tk.Label(edit_window, text="Item Name:", font=("Arial", 12)).pack(pady=(20,5))
        itemName_entry = tk.Entry(edit_window, font=("Arial", 12))
        itemName_entry.pack(padx=50, fill=tk.X)
        itemName_entry.insert(0, itemName)

        tk.Label(edit_window, text="Quantity:", font=("Arial", 12)).pack(pady=(10,5))
        quantity_entry = tk.Entry(edit_window, font=("Arial", 12))
        quantity_entry.pack(padx=50, fill=tk.X)
        quantity_entry.insert(0, quantity)

        tk.Label(edit_window, text="Batch Number:", font=("Arial", 12)).pack(pady=(10,5))
        BatchNumber_entry = tk.Entry(edit_window, font=("Arial", 12))
        BatchNumber_entry.pack(padx=50, fill=tk.X)
        BatchNumber_entry.insert(0, BatchNumber)

        tk.Label(edit_window, text="Location:", font=("Arial", 12)).pack(pady=(10,5))
        location_entry = tk.Entry(edit_window, font=("Arial", 12))
        location_entry.pack(padx=50, fill=tk.X)
        location_entry.insert(0, location)

        def save_edit():
            new_itemName = itemName_entry.get()
            new_quantity = quantity_entry.get()
            new_BatchNumber = BatchNumber_entry.get()
            new_location = location_entry.get()
            updateItem(item_id, new_itemName, new_quantity, new_BatchNumber, new_location)
            refresh_tree()
            edit_window.destroy()
            messagebox.showinfo("Updated", "Item updated successfully.")

        save_btn = tk.Button(
            edit_window,
            text="Save Changes",
            command=save_edit,
            bg="#0078D7",
            fg="white",
            font=("Arial", 10, "bold")
        )
        save_btn.pack(pady=20, padx=100, fill=tk.X)

    # Buttons 
    btn_frame = tk.Frame(inv_window)
    btn_frame.pack(pady=10)

    tk.Button(btn_frame, text="Add Item", command=add_item, bg="#0078D7", fg="white", font=("Arial", 10, "bold")).grid(row=0, column=0, padx=5, pady=5)
    tk.Button(btn_frame, text="Delete Item", command=deleteSelected, bg="#0078D7", fg="white", font=("Arial", 10, "bold")).grid(row=0, column=1, padx=5, pady=5)
    tk.Button(btn_frame, text="Edit Item", command=edit_item, bg="#0078D7", fg="white", font=("Arial", 10, "bold")).grid(row=0, column=2, padx=5, pady=5)


# Run
LoginWindow()
