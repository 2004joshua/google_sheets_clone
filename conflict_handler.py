# conflict_handler.py

def get_existing_schema(conn, table_name):
    """
    Retrieve the existing schema for a table using PRAGMA table_info.
    Returns a list of tuples if the table exists, otherwise an empty list.
    """
    cursor = conn.cursor()
    cursor.execute(f"PRAGMA table_info({table_name});")
    schema_info = cursor.fetchall()
    return schema_info

def handle_schema_conflict(existing_schema, inferred_schema_sql, table_name):
    """
    Handle a schema conflict by prompting the user.
    Options:
      - 'overwrite': drop the existing table and create a new one.
      - 'rename': use a different table name.
      - 'skip': keep the existing table.
    Returns the chosen action as a string.
    """
    print(f"Schema conflict detected for table '{table_name}'.")
    print("Existing schema:")
    for col in existing_schema:
        print(col)
    print("New inferred schema:")
    print(inferred_schema_sql)
    while True:
        choice = input("Enter 'o' to overwrite, 'r' to rename, or 's' to skip: ").strip().lower()
        if choice == 'o':
            return 'overwrite'
        elif choice == 'r':
            return 'rename'
        elif choice == 's':
            return 'skip'
        else:
            print("Invalid input. Please enter 'o', 'r', or 's'.")
