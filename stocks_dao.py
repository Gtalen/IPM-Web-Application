"""
----------------------------------------------------------------------------------------
DATA ACCESS OBJECT (DAO) FOR STOCKS TABLE - Investment Portfolio Management (IPM) SYSTEM
----------------------------------------------------------------------------------------
Author: Ebelechukwu Igwagu
---------------------------
This module provides the Data Access Object (DAO) for the Stocks table in the IPM system.
It includes methods for creating, reading, updating, and deleting (CRUD) stock records 
in the investment portfolio management system.
"""

from db_pool import get_connection  # Updated to use pooled connection
import pymysql

class StocksDAO:
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

    def create_stock(self, stock_data):
        """
        stock_data: (stock_symbol, stock_short_name, stock_company_name)
        """
        self.ensure_connection()
        try:
            with self.conn.cursor() as cursor:
                sql = """
                    INSERT IGNORE INTO stocks (stock_symbol, stock_short_name, stock_company_name)
                    VALUES (%s, %s, %s)
                """
                cursor.execute(sql, stock_data)
                self.conn.commit()
                return cursor.lastrowid
        except pymysql.MySQLError as e:
            print(f"[ERROR] create_stock: {e}")
            self.conn.rollback()
            return None

    def get_stock_by_id(self, stock_id):
        self.ensure_connection()
        try:
            with self.conn.cursor() as cursor:
                sql = "SELECT * FROM stocks WHERE stock_id = %s"
                cursor.execute(sql, (stock_id,))
                return cursor.fetchone()
        except pymysql.MySQLError as e:
            print(f"[ERROR] get_stock_by_id: {e}")
            return None

    def get_stock_by_symbol(self, symbol):
        self.ensure_connection()
        try:
            with self.conn.cursor() as cursor:
                sql = "SELECT * FROM stocks WHERE stock_symbol = %s"
                cursor.execute(sql, (symbol,))
                return cursor.fetchone()
        except pymysql.MySQLError as e:
            print(f"[ERROR] get_stock_by_symbol: {e}")
            return None

    def update_stock(self, stock_id, stock_data):
        self.ensure_connection()
        try:
            with self.conn.cursor() as cursor:
                sql = """
                    UPDATE stocks
                    SET stock_symbol = %s,
                        stock_short_name = %s,
                        stock_company_name = %s
                    WHERE stock_id = %s
                """
                cursor.execute(sql, (*stock_data, stock_id))
                self.conn.commit()
                return cursor.rowcount > 0
        except pymysql.MySQLError as e:
            print(f"[ERROR] update_stock: {e}")
            self.conn.rollback()
            return False

    def delete_stock(self, stock_id):
        self.ensure_connection()
        try:
            with self.conn.cursor() as cursor:
                sql = "DELETE FROM stocks WHERE stock_id = %s"
                cursor.execute(sql, (stock_id,))
                self.conn.commit()
                return cursor.rowcount
        except pymysql.MySQLError as e:
            print(f"[ERROR] delete_stock: {e}")
            self.conn.rollback()
            return None

    def list_all_stocks(self):
        self.ensure_connection()
        try:
            with self.conn.cursor() as cursor:
                sql = """
                    SELECT s.stock_id, s.stock_symbol, s.stock_short_name, s.stock_company_name,
                           (SELECT t.price_per_share
                            FROM transactions t
                            WHERE t.stock_id = s.stock_id
                            ORDER BY t.transaction_date DESC
                            LIMIT 1) AS price_per_share
                    FROM stocks s
                """
                cursor.execute(sql)
                return cursor.fetchall()
        except pymysql.MySQLError as e:
            print(f"[ERROR] list_all_stocks: {e}")
            return []

    def get_user_stock_holding(self, user_id, stock_id):
        self.ensure_connection()
        try:
            with self.conn.cursor() as cursor:
                sql = """
                    SELECT 
                        COALESCE(SUM(CASE 
                            WHEN transaction_type = 'buy' THEN quantity 
                            WHEN transaction_type = 'sell' THEN -quantity
                            ELSE 0
                        END), 0) AS current_quantity
                    FROM transactions
                    WHERE user_id = %s AND stock_id = %s
                """
                cursor.execute(sql, (user_id, stock_id))
                result = cursor.fetchone()
                return result['current_quantity'] if result else 0
        except pymysql.MySQLError as e:
            print(f"[ERROR] get_user_stock_holding: {e}")
            return 0

# Instantiate DAO
stocks_dao = StocksDAO()
