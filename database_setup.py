import sqlite3

# Connect to the database (Creates 'real_estate.db' if not exists)
conn = sqlite3.connect('real_estate.db')
cursor = conn.cursor()

# 1️⃣ Land Acquisition Table
cursor.execute('''
CREATE TABLE IF NOT EXISTS land_acquisition (
    land_id INTEGER PRIMARY KEY AUTOINCREMENT,
    land_name TEXT NOT NULL,
    total_purchase_price REAL NOT NULL,
    location TEXT NOT NULL,
    area_unit TEXT CHECK(area_unit IN ('Kanal', 'Marla', 'Gaj', 'Acre', 'Square Feet', 'Biswa', 'Square Meter', 'Guntha', 'Ground')) NOT NULL,
    total_area REAL NOT NULL,
    seller_names TEXT NOT NULL,
    payment_date TEXT NOT NULL,
    payment_mode TEXT CHECK(payment_mode IN ('Cash', 'RTGS', 'UPI', 'Bank Transfer')) NOT NULL,
    amount_paid REAL NOT NULL,
    remaining_balance REAL NOT NULL,
    additional_notes TEXT
);
''')

# 2️⃣ Land-Related Expenses Table
cursor.execute('''
CREATE TABLE IF NOT EXISTS land_expenses (
    expense_id INTEGER PRIMARY KEY AUTOINCREMENT,
    land_id INTEGER NOT NULL,
    expense_type TEXT NOT NULL,
    payment_mode TEXT CHECK(payment_mode IN ('Cash', 'RTGS', 'UPI', 'Bank Transfer')) NOT NULL,
    amount_paid REAL NOT NULL,
    payment_date TEXT NOT NULL,
    remaining_balance REAL NOT NULL,
    notes TEXT,
    FOREIGN KEY (land_id) REFERENCES land_acquisition(land_id) ON DELETE CASCADE
);
''')

# 3️⃣ Daily Expenses Table
cursor.execute('''
CREATE TABLE IF NOT EXISTS daily_expenses (
    expense_id INTEGER PRIMARY KEY AUTOINCREMENT,
    expense_type TEXT NOT NULL,
    amount_paid REAL NOT NULL,
    payment_date TEXT NOT NULL,
    project_name TEXT NOT NULL,
    vendor_name TEXT NOT NULL,
    notes TEXT
);
''')

# 4️⃣ Employee Salary Management Table
cursor.execute('''
CREATE TABLE IF NOT EXISTS employee_salary (
    employee_id INTEGER PRIMARY KEY AUTOINCREMENT,
    employee_name TEXT NOT NULL,
    total_salary REAL NOT NULL,
    payment_date TEXT NOT NULL,
    payment_status TEXT CHECK(payment_status IN ('Paid', 'Unpaid')) NOT NULL,
    next_payment_date TEXT NOT NULL,
    additional_costs REAL NOT NULL,
    notes TEXT
);
''')

# 5️⃣ Sales Tracking Table (Project-Based)
cursor.execute('''
CREATE TABLE IF NOT EXISTS sales_tracking (
    project_id INTEGER PRIMARY KEY AUTOINCREMENT,
    project_name TEXT NOT NULL,
    total_plots INTEGER NOT NULL,
    sold_plots TEXT NOT NULL,  -- Example: "Plot 1, Plot 2, Plot 3"
    remaining_plots TEXT NOT NULL,  -- Example: "Plot 4, Plot 5, Plot 6"
    sales_per_plot REAL NOT NULL,
    total_sales REAL NOT NULL
);
''')

# 6️⃣ Buyer Details Table
cursor.execute('''
CREATE TABLE IF NOT EXISTS buyer_details (
    buyer_id INTEGER PRIMARY KEY AUTOINCREMENT,
    buyer_name TEXT NOT NULL,
    contact_number TEXT NOT NULL,
    address TEXT NOT NULL,
    plot_numbers TEXT NOT NULL,  -- Example: "Plot 1, Plot 2"
    plot_area REAL NOT NULL,
    total_sale_price REAL NOT NULL,
    advance_payment REAL NOT NULL,
    remaining_balance REAL NOT NULL,
    payment_mode TEXT CHECK(payment_mode IN ('Cash', 'RTGS', 'UPI', 'Bank Transfer')) NOT NULL,
    payment_date TEXT NOT NULL,
    notes TEXT
);
               
''')
               
# ✅ User Table for Signup/Login
cursor.execute('''
CREATE TABLE IF NOT EXISTS users (
    user_id INTEGER PRIMARY KEY AUTOINCREMENT,
    username TEXT NOT NULL UNIQUE,
    password TEXT NOT NULL
);
''')



# Commit changes and close the connection
conn.commit()
conn.close()

print("✅ Database created successfully with all required tables!")
