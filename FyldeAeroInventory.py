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


# Login 

def LoginWindow():
    login_window = tk.Tk()  
    login_window.title("Login")
    login_window.geometry("300x260")
    login_window.resizable(False, False)
    login_window.eval('tk::PlaceWindow . center')

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
        if login(username_entry.get(), credential_entry.get()):
            messagebox.showinfo("Login Successful", "Welcome to Fylde Aero Inventory System")
            login_window.destroy()
            InventoryWindow() 
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

def InventoryWindow():
    inv_window = tk.Tk()
    inv_window.title("Fylde Aero Inventory System")
    inv_window.geometry("800x600")
    inv_window.resizable(False, False)
    inv_window.eval('tk::PlaceWindow . center')

    header = tk.Label(
        inv_window,
        text="Fylde Aero Inventory System",
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
        tree.heading(col, text=col)
        tree.column(col, width=150)
    tree.pack(fill=tk.BOTH, expand=True)

    def refresh_tree():
        for row in tree.get_children():
            tree.delete(row)
        for item in loadInv():
            tree.insert('', tk.END, values=item)

    refresh_tree()

    inv_window.mainloop() 


# Run
LoginWindow()
