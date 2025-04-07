# tests/test_database.py

import sqlite3
import pandas as pd
from database import get_connection, execute_query, list_tables

def test_get_connection(tmp_path):
    db_file = tmp_path / "test.db"
    conn = get_connection(str(db_file))
    conn.execute("CREATE TABLE test (id INTEGER);")
    conn.commit()
    result = conn.execute("SELECT name FROM sqlite_master WHERE type='table';").fetchall()
    conn.close()
    assert ("test",) in result

def test_execute_query(tmp_path):
    db_file = tmp_path / "test.db"
    conn = get_connection(str(db_file))
    conn.execute("CREATE TABLE test (id INTEGER, value TEXT);")
    conn.execute("INSERT INTO test (id, value) VALUES (1, 'a'), (2, 'b');")
    conn.commit()
    df = execute_query(conn, "SELECT * FROM test;")
    conn.close()
    assert len(df) == 2
    assert list(df.columns) == ["id", "value"]

def test_list_tables(tmp_path):
    db_file = tmp_path / "test.db"
    conn = get_connection(str(db_file))
    conn.execute("CREATE TABLE test1 (id INTEGER);")
    conn.execute("CREATE TABLE test2 (id INTEGER);")
    conn.commit()
    tables = list_tables(conn)
    conn.close()
    assert "test1" in tables
    assert "test2" in tables
