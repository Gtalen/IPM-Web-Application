"""
----------------------------------------------------------------------------------------
DATA ACCESS OBJECT (DAO) FOR USERS TABLE - Investment Portfolio Management (IPM) SYSTEM
----------------------------------------------------------------------------------------
Author: Ebelechukwu Igwagu
---------------------------
This module provides the Data Access Object (DAO) for the Users table in the IPM system.
It includes methods for creating, reading, updating, and deleting (CRUD) user records in the investment portfolio management system.
"""

import pymysql
import sql_connect # Connect to MySQL database
from werkzeug.security import generate_password_hash

class UsersDAO:
    def __init__(self):
        self.conn = sql_connect.connect_mysql()

    def close(self):
        if self.conn:
            self.conn.close()

    def create_user(self, user_data):
        """
        user_data: dict containing keys
        ('fullname', 'username', 'email', 'password_hash', 'dob')
        """
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
                return cursor.rowcount  # number of rows updated
        except pymysql.MySQLError as e:
            print(f"[ERROR] update_user_password: {e}")
            self.conn.rollback()
            return None


        
        
    def delete_user(self, user_id):
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

users_dao = UsersDAO()



"""
#  References:
- Amos, D. (2024) Object-Oriented Programming (OOP) in Python. https://realpython.com/python3-object-oriented-programming/.
"""