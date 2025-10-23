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

# Test Data
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
    cursor.execute("SELECT * FROM inventory WHERE itemName LIKE ?", ('%' + term + '%',))
    return cursor.fetchall()

def centreWindow(window, width, height):    # Fix found for ".eval('tk::PlaceWindow . center')" not centreing properly on modern tkinter
    window.update_idletasks()
    screen_width = window.winfo_screenwidth()
    screen_height = window.winfo_screenheight()
    x = (screen_width // 2) - (width // 2)
    y = (screen_height // 2) - (height // 2)
    window.geometry(f'{width}x{height}+{x}+{y}')

# Login 

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


# Inventory

def InventoryWindow(username):
    inv_window = tk.Tk()
    inv_window.title("Fylde Aero Inventory System")
    inv_window.geometry("800x600")
    inv_window.resizable(False, False)
    centreWindow(inv_window, 800, 600)
    header = tk.Label(
        inv_window,
        text="Fylde Aero Inventory System - Hello " + username,
        bg="#0078D7",
        fg="white",
        font=("Arial", 16, "bold"),
        pady=15
    )
    header.pack(fill=tk.X)

    # Treeview for inventory table
    columns = ("ID", "Item Name", "Quantity", "Batch Number", "Location")
    tree = ttk.Treeview(inv_window, columns=columns, show='headings')
    for col in columns:
        tree.heading(col, text=col, anchor=tk.CENTER)
        tree.column(col, width=150, anchor=tk.CENTER)
    tree.pack(fill=tk.BOTH, expand=True)

    def refresh_tree():
        for row in tree.get_children():
            tree.delete(row)
        for item in loadInv():
            tree.insert('', tk.END, values=item)

    refresh_tree()


LoginWindow.mainloop() 

# Run
LoginWindow()
