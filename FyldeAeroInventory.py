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

