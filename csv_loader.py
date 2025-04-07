# csv_loader.py

import pandas as pd
from schema_inference import infer_sqlite_schema
from conflict_handler import get_existing_schema, handle_schema_conflict

def load_csv_to_sqlite(file_path, conn, table_name):
    """
    Load a CSV file into SQLite.
    Returns the DataFrame and the inferred CREATE TABLE SQL statement.
    """
    # Read CSV into DataFrame
    df = pd.read_csv(file_path)
    
    # Infer the schema and generate a CREATE TABLE statement
    create_table_sql = infer_sqlite_schema(df, table_name)
    
    # Check for an existing table schema
    existing_schema = get_existing_schema(conn, table_name)
    if existing_schema:
        action = handle_schema_conflict(existing_schema, create_table_sql, table_name)
        if action == 'overwrite':
            conn.execute(f"DROP TABLE IF EXISTS {table_name};")
            conn.execute(create_table_sql)
        elif action == 'rename':
            new_table_name = input("Enter new table name: ").strip()
            create_table_sql = create_table_sql.replace(table_name, new_table_name, 1)
            table_name = new_table_name
            conn.execute(create_table_sql)
        elif action == 'skip':
            # Use the existing table without creating a new one
            pass
    else:
        conn.execute(create_table_sql)
    
    # Insert CSV data into the table (append data if table exists)
    df.to_sql(table_name, conn, if_exists='append', index=False)
    conn.commit()
    return df, create_table_sql
