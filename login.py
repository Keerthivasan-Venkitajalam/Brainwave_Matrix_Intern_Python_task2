import tkinter as tk
from tkinter import ttk, messagebox
from authentication import create_user, authenticate_user

def show_login_screen(main_app_callback):
    login_window = tk.Tk()
    login_window.title("Login")
    login_window.geometry("300x200")

    ttk.Label(login_window, text="Username:").grid(row=0, column=0, padx=10, pady=10, sticky="e")
    username_var = tk.StringVar()
    username_entry = ttk.Entry(login_window, textvariable=username_var)
    username_entry.grid(row=0, column=1, padx=10, pady=10, sticky="ew")

    ttk.Label(login_window, text="Password:").grid(row=1, column=0, padx=10, pady=10, sticky="e")
    password_var = tk.StringVar()
    password_entry = ttk.Entry(login_window, textvariable=password_var, show='*')
    password_entry.grid(row=1, column=1, padx=10, pady=10, sticky="ew")

    def login():
        username = username_var.get()
        password = password_var.get()
        if authenticate_user(username, password):
            messagebox.showinfo("Login", "Login successful")
            login_window.destroy()
            main_app_callback()
        else:
            messagebox.showerror("Login", "Invalid username or password")

    def show_signup():
        login_window.destroy()
        show_signup_screen(main_app_callback)

    ttk.Button(login_window, text="Login", command=login).grid(row=2, columnspan=2, pady=10)
    ttk.Button(login_window, text="Sign Up", command=show_signup).grid(row=3, columnspan=2, pady=10)

    login_window.mainloop()

def show_signup_screen(main_app_callback):
    signup_window = tk.Tk()
    signup_window.title("Sign Up")
    signup_window.geometry("300x200")

    ttk.Label(signup_window, text="Username:").grid(row=0, column=0, padx=10, pady=10, sticky="e")
    signup_username_var = tk.StringVar()
    signup_username_entry = ttk.Entry(signup_window, textvariable=signup_username_var)
    signup_username_entry.grid(row=0, column=1, padx=10, pady=10, sticky="ew")

    ttk.Label(signup_window, text="Password:").grid(row=1, column=0, padx=10, pady=10, sticky="e")
    signup_password_var = tk.StringVar()
    signup_password_entry = ttk.Entry(signup_window, textvariable=signup_password_var, show='*')
    signup_password_entry.grid(row=1, column=1, padx=10, pady=10, sticky="ew")

    def signup():
        username = signup_username_var.get()
        password = signup_password_var.get()
        success, message = create_user(username, password)
        if success:
            messagebox.showinfo("Sign Up", message)
            signup_window.destroy()
            show_login_screen(main_app_callback)
        else:
            messagebox.showerror("Sign Up", message)

    ttk.Button(signup_window, text="Sign Up", command=signup).grid(row=2, columnspan=2, pady=10)

    signup_window.mainloop()
