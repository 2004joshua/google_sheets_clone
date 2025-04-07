# csv_loader.py
import pandas as pd
import sqlite3
import logging
from schema_inference import infer_sqlite_schema
from conflict_handler import get_existing_schema, handle_schema_conflict

def load_csv_to_sqlite(csv_file, db_path, table_name, infer_schema=True):
    try:
        # Read CSV into a DataFrame
        df = pd.read_csv(csv_file)
    except Exception as e:
        logging.error(f"Error reading CSV file {csv_file}: {e}")
        raise

    conn = sqlite3.connect(db_path)
    cursor = conn.cursor()

    if infer_schema:
        # Check if table already exists
        existing_schema = get_existing_schema(conn, table_name)
        create_table_sql = infer_sqlite_schema(df, table_name)
        if existing_schema:
            # Handle schema conflict with user decision
            choice = handle_schema_conflict(existing_schema, create_table_sql)
            if choice == 'o':  # Overwrite
                cursor.execute(f"DROP TABLE IF EXISTS {table_name};")
            elif choice == 'r':  # Rename
                new_name = input("Enter new table name: ")
                table_name = new_name
                create_table_sql = infer_sqlite_schema(df, table_name)
            elif choice == 's':  # Skip loading
                conn.close()
                return
            else:
                logging.error("Invalid choice for schema conflict resolution.")
                conn.close()
                return

        try:
            cursor.execute(create_table_sql)
            conn.commit()
        except Exception as e:
            logging.error(f"Error creating table with SQL '{create_table_sql}': {e}")
            conn.close()
            raise

    try:
        # Insert data into SQLite table using pandas.to_sql
        df.to_sql(table_name, conn, if_exists='append', index=False)
    except Exception as e:
        logging.error(f"Error inserting data into table {table_name}: {e}")
        conn.close()
        raise

    conn.close()
