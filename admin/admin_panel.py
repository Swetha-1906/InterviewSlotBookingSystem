import sqlite3
import tkinter as tk
from tkinter import messagebox, ttk, filedialog
from tkcalendar import DateEntry
from datetime import date
import csv

# ---------- DB PATH ----------
db_path = r"D:\6th sem\PP Project\InterviewSlotBookingSystem\database\interviews.db"

# ---------- DB CONNECTION ----------
def connect_db():
    return sqlite3.connect(db_path)

# ---------- VALIDATION ----------
def is_valid_email(email):
    return "@" in email and "." in email

# ---------- INSERT ----------
def insert_user():
    name = name_entry.get().strip()
    email = email_entry.get().strip()
    selected_date = date_entry.get()
    slot = slot_var.get().strip()

    if not name or not email or not selected_date or not slot:
        messagebox.showerror("Error", "All fields are required")
        return

    if not is_valid_email(email):
        messagebox.showerror("Error", "Invalid Email Format")
        return

    try:
        conn = connect_db()
        cursor = conn.cursor()
        conn.execute("BEGIN")

        cursor.execute("SELECT * FROM appointments WHERE date=? AND slot=?", (selected_date, slot))
        if cursor.fetchone():
            messagebox.showerror("Error", "Slot already booked for this date")
            conn.rollback()
            conn.close()
            return

        cursor.execute(
            "INSERT INTO appointments (name, email, date, slot) VALUES (?, ?, ?, ?)",
            (name, email, selected_date, slot)
        )

        conn.commit()
        messagebox.showinfo("Success", "Record Inserted Successfully")
        clear_fields()
        load_data()

    except Exception as e:
        conn.rollback()
        messagebox.showerror("Error", f"Insert Failed\n{e}")
    finally:
        conn.close()

# ---------- UPDATE ----------
def update_user():
    selected = tree.focus()
    if not selected:
        messagebox.showerror("Error", "Select a record first")
        return

    user_id = tree.item(selected)["values"][0]

    name = name_entry.get().strip()
    email = email_entry.get().strip()
    selected_date = date_entry.get()
    slot = slot_var.get().strip()

    if not name or not email or not selected_date or not slot:
        messagebox.showerror("Error", "All fields are required")
        return

    if not is_valid_email(email):
        messagebox.showerror("Error", "Invalid Email Format")
        return

    try:
        conn = connect_db()
        cursor = conn.cursor()
        conn.execute("BEGIN")

        cursor.execute(
            "SELECT * FROM appointments WHERE date=? AND slot=? AND id!=?",
            (selected_date, slot, user_id)
        )
        if cursor.fetchone():
            messagebox.showerror("Error", "Slot already booked for this date")
            conn.rollback()
            conn.close()
            return

        cursor.execute("""
            UPDATE appointments
            SET name=?, email=?, date=?, slot=?
            WHERE id=?
        """, (name, email, selected_date, slot, user_id))

        conn.commit()
        messagebox.showinfo("Success", "Record Updated Successfully")
        clear_fields()
        load_data()

    except Exception as e:
        conn.rollback()
        messagebox.showerror("Error", f"Update Failed\n{e}")
    finally:
        conn.close()

# ---------- DELETE ----------
def delete_user():
    selected = tree.focus()
    if not selected:
        messagebox.showerror("Error", "Select a record first")
        return

    if not messagebox.askyesno("Confirm Delete", "Are you sure you want to delete this record?"):
        return

    user_id = tree.item(selected)["values"][0]

    try:
        conn = connect_db()
        cursor = conn.cursor()
        conn.execute("BEGIN")

        cursor.execute("DELETE FROM appointments WHERE id=?", (user_id,))
        conn.commit()

        messagebox.showinfo("Success", "Record Deleted Successfully")
        clear_fields()
        load_data()

    except Exception as e:
        conn.rollback()
        messagebox.showerror("Error", f"Delete Failed\n{e}")
    finally:
        conn.close()

# ---------- LOAD ----------
def load_data():
    for row in tree.get_children():
        tree.delete(row)

    conn = connect_db()
    cursor = conn.cursor()
    cursor.execute("SELECT * FROM appointments")
    rows = cursor.fetchall()
    conn.close()

    for i, row in enumerate(rows):
        tag = "evenrow" if i % 2 == 0 else "oddrow"
        tree.insert("", "end", values=row, tags=(tag,))

# ---------- OPEN ----------
def open_records():
    search_frame.pack(pady=10)
    table_frame.pack(pady=15)
    load_data()

# ---------- SEARCH ----------
def search_user():
    keyword = search_entry.get().strip()

    for row in tree.get_children():
        tree.delete(row)

    conn = connect_db()
    cursor = conn.cursor()
    cursor.execute("SELECT * FROM appointments WHERE name LIKE ?", ('%' + keyword + '%',))
    rows = cursor.fetchall()
    conn.close()

    for i, row in enumerate(rows):
        tag = "evenrow" if i % 2 == 0 else "oddrow"
        tree.insert("", "end", values=row, tags=(tag,))

