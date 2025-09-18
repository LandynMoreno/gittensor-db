"""
Test configuration and fixtures
"""
import pytest
from unittest.mock import Mock
from src.gittensor_db.connection.database import create_database_connection

@pytest.fixture
def mock_db_connection():
    """Mock database connection for testing"""
    mock_conn = Mock()
    mock_cursor = Mock()
    mock_conn.cursor.return_value = mock_cursor
    return mock_conn

@pytest.fixture
def real_db_connection():
    """Real database connection for integration tests"""
    conn = create_database_connection()
    yield conn
    if conn:
        conn.close()