# main.py
import sqlite3
import pandas as pd
from database import connect_db, execute_query, list_tables
from csv_loader import load_csv_to_sqlite
from lll_integration import generate_sql_from_query
from utils import setup_logging

def main():
    setup_logging()  # Configure logging to error_log.txt
    db_path = "database.db"
    conn = connect_db(db_path)
    
    while True:
        print("\n--- Menu ---")
        print("1. Load CSV")
        print("2. Run SQL Query")
        print("3. List Tables")
        print("4. Generate SQL from Natural Language Query")
        print("5. Exit")
        choice = input("Enter your choice: ")
        
        if choice == '1':
            csv_file = input("Enter CSV file path: ")
            table_name = input("Enter table name: ")
            try:
                load_csv_to_sqlite(csv_file, db_path, table_name, infer_schema=True)
                print(f"CSV loaded into table '{table_name}'.")
            except Exception as e:
                print("Error loading CSV. Check error_log.txt for details.")
        elif choice == '2':
            sql_query = input("Enter SQL query: ")
            try:
                result = execute_query(conn, sql_query)
                print(result)
            except Exception as e:
                print("Error executing query. Check error_log.txt for details.")
        elif choice == '3':
            try:
                tables = list_tables(conn)
                print("Available tables:")
                for table in tables:
                    print(table)
            except Exception as e:
                print("Error listing tables. Check error_log.txt for details.")
        elif choice == '4':
            table_schema = input("Enter table schema (e.g., sales (sale_id, product_id, quantity)): ")
            user_query = input("Enter your natural language query: ")
            response = generate_sql_from_query(table_schema, user_query)
            print("\nGenerated SQL:")
            print(response['sql'])
            print("\nExplanation:")
            print(response['explanation'])
        elif choice == '5':
            print("Exiting.")
            break
        else:
            print("Invalid choice. Please try again.")

if __name__ == '__main__':
    main()
