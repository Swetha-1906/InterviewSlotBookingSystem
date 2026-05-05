import tkinter as tk
from tkinter import messagebox
import threading
import time

balance = 1000
lock = threading.Lock()  

def transaction(action, amount):
    global balance

    log(f"{action} request started for Rs.{amount}")

    with lock:
        log(f"{action} entered critical section")

        current = balance
        time.sleep(2)   

        if action == "Deposit":
            balance = current + amount
            log(f"Deposited Rs.{amount}")

        elif action == "Withdraw":
            if current >= amount:
                balance = current - amount
                log(f"Withdrawn Rs.{amount}")
            else:
                log("Insufficient Balance")

        update_balance()
        log(f"{action} exited critical section\n")


def start_transaction(action):
    try:
        amount = int(amount_entry.get())
        t = threading.Thread(target=transaction, args=(action, amount))
        t.start()
    except ValueError:
        messagebox.showerror("Error", "Enter valid amount")

def update_balance():
    balance_label.config(text=f"Current Balance: Rs.{balance}")


def log(msg):
    output_box.insert(tk.END, msg + "\n")
    output_box.see(tk.END)


root = tk.Tk()
root.title("Bank Account Transaction Synchronization")
root.geometry("500x500")
root.config(bg="#cfe8ff")   

title = tk.Label(
    root,
    text="Bank Account Transaction",
    font=("Arial", 16, "bold"),
    bg="#cfe8ff",
    fg="black"
)
title.pack(pady=12)

balance_label = tk.Label(
    root,
    text=f"Current Balance: Rs.{balance}",
    font=("Arial", 13),
    bg="#cfe8ff",
    fg="black"
)
balance_label.pack(pady=8)

frame = tk.Frame(root, bg="#cfe8ff")
frame.pack(pady=8)

tk.Label(
    frame,
    text="Enter Amount:",
    font=("Arial", 11),
    bg="#cfe8ff",
    fg="black"
).grid(row=0, column=0, padx=8)

amount_entry = tk.Entry(frame, font=("Arial", 11), width=15)
amount_entry.grid(row=0, column=1, padx=8)

btn_frame = tk.Frame(root, bg="#cfe8ff")
btn_frame.pack(pady=12)

deposit_btn = tk.Button(
    btn_frame,
    text="Deposit",
    font=("Arial", 11),
    bg="white",
    fg="black",
    width=12,
    command=lambda: start_transaction("Deposit")
)
deposit_btn.grid(row=0, column=0, padx=8)

withdraw_btn = tk.Button(
    btn_frame,
    text="Withdraw",
    font=("Arial", 11),
    bg="white",
    fg="black",
    width=12,
    command=lambda: start_transaction("Withdraw")
)
withdraw_btn.grid(row=0, column=1, padx=8)

tk.Label(
    root,
    text="Transaction Log",
    font=("Arial", 11, "bold"),
    bg="#cfe8ff",
    fg="black"
).pack(pady=6)

output_box = tk.Text(root, width=55, height=15, font=("Arial", 10))
output_box.pack(pady=8)

root.mainloop()
