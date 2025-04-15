import tkinter as tk
from tkinter import ttk, messagebox
import sqlite3

class SalesTracking:
    def __init__(self, root):
        self.root = root
        self.root.title("Sales Tracking - Project Based")
        self.root.geometry("1100x600")

        # Connect to database
        self.conn = sqlite3.connect("real_estate.db")
        self.cursor = self.conn.cursor()

        self.selected_id = None

        # ==== Form Frame ====
        form_frame = tk.LabelFrame(root, text="Add / Update Project Sales", padx=10, pady=10)
        form_frame.pack(fill="x", padx=10, pady=10)

        self.fields = {}
        labels = [
            "Project Name:",
            "Total Plots:",
            "Sold Plots (e.g., 1,2,3):",
            "Remaining Plots (e.g., 4,5,6):",
            "Sales per Plot (Rs.):",
            "Total Sales (Rs.):"
        ]
        for i, label in enumerate(labels):
            tk.Label(form_frame, text=label).grid(row=i, column=0, sticky="w")
            entry = tk.Entry(form_frame, width=40)
            entry.grid(row=i, column=1, padx=10, pady=5)
            self.fields[label] = entry

        # Buttons in one row
        btn_frame = tk.Frame(form_frame)
        btn_frame.grid(row=6, column=0, columnspan=2, pady=10)

        tk.Button(btn_frame, text="Save Sales", width=15, command=self.save_sales).pack(side="left", padx=5)
        tk.Button(btn_frame, text="Update Selected", width=15, command=self.update_sales).pack(side="left", padx=5)
        tk.Button(btn_frame, text="Delete Selected", width=15, command=self.delete_record, bg="red", fg="white").pack(side="left", padx=5)

        # ==== Search Frame ====
        search_frame = tk.LabelFrame(root, text="Search by Project Name", padx=10, pady=10)
        search_frame.pack(fill="x", padx=10, pady=5)

        tk.Label(search_frame, text="Project Name:").pack(side="left")
        self.search_entry = tk.Entry(search_frame, width=30)
        self.search_entry.pack(side="left", padx=10)
        tk.Button(search_frame, text="Search", command=self.search_project).pack(side="left")
        tk.Button(search_frame, text="Clear", command=self.view_all).pack(side="left", padx=5)

        # ==== Table ====
        self.columns = ("Project Name", "Total Plots", "Sold Plots", "Remaining Plots", "Sales Per Plot", "Total Sales")
        self.tree = ttk.Treeview(root, columns=self.columns, show="headings")
        self.tree.pack(fill="both", expand=True, padx=10, pady=10)

        for col in self.columns:
            self.tree.heading(col, text=col)
            self.tree.column(col, anchor="center", width=150)

        self.tree.bind("<ButtonRelease-1>", self.on_row_select)

        self.view_all()

    def save_sales(self):
        try:
            project = self.fields["Project Name:"].get().strip()
            total = int(self.fields["Total Plots:"].get())
            sold = self.fields["Sold Plots (e.g., 1,2,3):"].get().strip()
            remaining = self.fields["Remaining Plots (e.g., 4,5,6):"].get().strip()
            per_plot = float(self.fields["Sales per Plot (Rs.):"].get())
            total_sale = float(self.fields["Total Sales (Rs.):"].get())

            if not project:
                raise ValueError("Project name is required.")

            self.cursor.execute("""
                INSERT INTO sales_tracking (project_name, total_plots, sold_plots, remaining_plots, sales_per_plot, total_sales)
                VALUES (?, ?, ?, ?, ?, ?)
            """, (project, total, sold, remaining, per_plot, total_sale))
            self.conn.commit()

            messagebox.showinfo("Success", f"Sales for project '{project}' saved successfully.")
            self.clear_fields()
            self.view_all()
        except Exception as e:
            messagebox.showerror("Error", f"Failed to save sales: {e}")

    def view_all(self):
        self.tree.delete(*self.tree.get_children())
        self.cursor.execute("SELECT * FROM sales_tracking")
        for row in self.cursor.fetchall():
            self.insert_row(row)

    def insert_row(self, row):
        _, project, total, sold, remaining, per_plot, total_sales = row
        self.tree.insert("", "end", values=(
            project,
            total,
            sold,
            remaining,
            f"Rs. {per_plot:,.2f}",
            f"Rs. {total_sales:,.2f}"
        ))

    def search_project(self):
        keyword = self.search_entry.get().strip()
        self.tree.delete(*self.tree.get_children())
        self.cursor.execute("SELECT * FROM sales_tracking WHERE project_name LIKE ?", (f"%{keyword}%",))
        for row in self.cursor.fetchall():
            self.insert_row(row)

    def clear_fields(self):
        for entry in self.fields.values():
            entry.delete(0, tk.END)
        self.selected_id = None

    def on_row_select(self, event):
        selected = self.tree.focus()
        if selected:
            project_name = self.tree.item(selected, 'values')[0]
            self.cursor.execute("SELECT * FROM sales_tracking WHERE project_name = ?", (project_name,))
            row = self.cursor.fetchone()
            if row:
                self.selected_id = row[0]
                self.fields["Project Name:"].delete(0, tk.END)
                self.fields["Project Name:"].insert(0, row[1])
                self.fields["Total Plots:"].delete(0, tk.END)
                self.fields["Total Plots:"].insert(0, row[2])
                self.fields["Sold Plots (e.g., 1,2,3):"].delete(0, tk.END)
                self.fields["Sold Plots (e.g., 1,2,3):"].insert(0, row[3])
                self.fields["Remaining Plots (e.g., 4,5,6):"].delete(0, tk.END)
                self.fields["Remaining Plots (e.g., 4,5,6):"].insert(0, row[4])
                self.fields["Sales per Plot (Rs.):"].delete(0, tk.END)
                self.fields["Sales per Plot (Rs.):"].insert(0, row[5])
                self.fields["Total Sales (Rs.):"].delete(0, tk.END)
                self.fields["Total Sales (Rs.):"].insert(0, row[6])

    def update_sales(self):
        if not self.selected_id:
            messagebox.showwarning("Warning", "Please select a record to update.")
            return
        try:
            project = self.fields["Project Name:"].get().strip()
            total = int(self.fields["Total Plots:"].get())
            sold = self.fields["Sold Plots (e.g., 1,2,3):"].get().strip()
            remaining = self.fields["Remaining Plots (e.g., 4,5,6):"].get().strip()
            per_plot = float(self.fields["Sales per Plot (Rs.):"].get())
            total_sale = float(self.fields["Total Sales (Rs.):"].get())

            self.cursor.execute("""
                UPDATE sales_tracking SET 
                    project_name = ?, total_plots = ?, sold_plots = ?, 
                    remaining_plots = ?, sales_per_plot = ?, total_sales = ?
                WHERE project_id = ?
            """, (project, total, sold, remaining, per_plot, total_sale, self.selected_id))
            self.conn.commit()

            messagebox.showinfo("Success", "Record updated successfully.")
            self.clear_fields()
            self.view_all()
        except Exception as e:
            messagebox.showerror("Error", f"Failed to update record: {e}")

    def delete_record(self):
        selected = self.tree.focus()
        if not selected:
            messagebox.showwarning("Warning", "Please select a record to delete.")
            return
        confirm = messagebox.askyesno("Confirm Delete", "Are you sure you want to delete this record?")
        if confirm:
            project_name = self.tree.item(selected, 'values')[0]
            self.cursor.execute("DELETE FROM sales_tracking WHERE project_name = ?", (project_name,))
            self.conn.commit()
            messagebox.showinfo("Deleted", "Record deleted successfully.")
            self.clear_fields()
            self.view_all()

if __name__ == "__main__":
    root = tk.Tk()
    app = SalesTracking(root)
    root.mainloop()
