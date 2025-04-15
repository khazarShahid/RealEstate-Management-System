import tkinter as tk
from tkinter import ttk
from PIL import Image, ImageTk

from land_acquisition import LandAcquisition
from land_expenses import LandExpenses
from daily_expenses import DailyExpenses
from salary_management import SalaryManagement
from sales_tracking import SalesTracking
from buyer_section import BuyerSection

class RealEstateApp:
    def __init__(self, root):
        self.root = root
        self.root.title("Real Estate Management System")
        self.root.geometry("900x600")
        self.root.configure(bg="#f5f5f5")

        try:
            self.root.iconbitmap("logo.ico")  # ✅ Icon (if available)
        except:
            pass

        # === Logo ===
        try:
            logo_image = Image.open("logo.jpg")
            logo_image = logo_image.resize((100, 100))
            self.logo_photo = ImageTk.PhotoImage(logo_image)
            logo_label = tk.Label(root, image=self.logo_photo, bg="#f5f5f5")
            logo_label.pack(pady=(20, 10))
        except Exception as e:
            print(f"⚠️ Could not load logo: {e}")

        # === Title ===
        title_label = tk.Label(
            root,
            text="Real Estate Management System",
            font=("Helvetica", 20, "bold"),
            bg="#f5f5f5",
            fg="#2c3e50"
        )
        title_label.pack(pady=10)

        # === Navigation ===
        nav_frame = tk.Frame(root, bg="#f5f5f5")
        nav_frame.pack(pady=20)

        self.create_nav_button(nav_frame, "🏠 Land Acquisition", LandAcquisition)
        self.create_nav_button(nav_frame, "💸 Land Expenses", LandExpenses)
        self.create_nav_button(nav_frame, "📅 Daily Expenses", DailyExpenses)
        self.create_nav_button(nav_frame, "👨‍💼 Salary Management", SalaryManagement)
        self.create_nav_button(nav_frame, "📊 Sales Tracking", SalesTracking)
        self.create_nav_button(nav_frame, "🧾 Buyer Section", BuyerSection)

        # # Footer
        # footer_label = tk.Label(
        #     root,
        #     text="© 2025 Developed by Mehwish Mushtaq",
        #     font=("Arial", 10),
        #     bg="#f5f5f5",
        #     fg="#7f8c8d"
        # )
        # footer_label.pack(side="bottom", pady=10)

    def create_nav_button(self, frame, text, window_class):
        button = tk.Button(
            frame,
            text=text,
            font=("Arial", 12),
            width=30,
            height=2,
            bg="#3498db",
            fg="white",
            activebackground="#2980b9",
            relief="raised",
            bd=3,
            command=lambda: self.open_window(window_class)
        )
        button.pack(pady=8)

    def open_window(self, window_class):
        new_window = tk.Toplevel(self.root)
        new_window.grab_set()
        window_class(new_window)