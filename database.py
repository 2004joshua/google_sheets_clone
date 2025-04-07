# database.py
import sqlite3
import pandas as pd
import logging

def connect_db(db_path="database.db"):
    try:
        conn = sqlite3.connect(db_path)
        return conn
    except Exception as e:
        logging.error(f"Error connecting to database: {e}")
        raise

def execute_query(conn, query):
    try:
        df = pd.read_sql_query(query, conn)
        return df
    except Exception as e:
        logging.error(f"Error executing query '{query}': {e}")
        raise

def list_tables(conn):
    try:
        query = "SELECT name FROM sqlite_master WHERE type='table';"
        df = pd.read_sql_query(query, conn)
        return df['name'].tolist()
    except Exception as e:
        logging.error(f"Error listing tables: {e}")
        raise
