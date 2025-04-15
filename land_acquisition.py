import tkinter as tk
from tkinter import ttk, messagebox
import sqlite3
import tempfile
import os

class LandAcquisition:
    def __init__(self, root):
        self.root = root
        self.root.title("🟩 Land Acquisition Details")
        self.root.geometry("1100x750")
        self.root.config(bg="#f4f4f4")

        # Database
        self.conn = sqlite3.connect("real_estate.db")
        self.cursor = self.conn.cursor()
        self.create_table()

        # Scrollable Frame
        container = tk.Frame(self.root)
        canvas = tk.Canvas(container, bg="#f4f4f4", height=650)
        scrollbar = tk.Scrollbar(container, orient="vertical", command=canvas.yview)
        self.scrollable_frame = tk.Frame(canvas, bg="#f4f4f4")

        self.scrollable_frame.bind(
            "<Configure>",
            lambda e: canvas.configure(scrollregion=canvas.bbox("all"))
        )

        canvas.create_window((0, 0), window=self.scrollable_frame, anchor="nw")
        canvas.configure(yscrollcommand=scrollbar.set)

        container.pack(fill="both", expand=True)
        canvas.pack(side="left", fill="both", expand=True)
        scrollbar.pack(side="right", fill="y")

        # Form Frame
        form_frame = tk.LabelFrame(self.scrollable_frame, text="Enter Land Acquisition Details", padx=15, pady=15, font=("Arial", 12, "bold"), bg="#f9f9f9")
        form_frame.pack(padx=20, pady=20, fill="both")

        labels = [
            "Land ID", "Land Name", "Total Purchase Price", "Location", "Select Area",
            "Total Area", "Seller Names", "Payment Date", "Payment Mode",
            "Amount Paid", "Remaining Balance", "Additional Notes"
        ]
        self.entries = {}

        for i, label in enumerate(labels):
            tk.Label(form_frame, text=label + ":", font=("Arial", 10), bg="#f9f9f9").grid(row=i, column=0, padx=10, pady=6, sticky="w")

        self.entries["land_id"] = tk.Entry(form_frame, width=30, font=("Arial", 10))
        self.entries["land_id"].grid(row=0, column=1, padx=10, pady=6)

        self.entries["land_name"] = tk.Entry(form_frame, width=30, font=("Arial", 10))
        self.entries["land_name"].grid(row=1, column=1, padx=10, pady=6)

        self.entries["total_purchase_price"] = tk.Entry(form_frame, width=30, font=("Arial", 10))
        self.entries["total_purchase_price"].grid(row=2, column=1, padx=10, pady=6)

        self.entries["location"] = tk.Entry(form_frame, width=30, font=("Arial", 10))
        self.entries["location"].grid(row=3, column=1, padx=10, pady=6)

        self.entries["area_unit"] = ttk.Combobox(form_frame, values=[
            "Kanal", "Marla", "Gaj", "Acre", "Sq Feet", "Biswa", "Sq Meter", "Guntha", "Ground"
        ], width=28, state="readonly", font=("Arial", 10))
        self.entries["area_unit"].grid(row=4, column=1, padx=10, pady=6)

        self.entries["total_area"] = tk.Entry(form_frame, width=30, font=("Arial", 10))
        self.entries["total_area"].grid(row=5, column=1, padx=10, pady=6)

        self.entries["seller_names"] = tk.Entry(form_frame, width=30, font=("Arial", 10))
        self.entries["seller_names"].grid(row=6, column=1, padx=10, pady=6)

        self.entries["payment_date"] = tk.Entry(form_frame, width=30, font=("Arial", 10))
        self.entries["payment_date"].grid(row=7, column=1, padx=10, pady=6)

        self.entries["payment_mode"] = ttk.Combobox(form_frame, values=[
            "Cash", "RTGS", "UPI", "Bank Transfer"
        ], width=28, state="readonly", font=("Arial", 10))
        self.entries["payment_mode"].grid(row=8, column=1, padx=10, pady=6)

        self.entries["amount_paid"] = tk.Entry(form_frame, width=30, font=("Arial", 10))
        self.entries["amount_paid"].grid(row=9, column=1, padx=10, pady=6)

        self.entries["remaining_balance"] = tk.Entry(form_frame, width=30, font=("Arial", 10))
        self.entries["remaining_balance"].grid(row=10, column=1, padx=10, pady=6)

        self.entries["additional_notes"] = tk.Entry(form_frame, width=30, font=("Arial", 10))
        self.entries["additional_notes"].grid(row=11, column=1, padx=10, pady=6)

        # Buttons
        tk.Button(form_frame, text="Save", command=self.save_data, bg="#c6f6c4", font=("Arial", 10)).grid(row=12, column=0, pady=10)
        tk.Button(form_frame, text="Update", command=self.update_data, bg="#ffd580", font=("Arial", 10)).grid(row=12, column=1, pady=10)
        tk.Button(form_frame, text="Delete", command=self.delete_data, bg="#f6a6a6", font=("Arial", 10)).grid(row=13, column=0, pady=5)
        tk.Button(form_frame, text="View Records", command=self.view_details, bg="#b3e5fc", font=("Arial", 10)).grid(row=14, column=0, columnspan=2, pady=10)

        # Table Frame
        table_frame = tk.LabelFrame(self.scrollable_frame, text="Saved Records", font=("Arial", 12, "bold"))
        table_frame.pack(fill="both", expand=True, padx=20, pady=10)

        self.tree = ttk.Treeview(table_frame, columns=(
            "ID", "Land Name", "Price", "Location", "Area Unit", "Total Area", "Seller",
            "Payment Date", "Payment Mode", "Paid", "Remaining", "Notes"
        ), show="headings")

        for col in self.tree["columns"]:
            self.tree.heading(col, text=col)
            self.tree.column(col, width=100)

        self.tree.pack(side="left", fill="both", expand=True)
        vsb = ttk.Scrollbar(table_frame, orient="vertical", command=self.tree.yview)
        self.tree.configure(yscrollcommand=vsb.set)
        vsb.pack(side="right", fill="y")

        self.tree.bind("<<TreeviewSelect>>", self.load_selected_row)
        self.selected_id = None
        self.view_details()

    def create_table(self):
        self.cursor.execute("""
            CREATE TABLE IF NOT EXISTS land_acquisition (
                land_id INTEGER PRIMARY KEY AUTOINCREMENT,
                land_name TEXT,
                total_purchase_price REAL,
                location TEXT,
                area_unit TEXT,
                total_area REAL,
                seller_names TEXT,
                payment_date TEXT,
                payment_mode TEXT,
                amount_paid REAL,
                remaining_balance REAL,
                additional_notes TEXT
            )
        """)
        self.conn.commit()

    def get_input_data(self):
        try:
            data = (
                self.entries["land_name"].get(),
                float(self.entries["total_purchase_price"].get()),
                self.entries["location"].get(),
                self.entries["area_unit"].get(),
                float(self.entries["total_area"].get()),
                self.entries["seller_names"].get(),
                self.entries["payment_date"].get(),
                self.entries["payment_mode"].get(),
                float(self.entries["amount_paid"].get()),
                float(self.entries["remaining_balance"].get()),
                self.entries["additional_notes"].get()
            )
            return data
        except ValueError:
            messagebox.showerror("Invalid Input", "Please fill all fields correctly.")
            return None

    def save_data(self):
        data = self.get_input_data()
        if data:
            self.cursor.execute("""
                INSERT INTO land_acquisition (
                    land_name, total_purchase_price, location, area_unit, total_area,
                    seller_names, payment_date, payment_mode, amount_paid,
                    remaining_balance, additional_notes
                ) VALUES (?, ?, ?, ?, ?, ?, ?, ?, ?, ?, ?)
            """, data)
            self.conn.commit()
            messagebox.showinfo("Success", "Data Saved!")
            self.clear_fields()
            self.view_details()

    def update_data(self):
        data = self.get_input_data()
        if data and self.selected_id:
            self.cursor.execute("""
                UPDATE land_acquisition SET
                    land_name=?, total_purchase_price=?, location=?, area_unit=?, total_area=?,
                    seller_names=?, payment_date=?, payment_mode=?, amount_paid=?,
                    remaining_balance=?, additional_notes=?
                WHERE land_id=?
            """, data + (int(self.selected_id),))
            self.conn.commit()
            messagebox.showinfo("Updated", "Record Updated!")
            self.clear_fields()
            self.view_details()
        else:
            messagebox.showwarning("Warning", "No record selected for update.")

    def delete_data(self):
        try:
            land_id = int(self.entries["land_id"].get())
        except ValueError:
            messagebox.showwarning("Warning", "Invalid Land ID.")
            return

        confirm = messagebox.askyesno("Confirm Delete", "Are you sure to delete this record?")
        if confirm:
            self.cursor.execute("DELETE FROM land_acquisition WHERE land_id=?", (land_id,))
            self.conn.commit()
            messagebox.showinfo("Deleted", "Record Deleted.")
            self.clear_fields()
            self.view_details()

    def view_details(self):
        self.tree.delete(*self.tree.get_children())
        self.cursor.execute("SELECT * FROM land_acquisition")
        for row in self.cursor.fetchall():
            self.tree.insert("", "end", values=row)

    def load_selected_row(self, event):
        selected = self.tree.focus()
        if selected:
            values = self.tree.item(selected, 'values')
            keys = list(self.entries.keys())
            for i, key in enumerate(keys):
                self.entries[key].delete(0, tk.END)
                self.entries[key].insert(0, values[i])
            self.selected_id = values[0]  # Ensure it's numeric

    
    def clear_fields(self):
        for entry in self.entries.values():
            entry.delete(0, tk.END)
        self.selected_id = None


# Run App
if __name__ == "__main__":
    root = tk.Tk()
    app = LandAcquisition(root)
    root.mainloop()
