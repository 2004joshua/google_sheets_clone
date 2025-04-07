# tests/test_csv_loader.py

import sqlite3
import pandas as pd
import tempfile
from csv_loader import load_csv_to_sqlite

def test_load_csv_to_sqlite(tmp_path):
    # Create a temporary CSV file
    csv_content = "col1,col2\n1,2\n3,4\n"
    csv_file = tmp_path / "test.csv"
    csv_file.write_text(csv_content)

    # Create a temporary SQLite database
    db_path = tmp_path / "test.db"
    conn = sqlite3.connect(str(db_path))
    
    # Load CSV into SQLite
    df, create_table_sql = load_csv_to_sqlite(str(csv_file), conn, table_name="test_table")
    
    # Verify that the table was created and data inserted
    result_df = pd.read_sql_query("SELECT * FROM test_table", conn)
    conn.close()
    
    assert len(result_df) == 2
    assert list(result_df.columns) == ["col1", "col2"]
