import tkinter as tk
from tkinter import messagebox
import sqlite3
import main  # Import your main app file

class LoginWindow:
    def __init__(self, root):
        self.root = root
        self.root.title("Login - Real Estate Management")
        self.root.geometry("500x470")
        self.root.configure(bg="#ecf0f1")

        try:
            self.root.iconbitmap("logo.ico")
        except:
            pass

        self.conn = sqlite3.connect("real_estate.db")
        self.cursor = self.conn.cursor()
        self.create_user_table()
        self.build_login_ui()

    def create_user_table(self):
        self.cursor.execute("""
            CREATE TABLE IF NOT EXISTS users (
                id INTEGER PRIMARY KEY AUTOINCREMENT,
                username TEXT UNIQUE NOT NULL,
                password TEXT NOT NULL
            )
        """)
        self.conn.commit()

    def build_login_ui(self):
        for widget in self.root.winfo_children():
            widget.destroy()

        frame = tk.Frame(self.root, bg="white", bd=2, relief="groove")
        frame.place(relx=0.5, rely=0.5, anchor="center", width=400, height=360)

        tk.Label(frame, text="Login", font=("Helvetica", 22, "bold"), bg="white", fg="#2c3e50").pack(pady=15)

        tk.Label(frame, text="Username", bg="white", anchor="w", font=("Arial", 13)).pack(fill="x", padx=20)
        self.login_user = tk.Entry(frame, font=("Arial", 13))
        self.login_user.pack(padx=20, pady=8, fill="x")

        tk.Label(frame, text="Password", bg="white", anchor="w", font=("Arial", 13)).pack(fill="x", padx=20)
        self.login_pass = tk.Entry(frame, show="*", font=("Arial", 13))
        self.login_pass.pack(padx=20, pady=8, fill="x")

        tk.Button(frame, text="🔐 Login", font=("Arial", 12, "bold"),
                  bg="#3498db", fg="white", height=2,
                  command=self.login).pack(pady=15)

        tk.Button(frame, text="New user? Signup here",
                  font=("Arial", 11), bg="#2ecc71", fg="white",
                  command=self.build_signup_ui).pack()

    def build_signup_ui(self):
        for widget in self.root.winfo_children():
            widget.destroy()

        frame = tk.Frame(self.root, bg="white", bd=2, relief="groove")
        frame.place(relx=0.5, rely=0.5, anchor="center", width=400, height=360)

        tk.Label(frame, text="Signup", font=("Helvetica", 22, "bold"), bg="white", fg="#2c3e50").pack(pady=15)

        tk.Label(frame, text="New Username", bg="white", anchor="w", font=("Arial", 13)).pack(fill="x", padx=20)
        self.signup_user = tk.Entry(frame, font=("Arial", 13))
        self.signup_user.pack(padx=20, pady=8, fill="x")

        tk.Label(frame, text="New Password", bg="white", anchor="w", font=("Arial", 13)).pack(fill="x", padx=20)
        self.signup_pass = tk.Entry(frame, show="*", font=("Arial", 13))
        self.signup_pass.pack(padx=20, pady=8, fill="x")

        tk.Button(frame, text="✅ Create Account", font=("Arial", 12, "bold"),
                  bg="#27ae60", fg="white", height=2,
                  command=self.signup).pack(pady=15)

        tk.Button(frame, text="Back to Login", font=("Arial", 11),
                  command=self.build_login_ui).pack()

    def signup(self):
        username = self.signup_user.get().strip()
        password = self.signup_pass.get().strip()

        if not username or not password:
            messagebox.showerror("Error", "All fields are required.")
            return

        try:
            self.cursor.execute("INSERT INTO users (username, password) VALUES (?, ?)", (username, password))
            self.conn.commit()
            messagebox.showinfo("Success", "Account created! Please login.")
            self.build_login_ui()
        except sqlite3.IntegrityError:
            messagebox.showerror("Error", "Username already exists.")

    def login(self):
        username = self.login_user.get().strip()
        password = self.login_pass.get().strip()

        self.cursor.execute("SELECT * FROM users WHERE username=? AND password=?", (username, password))
        user = self.cursor.fetchone()

        if user:
            messagebox.showinfo("Welcome", f"Welcome back, {username}!")
            self.root.destroy()
            self.launch_main_app()
        else:
            messagebox.showerror("Login Failed", "Invalid credentials!")

    def launch_main_app(self):
        new_root = tk.Tk()
        main.RealEstateApp(new_root)
        new_root.mainloop()

# ✅ Entry Point
if __name__ == "__main__":
    root = tk.Tk()
    LoginWindow(root)
    root.mainloop()
