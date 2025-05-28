"""
----------------------------------------------------------------------------------------
DATA ACCESS OBJECT (DAO) FOR USERS TABLE - Investment Portfolio Management (IPM) SYSTEM
----------------------------------------------------------------------------------------
Author: Ebelechukwu Igwagu
---------------------------
This module provides the Data Access Object (DAO) for the Users table in the IPM system.
It includes methods for creating, reading, updating, and deleting (CRUD) user records in 
the investment portfolio management system.
"""

from db_pool import get_connection  # Updated to use pooled connection
import pymysql
from werkzeug.security import generate_password_hash

class UsersDAO:
    def __init__(self):
        self.conn = get_connection()

    def ensure_connection(self):
        """Reconnect if the connection has gone away."""
        try:
            self.conn.ping(reconnect=True)
        except Exception:
            self.conn = get_connection()

    def close(self):
        if self.conn:
            self.conn.close()

    def create_user(self, user_data):
        """
        user_data: dict containing keys
        ('fullname', 'username', 'email', 'password_hash', 'dob')
        """
        self.ensure_connection()
        try:
            with self.conn.cursor() as cursor:
                sql = """
                    INSERT INTO users (fullname, username, email, password_hash, dob)
                    VALUES (%s, %s, %s, %s, %s)
                """
                cursor.execute(sql, (
                    user_data["fullname"],
                    user_data["username"],
                    user_data["email"],
                    user_data["password_hash"],
                    user_data["dob"],
                ))
                self.conn.commit()
                return cursor.lastrowid
        except pymysql.MySQLError as e:
            print(f"[ERROR] create_user: {e}")
            self.conn.rollback()
            return None

    def get_all_users(self):
        self.ensure_connection()
        try:
            with self.conn.cursor() as cursor:
                sql = """
                    SELECT user_id, fullname, username, email, dob, created_at
                    FROM users
                """
                cursor.execute(sql)
                return cursor.fetchall()
        except pymysql.MySQLError as e:
            print(f"[ERROR] get_all_users: {e}")
            return None 

    def get_user_by_id(self, user_id):
        self.ensure_connection()
        try:
            with self.conn.cursor() as cursor:
                sql = """
                    SELECT fullname, username, email, dob, created_at
                    FROM users
                    WHERE user_id = %s
                """
                cursor.execute(sql, (user_id,))
                return cursor.fetchone()
        except pymysql.MySQLError as e:
            print(f"[ERROR] get_user_by_id: {e}")
            return None

    def get_user_by_email(self, email):
        self.ensure_connection()
        try:
            with self.conn.cursor() as cursor:
                sql = """
                    SELECT fullname, username, email, dob, created_at
                    FROM users
                    WHERE email = %s
                """
                cursor.execute(sql, (email,))
                return cursor.fetchone()
        except pymysql.MySQLError as e:
            print(f"[ERROR] get_user_by_email: {e}")
            return None

    def update_user_password(self, username, email, new_password):
        self.ensure_connection()
        try:
            with self.conn.cursor() as cursor:
                sql = """
                    UPDATE users
                    SET password_hash = %s
                    WHERE username = %s AND email = %s
                """
                hashed_password = generate_password_hash(new_password)
                cursor.execute(sql, (hashed_password, username, email))
                self.conn.commit()
                return cursor.rowcount
        except pymysql.MySQLError as e:
            print(f"[ERROR] update_user_password: {e}")
            self.conn.rollback()
            return None

    def delete_user(self, user_id):
        self.ensure_connection()
        try:
            with self.conn.cursor() as cursor:
                sql = """
                    DELETE FROM users
                    WHERE user_id = %s
                """
                cursor.execute(sql, (user_id,))
                self.conn.commit()
                return cursor.rowcount
        except pymysql.MySQLError as e:
            print(f"[ERROR] delete_user: {e}")
            self.conn.rollback()
            return None

# Instantiate DAO
users_dao = UsersDAO()
