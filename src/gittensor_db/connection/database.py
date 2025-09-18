"""
Database connection utility for validator storage operations.
"""
import os
from typing import Optional
import bittensor as bt

try:
    import mysql.connector
    MYSQL_AVAILABLE = True
except ImportError:
    MYSQL_AVAILABLE = False
    bt.logging.warning("mysql-connector-python not installed. Database storage features will be disabled.")


def create_database_connection() -> Optional[object]:
    """
    Create a database connection using environment variables.

    Returns:
        Database connection if successful, None otherwise
    """
    if not MYSQL_AVAILABLE:
        bt.logging.error("Cannot create database connection: mysql-connector-python not installed")
        return None

    try:
        db_config = {
            'host': os.getenv('DB_HOST', 'localhost'),
            'port': int(os.getenv('DB_PORT', 3306)),
            'user': os.getenv('DB_USER', 'root'),
            'password': os.getenv('DB_PASSWORD', ''),
            'database': os.getenv('DB_NAME', 'gittensor_validator'),
            'autocommit': False,
            'charset': 'utf8mb4',
            'collation': 'utf8mb4_unicode_ci'
        }

        connection = mysql.connector.connect(**db_config)
        bt.logging.info("Successfully connected to database for validation result storage")
        return connection

    except mysql.connector.Error as e:
        bt.logging.error(f"Failed to connect to database: {e}")
        return None
    except Exception as e:
        bt.logging.error(f"Unexpected error connecting to database: {e}")
        return None


def test_database_connection() -> bool:
    """
    Test if database connection is working.

    Returns:
        True if connection successful, False otherwise
    """
    connection = create_database_connection()
    if connection:
        try:
            connection.close()
            return True
        except Exception as e:
            bt.logging.error(f"Error closing test connection: {e}")
            return False
    return False