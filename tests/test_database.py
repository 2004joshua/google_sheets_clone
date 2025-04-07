# tests/test_database.py
import sqlite3
import pandas as pd
import tempfile
from database import connect_db, execute_query, list_tables

def test_connect_db(tmp_path):
    db_file = tmp_path / "test.db"
    conn = connect_db(str(db_file))
    assert conn is not None
    conn.close()

def test_execute_and_list_tables(tmp_path):
    db_file = tmp_path / "test.db"
    conn = connect_db(str(db_file))
    cursor = conn.cursor()
    cursor.execute("CREATE TABLE test (id INTEGER PRIMARY KEY, name TEXT);")
    conn.commit()
    
    # Test execute_query: table should be empty
    df = execute_query(conn, "SELECT * FROM test;")
    assert df.empty
    
    # Test list_tables
    tables = list_tables(conn)
    assert "test" in tables
    conn.close()
