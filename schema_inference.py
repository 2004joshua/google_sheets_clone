# schema_inference.py

def infer_sqlite_schema(df, table_name):
    """
    Infer the SQLite schema from a DataFrame and return a CREATE TABLE SQL statement.
    """
    type_mapping = {
        'object': 'TEXT',
        'int64': 'INTEGER',
        'float64': 'REAL',
        'bool': 'INTEGER',  # SQLite does not have a native Boolean type.
        'datetime64[ns]': 'TEXT'
    }
    schema_parts = []
    for col, dtype in df.dtypes.iteritems():
        sqlite_type = type_mapping.get(str(dtype), 'TEXT')
        schema_parts.append(f'"{col}" {sqlite_type}')
    schema = ", ".join(schema_parts)
    create_table_sql = f"CREATE TABLE IF NOT EXISTS {table_name} ({schema});"
    return create_table_sql
