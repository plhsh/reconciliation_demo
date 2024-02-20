import pytest
from db_config import get_engine

# run "pytest tests/ from dags dir


def test_database_connection():
    try:
        engine = get_engine()
        conn = engine.connect()
        conn.close()
        assert True
    except Exception as e:
        pytest.fail(f"Database connection failed: {e}")
