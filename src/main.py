# src/main.py

import logging
from src.database import load_csv_to_sqlite, create_table_from_csv, list_tables, execute_query
from src.ai_sql import generate_sql_from_natural_language

logging.basicConfig(filename='error_log.txt', level=logging.ERROR,
                    format='%(asctime)s:%(levelname)s:%(message)s')

def main():
    print("Welcome to the CSV to SQLite CLI with AI assistance.")
    while True:
        print("\nOptions:")
        print("1. Load CSV into SQLite (manual table creation)")
        print("2. Create table from CSV (dynamic table creation with conflict handling)")
        print("3. List tables")
        print("4. Run SQL query")
        print("5. Generate SQL from natural language")
        print("6. Exit")
        choice = input("Enter your choice: ").strip()
        if choice == '1':
            csv_file = input("Enter CSV file path: ").strip()
            table_name = input("Enter table name: ").strip()
            load_csv_to_sqlite(csv_file, table_name)
        elif choice == '2':
            csv_file = input("Enter CSV file path: ").strip()
            table_name = input("Enter table name: ").strip()
            create_table_from_csv(csv_file, table_name)
        elif choice == '3':
            list_tables()
        elif choice == '4':
            query = input("Enter SQL query: ").strip()
            execute_query(query)
        elif choice == '5':
            prompt = input("Enter your natural language query: ").strip()
            # For a real implementation, you might fetch the schema dynamically.
            schema_description = "Assume tables with columns as per your CSV inputs"
            generate_sql_from_natural_language(prompt, schema_description)
        elif choice == '6':
            print("Exiting...")
            break
        else:
            print("Invalid choice. Please try again.")

if __name__ == "__main__":
    main()
