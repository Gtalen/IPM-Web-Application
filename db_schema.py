"""
---------------------------------------------------------------
Database Schema for the Investment Portfolio Management System
---------------------------------------------------------------
Author: Ebelechukwu Igwagu
---------------------------------------------------------------
This module defines the database schema for the Investment Portfolio Management System.
"""

# Import necessary libraries
import pymysql
import sql_connect

# Function to create the database schema

def create_database_schema():
    conn = sql_connect.connect_mysql()  # Connect to MySQL
    if conn:
        try:
            with conn.cursor() as cursor:
                # Create database if it doesn't exist
                query = "CREATE DATABASE IF NOT EXISTS investment_portfolio_db;"
                cursor.execute(query)
                print("Database created successfully.")
            
            conn.commit()
        except pymysql.MySQLError as e:
            print(f"Error creating database: {e}")
        finally:
            conn.close()
    else:
        print("Failed to connect to the database.")


# Function to create the Users table
def create_users_table():
    conn = sql_connect.connect_mysql()  # Connect to MySQL
    if conn:
        try:
            with conn.cursor() as cursor:
                query = """
                CREATE TABLE IF NOT EXISTS users (
                    user_id INT AUTO_INCREMENT PRIMARY KEY,
                    fullname VARCHAR(255) NOT NULL,
                    username VARCHAR(100) NOT NULL UNIQUE,
                    email VARCHAR(255) NOT NULL UNIQUE,
                    password_hash VARCHAR(255) NOT NULL,
                    dob DATE NOT NULL,
                    created_at DATETIME NOT NULL DEFAULT CURRENT_TIMESTAMP
                );
                """
                cursor.execute(query)
                print("Users table created successfully.")
            
            conn.commit()
        except pymysql.MySQLError as e:
            print(f"Error creating Users table: {e}")
        finally:
            conn.close()
    else:
        print("Failed to connect to the database.")


# Function to create the Stocks table
def create_stocks_table():
    conn = sql_connect.connect_mysql()
    if conn:
        try:
            with conn.cursor() as cursor:  # You missed () after conn.cursor
               query = """
                CREATE TABLE IF NOT EXISTS stocks (
                    stock_id INT AUTO_INCREMENT PRIMARY KEY,
                    stock_symbol VARCHAR(50) NOT NULL UNIQUE,
                    stock_short_name VARCHAR(255) NOT NULL,
                    stock_company_name VARCHAR(255) NOT NULL
                );
                """
               cursor.execute(query)
               print("Stocks table created successfully.")
            conn.commit()
        except pymysql.MySQLError as e:
            print(f"Error creating stocks table: {e}")
        finally:
            conn.close()
    else:
        print("Failed to connect to the database.")



# Function to create the Transactions table
def create_table_transactions():
    conn = sql_connect.connect_mysql()
    if conn:
        try:
            with conn.cursor() as cursor:  # ← FIXED: Added parentheses
                query = """
                CREATE TABLE IF NOT EXISTS transactions (
                    transaction_id INT AUTO_INCREMENT PRIMARY KEY,
                    user_id INT NOT NULL,
                    stock_id INT NOT NULL,
                    transaction_type ENUM('buy', 'sell') NOT NULL,
                    quantity INT NOT NULL,
                    price_per_share DECIMAL(10, 2) NOT NULL,
                    transaction_date DATETIME NOT NULL DEFAULT CURRENT_TIMESTAMP,
                    FOREIGN KEY (user_id) REFERENCES users(user_id),
                    FOREIGN KEY (stock_id) REFERENCES stocks(stock_id)
                );
                """
                cursor.execute(query)
                print("Transactions table created successfully.")
            conn.commit()
        except pymysql.MySQLError as e:  # ← FIXED: Typo in Exception Name
            print(f"Error creating transactions table: {e}")
        finally:
            conn.close()
    else:
        print("Failed to connect to the database.")


def main():
    create_database_schema()  # Call your schema creation function
    create_users_table()  # Call the function to create the Users table
    create_stocks_table()  # Call the function to create the stocks table
    create_table_transactions()  # Call the function to create the transactions table
if __name__ == "__main__":
    main()
