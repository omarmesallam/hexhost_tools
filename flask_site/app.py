from flask import Flask, render_template, request, redirect, url_for, flash
import mysql.connector
from mysql.connector import Error

app = Flask(__name__)
app.secret_key = "secret_key_for_flash_messages"

# Database Configuration
DB_CONFIG = {
    "host": "mohamed.hexhost.online",
    "user": "mohamedm_mohamedelwan",
    "password": "3030@Salma",
    "database": "mohamedm_nouralislam",
    "port": 3306,
    "connect_timeout": 10
}

def get_db_connection():
    """Establishes a connection to the MariaDB database."""
    try:
        conn = mysql.connector.connect(**DB_CONFIG)
        if conn.is_connected():
            return conn
    except Error as e:
        print(f"Database connection error: {e}")
    return None

@app.route("/")
def index():
    """Reads and displays data from the 'secretdata' table."""
    conn = get_db_connection()
    if not conn:
        return "Failed to connect to the database. Check your remote access settings."

    table_name = "secretdata"
    data = []
    columns = []

    try:
        cursor = conn.cursor(dictionary=True)
        # Ensure table exists (optional, but good for demo)
        cursor.execute(f"SHOW TABLES LIKE '{table_name}'")
        if not cursor.fetchone():
            flash(f"Table '{table_name}' does not exist. Please create it first.", "warning")
        else:
            cursor.execute(f"SELECT * FROM {table_name}")
            data = cursor.fetchall()
            if data:
                columns = list(data[0].keys())
        
        cursor.close()
        conn.close()
    except Error as e:
        flash(f"Error accessing table: {e}", "danger")
    
    return render_template("index.html", data=data, columns=columns)

@app.route("/add", methods=["POST"])
def add_data():
    """Adds data to the 'secretdata' table."""
    full_name = request.form.get("full_name")
    email = request.form.get("email")

    if not full_name or not email:
        flash("Full Name and Email are required!", "danger")
        return redirect(url_for("index"))

    conn = get_db_connection()
    if not conn:
        flash("Failed to connect to the database.", "danger")
        return redirect(url_for("index"))

    table_name = "secretdata"
    try:
        cursor = conn.cursor()
        
        # Get target columns (filtering out auto_increment)
        cursor.execute(f"SHOW COLUMNS FROM {table_name}")
        cols_info = cursor.fetchall()
        target_columns = [col[0] for col in cols_info if 'auto_increment' not in col[5].lower()]
        
        # Match input to target columns (expecting full_name and email as first two)
        insert_columns = target_columns[:2] 
        col_names_str = ", ".join(insert_columns)
        placeholders = ", ".join(["%s"] * len(insert_columns))
        
        sql = f"INSERT INTO {table_name} ({col_names_str}) VALUES ({placeholders})"
        cursor.execute(sql, (full_name, email))
        
        conn.commit()
        flash("Data added successfully!", "success")
        
        cursor.close()
        conn.close()
    except Error as e:
        flash(f"Error adding data: {e}", "danger")
        if conn.is_connected():
            conn.rollback()

    return redirect(url_for("index"))

@app.route("/create-table")
def create_table_route():
    """Creates the 'secretdata' table if it doesn't exist."""
    conn = get_db_connection()
    if not conn:
        flash("Failed to connect to the database.", "danger")
        return redirect(url_for("index"))

    table_name = "secretdata"
    fields = [
        "id INT AUTO_INCREMENT PRIMARY KEY",
        "full_name VARCHAR(255)",
        "email VARCHAR(255)",
        "created_at TIMESTAMP DEFAULT CURRENT_TIMESTAMP"
    ]

    try:
        cursor = conn.cursor()
        fields_str = ", ".join(fields)
        sql = f"CREATE TABLE IF NOT EXISTS {table_name} ({fields_str})"
        cursor.execute(sql)
        flash(f"Table '{table_name}' checked/created successfully.", "success")
        cursor.close()
        conn.close()
    except Error as e:
        flash(f"Error creating table: {e}", "danger")

    return redirect(url_for("index"))

if __name__ == "__main__":
    app.run(debug=True, port=5000)
