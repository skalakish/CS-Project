import tkinter as tk
from tkinter import ttk
from tkinter import messagebox
import sqlite3
import hashlib
import random


def hash_password(password):
    return hashlib.sha256(password.encode()).hexdigest()


def verify_login(username, password):
    hashed_password = hash_password(password)
    cursor.execute("SELECT * FROM users WHERE username = ? AND password = ?", (username, hashed_password))
    return cursor.fetchone() is not None


def register(username, password):
    hashed_password = hash_password(password)
    cursor.execute("INSERT INTO users (username, password) VALUES (?, ?)", (username, hashed_password))
    conn.commit()


def login():
    username = entry1.get()
    password = entry2.get()
    if verify_login(username, password):
        messagebox.showinfo("Login Successful", "Welcome back, {}!".format(username))
        root.withdraw()
        show_loading_screen()
    else:
        messagebox.showerror("Login Failed", "Invalid username or password")


def register_account():
    username = entry1.get()
    password = entry2.get()
    if username and password:
        register(username, password)
        messagebox.showinfo("Registration Successful", "Account registered successfully!")
    else:
        messagebox.showerror("Registration Failed", "Please enter both username and password")


def show_loading_screen():
    loading_window = tk.Toplevel(root)
    loading_window.geometry("300x150")
    loading_window.title("Loading...")
    loading_window.resizable(False, False)

    label = tk.Label(loading_window, text="Loading, please wait...", font=("Roboto", 12))
    label.pack(pady=20)

    progressbar = ttk.Progressbar(loading_window, mode="indeterminate")
    progressbar.pack(pady=10)
    progressbar.start()

    loading_window.after(10000, lambda: transition_to_main(loading_window))


def transition_to_main(loading_window):
    loading_window.destroy()
    open_main_window()


def open_main_window():
    main_window = tk.Toplevel(root)
    main_window.geometry("800x600")
    main_window.title("Main Window")
    main_window.configure(bg="#263238")

    label = tk.Label(main_window, text="Crypto Game", font=("Roboto", 24), fg="white", bg="#263238")
    label.pack(pady=20)

    bitcoin_button = ttk.Button(main_window, text="BITCOIN", command=lambda: make_choice("Bitcoin"))
    bitcoin_button.place(x=20, y=20)

    ethereum_button = ttk.Button(main_window, text="ETHEREUM", command=lambda: make_choice("Ethereum"))
    ethereum_button.place(x=20, y=60)

    litecoin_button = ttk.Button(main_window, text="LITECOIN", command=lambda: make_choice("Litecoin"))
    litecoin_button.place(x=20, y=100)

    flip_coin_button = ttk.Button(main_window, text="FLIP A COIN", command=flip_coin)
    flip_coin_button.place(x=700, y=550)

    end_game_button = ttk.Button(main_window, text="End Game", command=lambda: end_game(main_window))
    end_game_button.place(relx=0.5, rely=0.9, anchor="center")


# DEF GRAPH():
# DEF BALANCE():
# etc


def make_choice(choice):
    messagebox.showinfo("Choice", f"You chose {choice}")


def flip_coin():
    result = random.choice(["Heads", "Tails"])
    if result == "Heads":
        messagebox.showinfo("Coin Flip", "Heads! Sell!")
    else:
        messagebox.showinfo("Coin Flip", "Tails! Buy!")


def end_game(main_window):
    main_window.destroy()
    show_users_table()


def show_users_table():
    users_table_window = tk.Toplevel(root)
    users_table_window.geometry("800x400")
    users_table_window.title("Users Table")

    table_label = tk.Label(users_table_window, text="Top Users Table", font=("Roboto", 16))
    table_label.pack(pady=10)

    users_table = ttk.Treeview(users_table_window, columns=("ID", "Username", "All time profit", "Best profit"), show="headings")
    users_table.heading("ID", text="ID")
    users_table.heading("Username", text="Username")
    users_table.heading("All time profit", text="All time profit")
    users_table.heading("Best profit", text="Best profit")
    users_table.pack(pady=10)

    for i in range(1, 6):
        users_table.insert("", "end", values=(i, f"User{i}", i*100, i*10))


conn = sqlite3.connect('user_credentials.db')
cursor = conn.cursor()


cursor.execute('''CREATE TABLE IF NOT EXISTS users
                  (id INTEGER PRIMARY KEY, username TEXT, password TEXT)''')
conn.commit()


root = tk.Tk()
root.geometry("500x350")
root.title("Login System")
root.configure(bg="#263238")


frame = tk.Frame(root, bg="#263238")
frame.pack(pady=20, padx=60)


label = tk.Label(frame, text="Login System", font=("Roboto", 24), fg="white", bg="#263238")
label.pack(pady=12)


entry1 = ttk.Entry(frame)
entry1.pack(pady=12)
entry1.config(font=("Roboto", 12), justify="center")

entry2 = ttk.Entry(frame, show="*")
entry2.pack(pady=12)
entry2.config(font=("Roboto", 12), justify="center")


login_button = ttk.Button(frame, text="Login", command=login)
login_button.pack(pady=6)

register_button = ttk.Button(frame, text="Register", command=register_account)
register_button.pack(pady=6)


root.mainloop()
