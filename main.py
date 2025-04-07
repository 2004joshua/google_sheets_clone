# main.py

import sqlite3
from database import get_connection, execute_query, list_tables
from csv_loader import load_csv_to_sqlite
from lll_integration import generate_sql_from_query
from utils import setup_logging

setup_logging()  # Initialize logging

def cli_loop():
    conn = get_connection("database.db")
    
    while True:
        print("\nOptions:")
        print("1. Load CSV")
        print("2. Run SQL Query")
        print("3. List Tables")
        print("4. Run natural language query via LLM")
        print("5. Exit")
        choice = input("Enter your choice: ").strip()
        
        if choice == '1':
            file_path = input("Enter CSV file path: ").strip()
            table_name = input("Enter table name: ").strip()
            try:
                # Load CSV into SQLite with dynamic table creation and conflict handling
                _, inferred_sql = load_csv_to_sqlite(file_path, conn, table_name)
                print(f"CSV loaded into table '{table_name}'.")
                print("Table creation SQL was:")
                print(inferred_sql)
            except Exception as e:
                print("Error loading CSV. Check error_log.txt for details.")
        elif choice == '2':
            sql_query = input("Enter SQL query: ").strip()
            try:
                result = execute_query(conn, sql_query)
                print("Query Results:")
                print(result)
            except Exception as e:
                print("Error executing query. Check error_log.txt for details.")
        elif choice == '3':
            print("Listing tables:")
            print(list_tables(conn))
        elif choice == '4':
            # Simulate a natural language query using LLM integration
            table_schema = input("Enter table schema (e.g., sales (sale_id, product_id, quantity)): ").strip()
            user_query = input("Enter your natural language query: ").strip()
            response = generate_sql_from_query(table_schema, user_query)
            print("Generated SQL:")
            print(response['sql'])
            print("Explanation:")
            print(response['explanation'])
        elif choice == '5':
            print("Exiting.")
            break
        else:
            print("Invalid option. Please try again.")
    
    conn.close()

if __name__ == "__main__":
    cli_loop()
