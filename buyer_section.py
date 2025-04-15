import tkinter as tk
from tkinter import ttk, messagebox
import sqlite3
import datetime

class BuyerSection:
    def __init__(self, root):
        self.root = root
        self.root.title("Buyer Section")
        self.root.geometry("1300x650")

        self.conn = sqlite3.connect("real_estate.db")
        self.cursor = self.conn.cursor()
        self.create_table()

        self.selected_id = None  # For edit/delete tracking

        # ==== Buyer Form ====
        form = tk.LabelFrame(root, text="Add Buyer Details", padx=10, pady=10)
        form.pack(fill="x", padx=10, pady=10)

        # Row 1
        tk.Label(form, text="Project Name:").grid(row=0, column=0, sticky="w")
        self.project_name = tk.Entry(form)
        self.project_name.grid(row=0, column=1, padx=10, pady=5)

        tk.Label(form, text="Buyer Name:").grid(row=0, column=2, sticky="w")
        self.buyer_name = tk.Entry(form)
        self.buyer_name.grid(row=0, column=3, padx=10, pady=5)

        # Row 2
        tk.Label(form, text="Contact No:").grid(row=1, column=0, sticky="w")
        self.contact = tk.Entry(form)
        self.contact.grid(row=1, column=1, padx=10, pady=5)

        tk.Label(form, text="Address:").grid(row=1, column=2, sticky="w")
        self.address = tk.Entry(form)
        self.address.grid(row=1, column=3, padx=10, pady=5)

        # Row 3
        tk.Label(form, text="Plot Numbers:").grid(row=2, column=0, sticky="w")
        self.plot_numbers = tk.Entry(form)
        self.plot_numbers.grid(row=2, column=1, padx=10, pady=5)

        tk.Label(form, text="Plot Area:").grid(row=2, column=2, sticky="w")
        self.plot_area = tk.Entry(form)
        self.plot_area.grid(row=2, column=3, padx=10, pady=5)

        # Row 4
        tk.Label(form, text="Total Sale Price:").grid(row=3, column=0, sticky="w")
        self.total_price = tk.Entry(form)
        self.total_price.grid(row=3, column=1, padx=10, pady=5)

        tk.Label(form, text="Advance Received:").grid(row=3, column=2, sticky="w")
        self.advance = tk.Entry(form)
        self.advance.grid(row=3, column=3, padx=10, pady=5)

        # Row 5
        tk.Label(form, text="Remaining Balance:").grid(row=4, column=0, sticky="w")
        self.balance = tk.Entry(form)
        self.balance.grid(row=4, column=1, padx=10, pady=5)

        tk.Label(form, text="Payment Mode:").grid(row=4, column=2, sticky="w")
        self.payment_mode = ttk.Combobox(form, values=["Cash", "RTGS", "UPI", "Bank Transfer"])
        self.payment_mode.grid(row=4, column=3, padx=10, pady=5)

        # Row 6
        tk.Label(form, text="Payment Date:").grid(row=5, column=0, sticky="w")
        self.payment_date = tk.Entry(form)
        self.payment_date.insert(0, datetime.date.today().strftime("%Y-%m-%d"))
        self.payment_date.grid(row=5, column=1, padx=10, pady=5)

        tk.Label(form, text="Notes:").grid(row=5, column=2, sticky="w")
        self.notes = tk.Entry(form)
        self.notes.grid(row=5, column=3, padx=10, pady=5)

        # Buttons
        tk.Button(form, text="Save Buyer", command=self.save_buyer).grid(row=6, column=0, pady=10)
        tk.Button(form, text="Update Buyer", command=self.update_buyer).grid(row=6, column=1, pady=10)
        tk.Button(form, text="Delete Buyer", command=self.delete_buyer).grid(row=6, column=2, pady=10)
        tk.Button(form, text="View All", command=self.view_all).grid(row=6, column=3, pady=10)

        # ==== Search by Project ====
        search = tk.LabelFrame(root, text="Search Buyer by Project", padx=10, pady=10)
        search.pack(fill="x", padx=10)

        tk.Label(search, text="Project Name:").pack(side="left")
        self.search_entry = tk.Entry(search)
        self.search_entry.pack(side="left", padx=10)
        tk.Button(search, text="Search", command=self.search_buyer).pack(side="left")

        # ==== Table ====
        self.tree = ttk.Treeview(root, columns=("ID", "Project", "Buyer", "Contact", "Plots", "Area", "Total", "Advance", "Balance", "Mode", "Date", "Notes"), show="headings")
        self.tree.pack(fill="both", expand=True, padx=10, pady=10)

        for col in self.tree["columns"]:
            self.tree.heading(col, text=col)
            self.tree.column(col, width=100)

        self.tree.bind("<ButtonRelease-1>", self.select_item)

    def create_table(self):
        self.cursor.execute("""
            CREATE TABLE IF NOT EXISTS buyer_section (
                id INTEGER PRIMARY KEY AUTOINCREMENT,
                project_name TEXT,
                buyer_name TEXT,
                contact TEXT,
                address TEXT,
                plot_numbers TEXT,
                plot_area TEXT,
                total_price REAL,
                advance REAL,
                balance REAL,
                payment_mode TEXT,
                payment_date TEXT,
                notes TEXT
            )
        """)
        self.conn.commit()

    def save_buyer(self):
        try:
            data = (
                self.project_name.get(),
                self.buyer_name.get(),
                self.contact.get(),
                self.address.get(),
                self.plot_numbers.get(),
                self.plot_area.get(),
                float(self.total_price.get()),
                float(self.advance.get()),
                float(self.balance.get()),
                self.payment_mode.get(),
                self.payment_date.get(),
                self.notes.get()
            )
            self.cursor.execute("""
                INSERT INTO buyer_section (
                    project_name, buyer_name, contact, address, plot_numbers, plot_area,
                    total_price, advance, balance, payment_mode, payment_date, notes
                ) VALUES (?, ?, ?, ?, ?, ?, ?, ?, ?, ?, ?, ?)
            """, data)
            self.conn.commit()
            messagebox.showinfo("Success", "Buyer data saved successfully.")
            self.clear_form()
            self.view_all()
        except Exception as e:
            messagebox.showerror("Error", f"Error: {e}")

    def view_all(self):
        self.tree.delete(*self.tree.get_children())
        self.cursor.execute("SELECT id, project_name, buyer_name, contact, plot_numbers, plot_area, total_price, advance, balance, payment_mode, payment_date, notes FROM buyer_section")
        for row in self.cursor.fetchall():
            self.tree.insert("", "end", values=row)

    def search_buyer(self):
        self.tree.delete(*self.tree.get_children())
        keyword = self.search_entry.get()
        self.cursor.execute("SELECT id, project_name, buyer_name, contact, plot_numbers, plot_area, total_price, advance, balance, payment_mode, payment_date, notes FROM buyer_section WHERE project_name LIKE ?", (f"%{keyword}%",))
        for row in self.cursor.fetchall():
            self.tree.insert("", "end", values=row)

    def select_item(self, event):
        selected = self.tree.focus()
        if selected:
            values = self.tree.item(selected, "values")
            self.selected_id = values[0]
            self.project_name.delete(0, tk.END)
            self.project_name.insert(0, values[1])
            self.buyer_name.delete(0, tk.END)
            self.buyer_name.insert(0, values[2])
            self.contact.delete(0, tk.END)
            self.contact.insert(0, values[3])
            self.plot_numbers.delete(0, tk.END)
            self.plot_numbers.insert(0, values[4])
            self.plot_area.delete(0, tk.END)
            self.plot_area.insert(0, values[5])
            self.total_price.delete(0, tk.END)
            self.total_price.insert(0, values[6])
            self.advance.delete(0, tk.END)
            self.advance.insert(0, values[7])
            self.balance.delete(0, tk.END)
            self.balance.insert(0, values[8])
            self.payment_mode.set(values[9])
            self.payment_date.delete(0, tk.END)
            self.payment_date.insert(0, values[10])
            self.notes.delete(0, tk.END)
            self.notes.insert(0, values[11])

    def update_buyer(self):
        if not self.selected_id:
            messagebox.showwarning("No selection", "Please select a record to update.")
            return
        try:
            data = (
                self.project_name.get(),
                self.buyer_name.get(),
                self.contact.get(),
                self.address.get(),
                self.plot_numbers.get(),
                self.plot_area.get(),
                float(self.total_price.get()),
                float(self.advance.get()),
                float(self.balance.get()),
                self.payment_mode.get(),
                self.payment_date.get(),
                self.notes.get(),
                self.selected_id
            )
            self.cursor.execute("""
                UPDATE buyer_section SET
                    project_name=?, buyer_name=?, contact=?, address=?, plot_numbers=?,
                    plot_area=?, total_price=?, advance=?, balance=?, payment_mode=?,
                    payment_date=?, notes=?
                WHERE id=?
            """, data)
            self.conn.commit()
            messagebox.showinfo("Success", "Buyer data updated successfully.")
            self.clear_form()
            self.view_all()
        except Exception as e:
            messagebox.showerror("Error", f"Error: {e}")

    def delete_buyer(self):
        if not self.selected_id:
            messagebox.showwarning("No selection", "Please select a record to delete.")
            return
        confirm = messagebox.askyesno("Confirm Delete", "Are you sure you want to delete this record?")
        if confirm:
            self.cursor.execute("DELETE FROM buyer_section WHERE id=?", (self.selected_id,))
            self.conn.commit()
            messagebox.showinfo("Deleted", "Buyer data deleted successfully.")
            self.clear_form()
            self.view_all()

    def clear_form(self):
        self.selected_id = None
        for widget in [self.project_name, self.buyer_name, self.contact, self.address, self.plot_numbers,
                       self.plot_area, self.total_price, self.advance, self.balance, self.notes]:
            widget.delete(0, tk.END)
        self.payment_mode.set('')
        self.payment_date.delete(0, tk.END)
        self.payment_date.insert(0, datetime.date.today().strftime("%Y-%m-%d"))

# Run the App
if __name__ == "__main__":
    root = tk.Tk()
    app = BuyerSection(root)
    root.mainloop()
