import tkinter as tk
from tkinter import ttk, messagebox
import sqlite3
from authentication import delete_user

def delete_user_gui():
    def refresh_user_list():
        conn = sqlite3.connect('users.db')
        c = conn.cursor()
        c.execute("SELECT username FROM users")
        users = c.fetchall()
        conn.close()
        user_list_var.set([user[0] for user in users])

    def delete_selected_user():
        selected_user = user_listbox.get(tk.ACTIVE)
        if delete_user(selected_user):
            messagebox.showinfo("Delete User", f"User '{selected_user}' deleted successfully")
            refresh_user_list()
        else:
            messagebox.showerror("Delete User", f"Failed to delete user '{selected_user}'")

    root = tk.Tk()
    root.title("Delete User")
    root.geometry("300x300")

    user_list_var = tk.StringVar(value=[])
    user_listbox = tk.Listbox(root, listvariable=user_list_var, height=15)
    user_listbox.pack(fill='both', expand=True)

    ttk.Button(root, text="Delete User", command=delete_selected_user).pack(pady=10)

    refresh_user_list()
    root.mainloop()

if __name__ == '__main__':
    delete_user_gui()
