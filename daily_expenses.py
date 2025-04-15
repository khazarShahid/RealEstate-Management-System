import tkinter as tk
from tkinter import ttk, messagebox
import sqlite3

class DailyExpenses:
    def __init__(self, root):
        self.root = root
        self.root.title("Daily Expenses")
        self.root.geometry("1000x600")

        # DB Connection
        self.conn = sqlite3.connect("real_estate.db")
        self.cursor = self.conn.cursor()
        self.create_table()

        self.selected_id = None  # to track the selected record ID

        # ========== Form Area ==========
        form_frame = tk.LabelFrame(root, text="Add / Update Daily Expense", padx=10, pady=10)
        form_frame.pack(fill="x", padx=10, pady=10)

        tk.Label(form_frame, text="Project Name:").grid(row=0, column=0, sticky="w")
        self.project_dropdown = ttk.Combobox(form_frame, width=30)
        self.project_dropdown.grid(row=0, column=1, padx=10, pady=5)
        self.load_projects()

        tk.Label(form_frame, text="Expense Type:").grid(row=1, column=0, sticky="w")
        self.expense_type = tk.Entry(form_frame, width=32)
        self.expense_type.grid(row=1, column=1, padx=10, pady=5)

        tk.Label(form_frame, text="Amount Paid:").grid(row=2, column=0, sticky="w")
        self.amount = tk.Entry(form_frame, width=32)
        self.amount.grid(row=2, column=1, padx=10, pady=5)

        tk.Label(form_frame, text="Payment Date (YYYY-MM-DD):").grid(row=3, column=0, sticky="w")
        self.payment_date = tk.Entry(form_frame, width=32)
        self.payment_date.grid(row=3, column=1, padx=10, pady=5)

        tk.Label(form_frame, text="Vendor/Supplier Name:").grid(row=4, column=0, sticky="w")
        self.vendor_name = tk.Entry(form_frame, width=32)
        self.vendor_name.grid(row=4, column=1, padx=10, pady=5)

        tk.Label(form_frame, text="Notes:").grid(row=5, column=0, sticky="w")
        self.notes = tk.Entry(form_frame, width=32)
        self.notes.grid(row=5, column=1, padx=10, pady=5)

        # Buttons
        tk.Button(form_frame, text="Save Expense", command=self.save_data).grid(row=6, column=0, pady=10)
        tk.Button(form_frame, text="View All", command=self.view_all).grid(row=6, column=1, pady=10)
        tk.Button(form_frame, text="Update", command=self.update_data).grid(row=6, column=2, pady=10)
        tk.Button(form_frame, text="Delete", command=self.delete_data).grid(row=6, column=3, pady=10)

        # ========== Search and Table ==========
        search_frame = tk.LabelFrame(root, text="Search Expenses by Date", padx=10, pady=10)
        search_frame.pack(fill="x", padx=10, pady=5)

        tk.Label(search_frame, text="Search Date (YYYY-MM-DD):").pack(side="left")
        self.search_date = tk.Entry(search_frame, width=30)
        self.search_date.pack(side="left", padx=10)
        tk.Button(search_frame, text="Search", command=self.search_by_date).pack(side="left")

        # Treeview Table
        self.tree = ttk.Treeview(root, columns=("ID", "Project", "Type", "Amount", "Date", "Vendor", "Notes"), show="headings")
        self.tree.pack(fill="both", expand=True, padx=10, pady=10)

        # Set column headings
        self.tree.heading("ID", text="ID")
        self.tree.column("ID", width=40)
        for col in ("Project", "Type", "Amount", "Date", "Vendor", "Notes"):
            self.tree.heading(col, text=col)
            self.tree.column(col, width=150)

        self.tree.bind("<Double-1>", self.on_row_select)  # bind double click

    def create_table(self):
        self.cursor.execute("""
            CREATE TABLE IF NOT EXISTS daily_expenses (
                expense_id INTEGER PRIMARY KEY AUTOINCREMENT,
                project_name TEXT NOT NULL,
                expense_type TEXT NOT NULL,
                amount_paid REAL NOT NULL,
                payment_date TEXT NOT NULL,
                vendor_name TEXT,
                notes TEXT
            )
        """)
        self.conn.commit()

    def load_projects(self):
        self.cursor.execute("SELECT land_name FROM land_acquisition")
        projects = self.cursor.fetchall()
        self.project_dropdown["values"] = [p[0] for p in projects]

    def save_data(self):
        try:
            project = self.project_dropdown.get()
            if not project:
                raise ValueError("Project name is required.")
            data = (
                project,
                self.expense_type.get(),
                float(self.amount.get()),
                self.payment_date.get(),
                self.vendor_name.get(),
                self.notes.get()
            )
            self.cursor.execute("""
                INSERT INTO daily_expenses (project_name, expense_type, amount_paid, payment_date, vendor_name, notes)
                VALUES (?, ?, ?, ?, ?, ?)
            """, data)
            self.conn.commit()
            messagebox.showinfo("Success", "Expense saved successfully.")
            self.clear_fields()
            self.view_all()
        except Exception as e:
            messagebox.showerror("Error", str(e))

    def view_all(self):
        self.tree.delete(*self.tree.get_children())
        self.cursor.execute("""
            SELECT expense_id, project_name, expense_type, amount_paid, payment_date, vendor_name, notes FROM daily_expenses
        """)
        for row in self.cursor.fetchall():
            self.tree.insert("", "end", values=row)

    def search_by_date(self):
        self.tree.delete(*self.tree.get_children())
        search_date = self.search_date.get()
        self.cursor.execute("""
            SELECT expense_id, project_name, expense_type, amount_paid, payment_date, vendor_name, notes
            FROM daily_expenses WHERE payment_date = ?
        """, (search_date,))
        for row in self.cursor.fetchall():
            self.tree.insert("", "end", values=row)

    def on_row_select(self, event):
        selected = self.tree.focus()
        values = self.tree.item(selected, 'values')
        if values:
            self.selected_id = values[0]
            self.project_dropdown.set(values[1])
            self.expense_type.delete(0, tk.END)
            self.expense_type.insert(0, values[2])
            self.amount.delete(0, tk.END)
            self.amount.insert(0, values[3])
            self.payment_date.delete(0, tk.END)
            self.payment_date.insert(0, values[4])
            self.vendor_name.delete(0, tk.END)
            self.vendor_name.insert(0, values[5])
            self.notes.delete(0, tk.END)
            self.notes.insert(0, values[6])

    def update_data(self):
        if self.selected_id:
            data = (
                self.project_dropdown.get(),
                self.expense_type.get(),
                float(self.amount.get()),
                self.payment_date.get(),
                self.vendor_name.get(),
                self.notes.get(),
                self.selected_id
            )
            self.cursor.execute("""
                UPDATE daily_expenses
                SET project_name = ?, expense_type = ?, amount_paid = ?, payment_date = ?, vendor_name = ?, notes = ?
                WHERE expense_id = ?
            """, data)
            self.conn.commit()
            messagebox.showinfo("Updated", "Record updated successfully.")
            self.clear_fields()
            self.view_all()
            self.selected_id = None
        else:
            messagebox.showwarning("Warning", "Please select a record to update.")

    def delete_data(self):
        if self.selected_id:
            confirm = messagebox.askyesno("Confirm", "Are you sure you want to delete this record?")
            if confirm:
                self.cursor.execute("DELETE FROM daily_expenses WHERE expense_id = ?", (self.selected_id,))
                self.conn.commit()
                messagebox.showinfo("Deleted", "Record deleted successfully.")
                self.clear_fields()
                self.view_all()
                self.selected_id = None
        else:
            messagebox.showwarning("Warning", "Please select a record to delete.")

    def clear_fields(self):
        self.project_dropdown.set("")
        self.expense_type.delete(0, tk.END)
        self.amount.delete(0, tk.END)
        self.payment_date.delete(0, tk.END)
        self.vendor_name.delete(0, tk.END)
        self.notes.delete(0, tk.END)
        self.selected_id = None


# Run app
if __name__ == "__main__":
    root = tk.Tk()
    app = DailyExpenses(root)
    root.mainloop()
