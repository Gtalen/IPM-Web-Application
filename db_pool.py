"""
db_pool.py
----------------------------
Author: Ebelechukwu Igwagu
----------------------------
This module sets up a MySQL connection pool using DBUtils + pymysql.
"""

from dbutils.pooled_db import PooledDB
import pymysql
from paconfig import username, password, database  # Import your DB credentials

# Create the connection pool
db_pool = PooledDB(
    creator=pymysql,
    host='Gtalen.mysql.pythonanywhere-services.com',
    user=username,
    password=password,
    database=database,
    autocommit=True,
    charset='utf8mb4',
    cursorclass=pymysql.cursors.DictCursor,
    blocking=True,
    maxconnections=10,  # Set based on your expected concurrent load
    ping=1              # Ensures stale connections are validated and replaced
)

def get_connection():
    """Get a pooled connection."""
    return db_pool.connection()
