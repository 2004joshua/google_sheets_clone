# database.py
import pandas as pd
import sqlite3
import logging

DATABASE = 'database.db'

def get_connection():
    return sqlite3.connect(DATABASE)

def load_csv_to_sqlite(csv_file, table_name):
    try:
        df = pd.read_csv(csv_file)
        conn = get_connection()
        # Insert data into the table; use 'fail' to avoid overwriting an existing table
        df.to_sql(table_name, conn, if_exists='fail', index=False)
        conn.commit()
        conn.close()
        print(f"CSV file '{csv_file}' successfully loaded into table '{table_name}'.")
    except Exception as e:
        logging.error(f"Error loading CSV to SQLite: {e}")
        print(f"Error: {e}")

def infer_sqlite_type(dtype):
    if pd.api.types.is_integer_dtype(dtype):
        return "INTEGER"
    elif pd.api.types.is_float_dtype(dtype):
        return "REAL"
    else:
        return "TEXT"

def create_table_from_csv(csv_file, table_name):
    try:
        df = pd.read_csv(csv_file)
        conn = get_connection()
        cursor = conn.cursor()
        # Check if the table already exists
        cursor.execute("SELECT name FROM sqlite_master WHERE type='table' AND name=?;", (table_name,))
        existing = cursor.fetchone()
        if existing:
            # Retrieve existing table schema
            cursor.execute(f"PRAGMA table_info({table_name});")
            existing_schema = cursor.fetchall()  # Each row: (cid, name, type, notnull, dflt_value, pk)
            existing_columns = {col[1]: col[2] for col in existing_schema}
            # Infer new schema from the CSV
            new_columns = {col: infer_sqlite_type(dtype) for col, dtype in zip(df.columns, df.dtypes)}
            conflict = False
            for col in new_columns:
                if col in existing_columns and existing_columns[col] != new_columns[col]:
                    conflict = True
                    print(f"Schema conflict for column '{col}': existing type {existing_columns[col]} vs new type {new_columns[col]}")
            if conflict:
                choice = input("Schema conflict detected. Type 'overwrite' to replace table, 'rename' to create a new table, or 'skip' to cancel: ").strip().lower()
                if choice == 'overwrite':
                    cursor.execute(f"DROP TABLE IF EXISTS {table_name};")
                    conn.commit()
                elif choice == 'rename':
                    table_name = table_name + "_new"
                    print(f"New table will be created as '{table_name}'.")
                elif choice == 'skip':
                    print("Skipping table creation.")
                    conn.close()
                    return
                else:
                    print("Invalid choice. Skipping table creation.")
                    conn.close()
                    return
            else:
                print("No schema conflicts detected. Appending data to existing table.")
        # Build the CREATE TABLE statement dynamically
        columns = []
        for col, dtype in zip(df.columns, df.dtypes):
            sql_type = infer_sqlite_type(dtype)
            columns.append(f"{col} {sql_type}")
        create_stmt = f"CREATE TABLE IF NOT EXISTS {table_name} ({', '.join(columns)});"
        cursor.execute(create_stmt)
        conn.commit()
        # Insert CSV data into the table
        df.to_sql(table_name, conn, if_exists='append', index=False)
        conn.commit()
        conn.close()
        print(f"Table '{table_name}' created (or updated) and CSV data inserted.")
    except Exception as e:
        logging.error(f"Error creating table from CSV: {e}")
        print(f"Error: {e}")

def list_tables():
    try:
        conn = get_connection()
        cursor = conn.cursor()
        cursor.execute("SELECT name FROM sqlite_master WHERE type='table';")
        tables = cursor.fetchall()
        conn.close()
        print("Tables in the database:")
        for table in tables:
            print(f"- {table[0]}")
    except Exception as e:
        logging.error(f"Error listing tables: {e}")
        print(f"Error: {e}")

def execute_query(query):
    try:
        conn = get_connection()
        cursor = conn.cursor()
        cursor.execute(query)
        rows = cursor.fetchall()
        columns = [description[0] for description in cursor.description] if cursor.description else []
        conn.commit()
        conn.close()
        print("Query executed. Results:")
        if columns:
            print("\t".join(columns))
        for row in rows:
            print("\t".join(map(str, row)))
    except Exception as e:
        logging.error(f"Error executing query: {e}")
        print(f"Error: {e}")
