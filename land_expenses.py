import tkinter as tk
from tkinter import ttk, messagebox
import sqlite3

class LandExpenses:
    def __init__(self, root):
        self.root = root
        self.root.title("Land-Related Expenses")
        self.root.geometry("850x700")

        # Database Connection
        self.conn = sqlite3.connect("real_estate.db")
        self.cursor = self.conn.cursor()
        self.create_table()

        # Dictionary to hold project name -> id mapping
        self.project_map = {}

        # --- Form Inputs ---
        label_opts = {'padx': 10, 'pady': 5, 'sticky': 'w'}
        entry_opts = {'padx': 10, 'pady': 5}

        tk.Label(root, text="Select Land Project:").grid(row=0, column=0, **label_opts)
        self.land_id = ttk.Combobox(root, width=30, state="readonly")
        self.land_id.grid(row=0, column=1, **entry_opts)
        self.load_land_projects()

        tk.Label(root, text="Expense Type:").grid(row=1, column=0, **label_opts)
        self.expense_type = tk.Entry(root, width=32)
        self.expense_type.grid(row=1, column=1, **entry_opts)

        tk.Label(root, text="Payment Mode:").grid(row=2, column=0, **label_opts)
        self.payment_mode = ttk.Combobox(root, values=["Cash", "RTGS", "UPI", "Bank Transfer"], width=30, state="readonly")
        self.payment_mode.grid(row=2, column=1, **entry_opts)

        tk.Label(root, text="Amount Paid:").grid(row=3, column=0, **label_opts)
        self.amount_paid = tk.Entry(root, width=32)
        self.amount_paid.grid(row=3, column=1, **entry_opts)

        tk.Label(root, text="Payment Date:").grid(row=4, column=0, **label_opts)
        self.payment_date = tk.Entry(root, width=32)
        self.payment_date.grid(row=4, column=1, **entry_opts)

        tk.Label(root, text="Remaining Balance:").grid(row=5, column=0, **label_opts)
        self.remaining_balance = tk.Entry(root, width=32)
        self.remaining_balance.grid(row=5, column=1, **entry_opts)

        tk.Label(root, text="Notes:").grid(row=6, column=0, **label_opts)
        self.notes = tk.Entry(root, width=32)
        self.notes.grid(row=6, column=1, **entry_opts)

        # --- Buttons ---
        self.selected_expense_id = None
        btn_frame = tk.Frame(root)
        btn_frame.grid(row=7, column=0, columnspan=2, pady=15)

        tk.Button(btn_frame, text="Save Expense", width=15, command=self.save_data).grid(row=0, column=0, padx=10)
        tk.Button(btn_frame, text="View Expenses", width=15, command=self.view_details).grid(row=0, column=1, padx=10)
        tk.Button(btn_frame, text="Update", width=15, command=self.update_data).grid(row=0, column=2, padx=10)
        tk.Button(btn_frame, text="Delete", width=15, command=self.delete_data).grid(row=0, column=3, padx=10)

        # --- Table ---
        columns = ("ID", "Land ID", "Expense Type", "Amount", "Payment Mode", "Date", "Balance", "Notes")
        self.tree = ttk.Treeview(root, columns=columns, show="headings")
        self.tree.grid(row=8, column=0, columnspan=2, padx=10, pady=20, sticky="nsew")

        for col in columns:
            self.tree.heading(col, text=col)
            self.tree.column(col, width=100)

        self.tree.bind("<ButtonRelease-1>", self.get_selected_row)

        root.grid_rowconfigure(8, weight=1)
        root.grid_columnconfigure(1, weight=1)

    def create_table(self):
        self.cursor.execute("""
            CREATE TABLE IF NOT EXISTS land_expenses (
                expense_id INTEGER PRIMARY KEY AUTOINCREMENT,
                land_id INTEGER NOT NULL,
                expense_type TEXT NOT NULL,
                payment_mode TEXT NOT NULL,
                amount_paid REAL NOT NULL,
                payment_date TEXT NOT NULL,
                remaining_balance REAL NOT NULL,
                notes TEXT,
                FOREIGN KEY (land_id) REFERENCES land_acquisition(land_id) ON DELETE CASCADE
            )
        """)
        self.conn.commit()

    def load_land_projects(self):
        try:
            self.cursor.execute("SELECT land_id, land_name FROM land_acquisition")
            projects = self.cursor.fetchall()
            self.project_map = {p[1]: p[0] for p in projects}  # name -> id
            self.land_id["values"] = list(self.project_map.keys())
        except Exception as e:
            messagebox.showerror("Database Error", f"Error loading projects:\n{e}")

    def save_data(self):
        selected_project = self.land_id.get()
        if not selected_project:
            messagebox.showerror("Input Error", "Please select a land project.")
            return

        try:
            land_id = self.project_map[selected_project]
            data = (
                land_id,
                self.expense_type.get(),
                self.payment_mode.get(),
                float(self.amount_paid.get()),
                self.payment_date.get(),
                float(self.remaining_balance.get()),
                self.notes.get()
            )
            self.cursor.execute("""
                INSERT INTO land_expenses (land_id, expense_type, payment_mode, amount_paid, payment_date, remaining_balance, notes)
                VALUES (?, ?, ?, ?, ?, ?, ?)
            """, data)
            self.conn.commit()
            messagebox.showinfo("Success", "Expense added successfully!")
            self.clear_fields()
            self.view_details()
        except ValueError:
            messagebox.showerror("Input Error", "Please enter valid numeric values.")
        except Exception as e:
            messagebox.showerror("Database Error", f"Error saving data:\n{e}")

    def view_details(self):
        self.tree.delete(*self.tree.get_children())
        selected_project = self.land_id.get()
        if not selected_project:
            messagebox.showerror("Input Error", "Please select a land project to view expenses.")
            return
        try:
            land_id = self.project_map[selected_project]
            self.cursor.execute("""
                SELECT expense_id, land_id, expense_type, amount_paid, payment_mode, payment_date, remaining_balance, notes 
                FROM land_expenses
                WHERE land_id = ?
            """, (land_id,))
            rows = self.cursor.fetchall()
            for row in rows:
                self.tree.insert("", "end", values=row)
        except Exception as e:
            messagebox.showerror("Database Error", f"Error loading data:\n{e}")

    def get_selected_row(self, event):
        selected = self.tree.focus()
        if not selected:
            return
        values = self.tree.item(selected, "values")
        self.selected_expense_id = values[0]

        # Reverse lookup project name from ID
        land_id_value = int(values[1])
        project_name = next((name for name, pid in self.project_map.items() if pid == land_id_value), "")
        self.land_id.set(project_name)

        self.expense_type.delete(0, tk.END)
        self.expense_type.insert(0, values[2])
        self.amount_paid.delete(0, tk.END)
        self.amount_paid.insert(0, values[3])
        self.payment_mode.set(values[4])
        self.payment_date.delete(0, tk.END)
        self.payment_date.insert(0, values[5])
        self.remaining_balance.delete(0, tk.END)
        self.remaining_balance.insert(0, values[6])
        self.notes.delete(0, tk.END)
        self.notes.insert(0, values[7])

    def update_data(self):
        if not self.selected_expense_id:
            messagebox.showerror("Error", "Please select a record to update.")
            return
        try:
            land_id = self.project_map[self.land_id.get()]
            self.cursor.execute("""
                UPDATE land_expenses
                SET land_id=?, expense_type=?, payment_mode=?, amount_paid=?, payment_date=?, remaining_balance=?, notes=?
                WHERE expense_id=?
            """, (
                land_id,
                self.expense_type.get(),
                self.payment_mode.get(),
                float(self.amount_paid.get()),
                self.payment_date.get(),
                float(self.remaining_balance.get()),
                self.notes.get(),
                self.selected_expense_id
            ))
            self.conn.commit()
            messagebox.showinfo("Success", "Record updated successfully!")
            self.clear_fields()
            self.view_details()
        except Exception as e:
            messagebox.showerror("Update Error", f"Could not update record:\n{e}")

    def delete_data(self):
        if not self.selected_expense_id:
            messagebox.showerror("Error", "Please select a record to delete.")
            return
        try:
            self.cursor.execute("DELETE FROM land_expenses WHERE expense_id=?", (self.selected_expense_id,))
            self.conn.commit()
            messagebox.showinfo("Deleted", "Record deleted successfully!")
            self.clear_fields()
            self.view_details()
        except Exception as e:
            messagebox.showerror("Delete Error", f"Could not delete record:\n{e}")

    def clear_fields(self):
        self.selected_expense_id = None
        self.expense_type.delete(0, tk.END)
        self.amount_paid.delete(0, tk.END)
        self.payment_date.delete(0, tk.END)
        self.remaining_balance.delete(0, tk.END)
        self.notes.delete(0, tk.END)
        self.payment_mode.set("")
        self.land_id.set("")

# Run the App
if __name__ == "__main__":
    root = tk.Tk()
    app = LandExpenses(root)
    root.mainloop()
