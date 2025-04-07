# conflict_handler.py
def get_existing_schema(conn, table_name):
    cursor = conn.cursor()
    cursor.execute(f"PRAGMA table_info({table_name});")
    return cursor.fetchall()

def handle_schema_conflict(existing_schema, inferred_schema_sql):
    print("Schema conflict detected!")
    print("Existing schema:")
    for col in existing_schema:
        print(col)
    print("\nInferred schema:")
    print(inferred_schema_sql)
    choice = input("Enter 'o' to overwrite, 'r' to rename, or 's' to skip: ")
    return choice.lower()
