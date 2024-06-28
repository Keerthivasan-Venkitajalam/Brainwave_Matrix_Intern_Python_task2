import tkinter as tk
from tkinter import ttk
import sqlite3

def view_database():
    conn = sqlite3.connect('users.db')
    c = conn.cursor()
    c.execute("SELECT * FROM users")
    rows = c.fetchall()
    conn.close()

    root = tk.Tk()
    root.title("View Database")
    root.geometry("400x300")

    tree = ttk.Treeview(root, columns=("ID", "Username", "Password"), show="headings")
    tree.heading("ID", text="ID")
    tree.heading("Username", text="Username")
    tree.heading("Password", text="Password")

    for row in rows:
        tree.insert("", tk.END, values=row)

    tree.pack(fill="both", expand=True)
    root.mainloop()

if __name__ == '__main__':
    view_database()
