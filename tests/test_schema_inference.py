# tests/test_schema_inference.py
import pandas as pd
from schema_inference import infer_sqlite_schema

def test_infer_sqlite_schema():
    data = {
        "col1": [1, 2, 3],
        "col2": ["a", "b", "c"],
        "col3": [1.1, 2.2, 3.3]
    }
    df = pd.DataFrame(data)
    create_table_sql = infer_sqlite_schema(df, table_name="test_table")
    expected_sql = (
        'CREATE TABLE IF NOT EXISTS test_table ("col1" INTEGER, "col2" TEXT, "col3" REAL);'
    )
    assert create_table_sql == expected_sql
