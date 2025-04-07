# database.py

import sqlite3
import pandas as pd

def get_connection(db_file):
    """Connect to the SQLite database and return the connection."""
    conn = sqlite3.connect(db_file)
    return conn

def execute_query(conn, query):
    """Execute a SQL query and return results as a DataFrame."""
    return pd.read_sql_query(query, conn)

def list_tables(conn):
    """List all tables in the SQLite database."""
    query = "SELECT name FROM sqlite_master WHERE type='table';"
    df = pd.read_sql_query(query, conn)
    return df['name'].tolist()
