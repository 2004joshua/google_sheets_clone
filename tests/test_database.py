import os
import sqlite3
import pytest
from src.database import load_csv_to_sqlite, create_table_from_csv, list_tables, execute_query, get_connection

# Remove the database file before each test to start fresh.
@pytest.fixture(autouse=True)
def clean_db():
    db_file = "database.db"
    if os.path.exists(db_file):
        os.remove(db_file)
    yield
    if os.path.exists(db_file):
        os.remove(db_file)

def test_load_csv_to_sqlite(tmp_path):
    # Create a sample CSV file
    csv_file = tmp_path / "sample.csv"
    csv_file.write_text("id,name\n1,Alice\n2,Bob")
    
    # Load CSV into SQLite using manual table creation
    load_csv_to_sqlite(str(csv_file), "test_table")
    
    # Verify the table was created and data is inserted correctly
    conn = get_connection()
    cursor = conn.cursor()
    cursor.execute("SELECT * FROM test_table")
    rows = cursor.fetchall()
    conn.close()
    assert len(rows) == 2
    assert rows[0] == (1, "Alice")
    assert rows[1] == (2, "Bob")

def test_create_table_from_csv(tmp_path):
    # Create a sample CSV file
    csv_file = tmp_path / "sample.csv"
    csv_file.write_text("id,name\n1,Alice\n2,Bob")
    
    # Create table dynamically from CSV
    create_table_from_csv(str(csv_file), "test_table_create")
    
    # Verify the table was created and data is inserted correctly
    conn = get_connection()
    cursor = conn.cursor()
    cursor.execute("SELECT * FROM test_table_create")
    rows = cursor.fetchall()
    conn.close()
    assert len(rows) == 2

def test_execute_query(tmp_path, capsys):
    # Create a sample CSV file and load it into a table
    csv_file = tmp_path / "sample.csv"
    csv_file.write_text("id,name\n1,Alice\n2,Bob")
    load_csv_to_sqlite(str(csv_file), "test_exec")
    
    # Execute a query and capture the printed output
    execute_query("SELECT * FROM test_exec;")
    captured = capsys.readouterr().out
    assert "Alice" in captured
    assert "Bob" in captured

def test_list_tables(tmp_path, capsys):
    # Create a CSV file and load it to create a table
    csv_file = tmp_path / "sample.csv"
    csv_file.write_text("id,name\n1,Alice")
    load_csv_to_sqlite(str(csv_file), "table_list")
    
    # Capture output from list_tables() to ensure it includes the created table
    list_tables()
    captured = capsys.readouterr().out
    assert "table_list" in captured