# ---------- SAVE ----------
def save_data():
    file_path = filedialog.asksaveasfilename(defaultextension=".csv", filetypes=[("CSV File", "*.csv")])
    if not file_path:
        return

    conn = connect_db()
    cursor = conn.cursor()
    cursor.execute("SELECT * FROM appointments")
    rows = cursor.fetchall()
    conn.close()

    with open(file_path, "w", newline="") as file:
        writer = csv.writer(file)
        writer.writerow(["ID", "Name", "Email", "Date", "Slot"])
        writer.writerows(rows)

    messagebox.showinfo("Save", "Records exported successfully")

# ---------- SELECT ----------
def select_record(event):
    selected = tree.focus()
    if not selected:
        return

    values = tree.item(selected, "values")

    clear_fields()
    name_entry.insert(0, values[1])
    email_entry.insert(0, values[2])
    date_entry.set_date(values[3])
    slot_var.set(values[4])

# ---------- CLEAR ----------
def clear_fields():
    name_entry.delete(0, tk.END)
    email_entry.delete(0, tk.END)
    date_entry.set_date(date.today())
    slot_var.set("")

# ---------- EXIT ----------
def exit_app():
    if messagebox.askyesno("Exit", "Are you sure you want to exit?"):
        root.destroy()

# ---------- GUI ----------
root = tk.Tk()
root.title("Admin Panel - Interview Slot Booking")
root.geometry("950x650")
root.configure(bg="#e6f2ff")
root.resizable(False, False)

# ---------- TITLE ----------
tk.Label(root, text="Admin Panel", font=("Arial", 22, "bold"),
         bg="#e6f2ff", fg="#0077b6").pack(pady=15)

# ---------- MENU ----------
menu = tk.Menu(root)
root.config(menu=menu)

file_menu = tk.Menu(menu, tearoff=0)
menu.add_cascade(label="File", menu=file_menu)
file_menu.add_command(label="Open", command=open_records)
file_menu.add_command(label="Save", command=save_data)
file_menu.add_separator()
file_menu.add_command(label="Exit", command=exit_app)

# ---------- CENTER FORM CARD ----------
form_frame = tk.Frame(root, bg="white", bd=2, relief="groove")
form_frame.pack(pady=10)
form_frame.configure(width=420, height=260)
form_frame.pack_propagate(False)

tk.Label(form_frame, text="Name", bg="white").place(x=50, y=25)
name_entry = tk.Entry(form_frame, width=30)
name_entry.place(x=150, y=25)

tk.Label(form_frame, text="Email", bg="white").place(x=50, y=65)
email_entry = tk.Entry(form_frame, width=30)
email_entry.place(x=150, y=65)

tk.Label(form_frame, text="Date", bg="white").place(x=50, y=105)
date_entry = DateEntry(form_frame, width=27, background="#0077b6", foreground="white", date_pattern="yyyy-mm-dd")
date_entry.place(x=150, y=105)

tk.Label(form_frame, text="Slot", bg="white").place(x=50, y=145)
slot_var = tk.StringVar()
slot_dropdown = ttk.Combobox(form_frame, textvariable=slot_var,
                             values=["10:00-11:00", "11:00-12:00", "2:00-3:00"],
                             state="readonly", width=27)
slot_dropdown.place(x=150, y=145)

tk.Button(form_frame, text="Insert", bg="#0077b6", fg="white", width=10, command=insert_user).place(x=40, y=205)
tk.Button(form_frame, text="Update", bg="#0077b6", fg="white", width=10, command=update_user).place(x=155, y=205)
tk.Button(form_frame, text="Delete", bg="#0077b6", fg="white", width=10, command=delete_user).place(x=270, y=205)

# ---------- SEARCH ----------
search_frame = tk.Frame(root, bg="#e6f2ff")
tk.Label(search_frame, text="Search by Name:", bg="#e6f2ff").pack(side=tk.LEFT, padx=5)
search_entry = tk.Entry(search_frame, width=30)
search_entry.pack(side=tk.LEFT, padx=5)
tk.Button(search_frame, text="Search", bg="#0077b6", fg="white", command=search_user).pack(side=tk.LEFT)

# ---------- TABLE ----------
table_frame = tk.Frame(root)

tree = ttk.Treeview(table_frame, columns=("ID", "Name", "Email", "Date", "Slot"), show="headings", height=12)

for col in ("ID", "Name", "Email", "Date", "Slot"):
    tree.heading(col, text=col)
    tree.column(col, anchor="center", width=170 if col != "ID" else 60)

tree.tag_configure("evenrow", background="#f2f9ff")
tree.tag_configure("oddrow", background="white")

scrollbar = ttk.Scrollbar(table_frame, orient="vertical", command=tree.yview)
tree.configure(yscrollcommand=scrollbar.set)

tree.pack(side=tk.LEFT)
scrollbar.pack(side=tk.RIGHT, fill=tk.Y)

tree.bind("<<TreeviewSelect>>", select_record)

root.mainloop()