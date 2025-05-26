"""
----------------------------------------------------------------------------------------
DATA ACCESS OBJECT (DAO) FOR TRANSACTIONS TABLE - Investment Portfolio Management (IPM) SYSTEM
----------------------------------------------------------------------------------------
Author: Ebelechukwu Igwagu
---------------------------
This module provides the Data Access Object (DAO) for the transactions table in the IPM system.
It includes methods for creating, reading, updating, and deleting (CRUD) transactions in the investment portfolio management system.
"""

import pymysql
import sql_connect

# DAO class for handling transactions in the investment portfolio management system

class TransactionsDAO:

    def __init__(self):
        self.conn = sql_connect.connect_mysql()

    def close(self):
        if self.conn:
            self.conn.close()

    def create_transaction(self, transaction_data):
        """
        transaction_data: (user_id, stock_id, transaction_type, quantity, price_per_share)
        """
        try:
            with self.conn.cursor() as cursor:
                sql = """
                    INSERT INTO transactions (user_id, stock_id, transaction_type, quantity, price_per_share)
                    VALUES (%s, %s, %s, %s, %s)
                """
                cursor.execute(sql, transaction_data)
                self.conn.commit()
                return cursor.lastrowid
        except pymysql.MySQLError as e:
            print(f"[ERROR] create_transaction: {e}")
            self.conn.rollback()
            return None


        
    def get_transaction_by_id(self, transaction_id):
        try:
            with self.conn.cursor() as cursor:
                sql = """
                      SELECT t.transaction_id, t.stock_id, s.stock_symbol, t.transaction_type, t.quantity, t.price_per_share, t.transaction_date
                      FROM transactions t 
                      INNER JOIN stocks s 
                      ON t.stock_id = s.stock_id 
                      WHERE t.transaction_id = %s
                """
                cursor.execute(sql, (transaction_id,))
                return cursor.fetchone()
        except pymysql.MySQLError as e:
            print(f"[ERROR] get_transaction_by_id: {e}")
            return None

    def get_transactions_by_user_id(self, user_id):
        try:
            with self.conn.cursor() as cursor:
                sql ="""
                      SELECT t.transaction_id, t.user_id, t.stock_id, s.stock_symbol, t.transaction_type, t.quantity, t.price_per_share, t.transaction_date
                      FROM transactions t 
                      INNER JOIN stocks s 
                      ON t.stock_id = s.stock_id 
                      WHERE user_id = %s
                """
                cursor.execute(sql, (user_id,))
                return cursor.fetchall()
        except pymysql.MySQLError as e:
            print(f"[ERROR] get_transactions_by_user_id: {e}")
            return None
   
    def get_transactions_by_stock_id(self, stock_id):
        try:
            with self.conn.cursor() as cursor:
                sql ="""
                      SELECT t.transaction_id, t.user_id, t.stock_id, s.stock_symbol, t.transaction_type, t.quantity, t.price_per_share, t.transaction_date
                      FROM transactions t 
                      INNER JOIN stocks s 
                      ON t.stock_id = s.stock_id 
                      WHERE stock_id = %s
                """
                cursor.execute(sql, (stock_id,))
                return cursor.fetchall()
        except pymysql.MySQLError as e:
            print(f"[ERROR] get_transactions_by_stock_id: {e}")
            return None

    def update_transaction_quantity(self, transaction_id, new_quantity):
        try:
            with self.conn.cursor() as cursor:
                sql = """
                    UPDATE transactions
                    SET quantity = %s
                    WHERE transaction_id = %s
                """
                cursor.execute(sql, (new_quantity, transaction_id))
                self.conn.commit()
                return cursor.rowcount
        except pymysql.MySQLError as e:
            print(f"[ERROR] update_transaction_quantity: {e}")
            self.conn.rollback()
            return None

    def update_transaction_price(self, transaction_id, new_price):
        try:
            with self.conn.cursor() as cursor:
                sql = """
                    UPDATE transactions
                    SET price_per_share = %s
                    WHERE transaction_id = %s
                """
                cursor.execute(sql, (new_price, transaction_id))
                self.conn.commit()
                return cursor.rowcount
        except pymysql.MySQLError as e:
            print(f"[ERROR] update_transaction_price: {e}")
            self.conn.rollback()
            return None

    def delete_transaction(self, transaction_id):
        try:
            with self.conn.cursor() as cursor:
                sql = "DELETE FROM transactions WHERE transaction_id = %s"
                cursor.execute(sql, (transaction_id,))
                self.conn.commit()
                return cursor.rowcount
        except pymysql.MySQLError as e:
            print(f"[ERROR] delete_transaction: {e}")
            self.conn.rollback()
            return None
        
transactions_dao = TransactionsDAO()
