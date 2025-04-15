import tkinter as tk
from tkinter import ttk, messagebox
import sqlite3

class SalaryManagement:
    def __init__(self, root):
        self.root = root
        self.root.title("Employee Salary Management")
        self.root.geometry("1150x650")

        # Connect to database
        self.conn = sqlite3.connect("real_estate.db")
        self.cursor = self.conn.cursor()
        self.create_table()

        # ====== Form Frame ======
        form_frame = tk.LabelFrame(root, text="Add / Update Salary Details", padx=10, pady=10)
        form_frame.pack(fill="x", padx=10, pady=10)

        # Variables
        self.selected_id = None

        # Form Inputs
        tk.Label(form_frame, text="Employee Name:").grid(row=0, column=0, sticky="w")
        self.employee_name = tk.Entry(form_frame, width=30)
        self.employee_name.grid(row=0, column=1, padx=10, pady=5)

        tk.Label(form_frame, text="Total Salary:").grid(row=1, column=0, sticky="w")
        self.salary = tk.Entry(form_frame, width=30)
        self.salary.grid(row=1, column=1, padx=10, pady=5)

        tk.Label(form_frame, text="Payment Date (YYYY-MM-DD):").grid(row=2, column=0, sticky="w")
        self.payment_date = tk.Entry(form_frame, width=30)
        self.payment_date.grid(row=2, column=1, padx=10, pady=5)

        tk.Label(form_frame, text="Payment Status:").grid(row=3, column=0, sticky="w")
        self.status = ttk.Combobox(form_frame, values=["Paid", "Unpaid"], width=28)
        self.status.grid(row=3, column=1, padx=10, pady=5)

        tk.Label(form_frame, text="Next Payment Date (YYYY-MM-DD):").grid(row=4, column=0, sticky="w")
        self.next_payment = tk.Entry(form_frame, width=30)
        self.next_payment.grid(row=4, column=1, padx=10, pady=5)

        tk.Label(form_frame, text="Additional Costs:").grid(row=5, column=0, sticky="w")
        self.additional_cost = tk.Entry(form_frame, width=30)
        self.additional_cost.grid(row=5, column=1, padx=10, pady=5)

        tk.Label(form_frame, text="Notes:").grid(row=6, column=0, sticky="w")
        self.notes = tk.Entry(form_frame, width=30)
        self.notes.grid(row=6, column=1, padx=10, pady=5)

        # Buttons
        tk.Button(form_frame, text="Save Salary", command=self.save_salary).grid(row=7, column=0, pady=10)
        tk.Button(form_frame, text="Update Selected", command=self.update_salary).grid(row=7, column=1, pady=10)
        tk.Button(form_frame, text="Delete Selected", command=self.delete_salary).grid(row=7, column=2, pady=10)

        # ====== Search Section ======
        search_frame = tk.LabelFrame(root, text="Search Salaries by Date or Month", padx=10, pady=10)
        search_frame.pack(fill="x", padx=10, pady=5)

        tk.Label(search_frame, text="Search Date or Month (YYYY-MM or YYYY-MM-DD):").pack(side="left")
        self.search_date = tk.Entry(search_frame, width=30)
        self.search_date.pack(side="left", padx=10)
        tk.Button(search_frame, text="Search", command=self.search_salary).pack(side="left")
        tk.Button(search_frame, text="Show All", command=self.view_all).pack(side="left", padx=5)

        # ====== Table ======
        self.tree = ttk.Treeview(root, columns=("ID", "Name", "Salary", "Pay Date", "Status", "Next Pay", "Extra", "Notes"), show="headings")
        self.tree.pack(fill="both", expand=True, padx=10, pady=10)

        for col in self.tree["columns"]:
            self.tree.heading(col, text=col)
            self.tree.column(col, width=130)

        self.tree.bind("<ButtonRelease-1>", self.get_selected_row)

        # Load data
        self.view_all()

    def create_table(self):
        self.cursor.execute("""
            CREATE TABLE IF NOT EXISTS employee_salary (
                employee_id INTEGER PRIMARY KEY AUTOINCREMENT,
                employee_name TEXT,
                total_salary REAL,
                payment_date TEXT,
                payment_status TEXT,
                next_payment_date TEXT,
                additional_costs REAL,
                notes TEXT
            )
        """)
        self.conn.commit()

    def save_salary(self):
        try:
            data = (
                self.employee_name.get(),
                float(self.salary.get()),
                self.payment_date.get(),
                self.status.get(),
                self.next_payment.get(),
                float(self.additional_cost.get() or 0),
                self.notes.get()
            )

            self.cursor.execute("""
                INSERT INTO employee_salary (
                    employee_name, total_salary, payment_date, payment_status, 
                    next_payment_date, additional_costs, notes
                ) VALUES (?, ?, ?, ?, ?, ?, ?)
            """, data)
            self.conn.commit()
            messagebox.showinfo("Success", "Salary record saved.")
            self.clear_fields()
            self.view_all()

        except Exception as e:
            messagebox.showerror("Error", f"Failed to save salary: {e}")

    def view_all(self):
        self.tree.delete(*self.tree.get_children())
        self.cursor.execute("SELECT * FROM employee_salary")
        for row in self.cursor.fetchall():
            self.tree.insert("", "end", values=row)

    def search_salary(self):
        self.tree.delete(*self.tree.get_children())
        keyword = self.search_date.get()
        self.cursor.execute("""
            SELECT * FROM employee_salary WHERE payment_date LIKE ?
        """, (f"{keyword}%",))
        for row in self.cursor.fetchall():
            self.tree.insert("", "end", values=row)

    def get_selected_row(self, event):
        selected = self.tree.focus()
        if selected:
            values = self.tree.item(selected, "values")
            self.selected_id = values[0]
            self.employee_name.delete(0, tk.END)
            self.employee_name.insert(0, values[1])

            self.salary.delete(0, tk.END)
            self.salary.insert(0, values[2])

            self.payment_date.delete(0, tk.END)
            self.payment_date.insert(0, values[3])

            self.status.set(values[4])

            self.next_payment.delete(0, tk.END)
            self.next_payment.insert(0, values[5])

            self.additional_cost.delete(0, tk.END)
            self.additional_cost.insert(0, values[6])

            self.notes.delete(0, tk.END)
            self.notes.insert(0, values[7])

    def update_salary(self):
        if not self.selected_id:
            messagebox.showwarning("Warning", "Please select a record to update.")
            return

        try:
            data = (
                self.employee_name.get(),
                float(self.salary.get()),
                self.payment_date.get(),
                self.status.get(),
                self.next_payment.get(),
                float(self.additional_cost.get() or 0),
                self.notes.get(),
                self.selected_id
            )
            self.cursor.execute("""
                UPDATE employee_salary SET 
                    employee_name = ?, total_salary = ?, payment_date = ?, 
                    payment_status = ?, next_payment_date = ?, 
                    additional_costs = ?, notes = ?
                WHERE employee_id = ?
            """, data)
            self.conn.commit()
            messagebox.showinfo("Success", "Salary record updated.")
            self.clear_fields()
            self.view_all()
        except Exception as e:
            messagebox.showerror("Error", f"Failed to update: {e}")

    def delete_salary(self):
        if not self.selected_id:
            messagebox.showwarning("Warning", "Please select a record to delete.")
            return

        confirm = messagebox.askyesno("Confirm Delete", "Are you sure you want to delete this record?")
        if confirm:
            try:
                self.cursor.execute("DELETE FROM employee_salary WHERE employee_id=?", (self.selected_id,))
                self.conn.commit()
                messagebox.showinfo("Deleted", "Salary record deleted.")
                self.clear_fields()
                self.view_all()
            except Exception as e:
                messagebox.showerror("Error", f"Failed to delete: {e}")

    def clear_fields(self):
        self.selected_id = None
        self.employee_name.delete(0, tk.END)
        self.salary.delete(0, tk.END)
        self.payment_date.delete(0, tk.END)
        self.status.set("")
        self.next_payment.delete(0, tk.END)
        self.additional_cost.delete(0, tk.END)
        self.notes.delete(0, tk.END)

# Run App
if __name__ == "__main__":
    root = tk.Tk()
    app = SalaryManagement(root)
    root.mainloop()
