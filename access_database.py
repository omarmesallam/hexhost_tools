import mysql.connector
from mysql.connector import Error

def connect_to_db():
    """Establishes a connection to the MariaDB database."""
    try:
        mydb = mysql.connector.connect(
            host="mohamed.hexhost.online",
            user="mohamedm_mohamedelwan",
            password="3030@Salma",
            database="mohamedm_nouralislam",
            port=3306,
            connect_timeout=10
        )
        if mydb.is_connected():
            print("Successfully connected to the database!")
            return mydb
    except Error as e:
        if e.errno == 1130:
            print("\n[REMOTE ACCESS DENIED] MariaDB Error 1130")
            print(f"Details: {e.msg}")
            print("TO FIX: Log into your cPanel, find 'Remote MySQL', and add your IP to the whitelist.")
        else:
            print(f"Error while connecting to MariaDB: {e}")
        
        error_str = str(e)
        if "110" in error_str or "10060" in error_str:
            print("\nTIP: Connection Timed Out. Check your IP whitelist in cPanel.")
        return None

def create_table(connection, table_name, fields):
    """
    Creates a new table in the database.
    
    Args:
        connection: Active database connection.
        table_name (str): Name of the new table.
        fields (list): List of field definitions (e.g., ["id INT AUTO_INCREMENT PRIMARY KEY", "name VARCHAR(255)"]).
    """
    if not connection or not connection.is_connected():
        print("Error: No active database connection.")
        return

    try:
        cursor = connection.cursor()
        
        # Join the list of fields into a comma-separated string
        fields_str = ", ".join(fields)
        sql = f"CREATE TABLE {table_name} ({fields_str})"
        
        print(f"Creating table '{table_name}'...")
        cursor.execute(sql)
        print(f"Table '{table_name}' created successfully.")
        
        cursor.close()
    except Error as e:
        print(f"Error creating table: {e}")

def read_table_data(connection, table_name):
    """Reads and displays data from a specific table."""
    if not connection or not connection.is_connected():
        print("Error: No active database connection.")
        return

    try:
        cursor = connection.cursor()
        print(f"\nFetching data from '{table_name}'...")
        cursor.execute(f"SELECT * FROM {table_name}")
        
        rows = cursor.fetchall()
        
        if not rows:
            print(f"The table '{table_name}' is empty.")
        else:
            # Print column names
            column_names = [i[0] for i in cursor.description]
            print(f"Columns: {column_names}")
            print("-" * 50)
            
            for row in rows:
                print(row)
        
        cursor.close()
    except Error as e:
        print(f"Error accessing table '{table_name}': {e}")
        if e.errno == 1146:
            print(f"TIP: Table '{table_name}' does not exist.")


def add_data_to_table(connection, table_name, data_rows):
    """
    Adds data to a specific table.

    Args:
        connection: Active database connection.
        table_name (str): Name of the table to add data to.
        data_rows (list): List of data rows to insert.
    """
    if not connection or not connection.is_connected():
        print("Error: No active database connection.")
        return

    if not data_rows:
        print("No data to insert.")
        return

    try:
        cursor = connection.cursor()
        
        # Get column names to build the query
        cursor.execute(f"SHOW COLUMNS FROM {table_name}")
        columns = cursor.fetchall()
        
        # Filter columns that are not AUTO_INCREMENT
        # col[0] is the column name, col[5] is the 'Extra' field (e.g., 'auto_increment')
        target_columns = [col[0] for col in columns if 'auto_increment' not in col[5].lower()]
        
        # We assume the data_rows match the first N non-auto-increment columns
        num_data_cols = len(data_rows[0])
        insert_columns = target_columns[:num_data_cols]
        
        col_names_str = ", ".join(insert_columns)
        placeholders = ", ".join(["%s"] * num_data_cols)
        
        sql = f"INSERT INTO {table_name} ({col_names_str}) VALUES ({placeholders})"
        
        print(f"Inserting data into '{table_name}'...")
        cursor.executemany(sql, data_rows)
        connection.commit()
        
        print(f"Successfully inserted {cursor.rowcount} rows.")
        cursor.close()
    except Error as e:
        print(f"Error inserting data into '{table_name}': {e}")
        if connection.is_connected():
            connection.rollback()



if __name__ == "__main__":
    # 1. Connect
    connection = connect_to_db()
    
    if connection:
        # 2. Example: Create a new table
        # We specify both the name and the type for each field
        new_fields = [
            "id INT AUTO_INCREMENT PRIMARY KEY",
            "full_name VARCHAR(255)",
            "email VARCHAR(255)",
            "created_at TIMESTAMP DEFAULT CURRENT_TIMESTAMP"
        ]

        data_rows = [['mohamed hussin','mhussin@fff.sss'],
                ['ahmed hussin','sdsdad@ddd.com']

                ]
        
        # Uncomment the line below to actually create a table
        # create_table(connection, "users_table", new_fields)
        
        # 3. Read Data

        add_data_to_table(connection, "secretdata", data_rows)
        # create_table(connection,'secretdata',
        #              new_fields)

        read_table_data(connection, "secretdata")

        # 4. Close Connection
        connection.close()
        print("\nConnection closed.")
