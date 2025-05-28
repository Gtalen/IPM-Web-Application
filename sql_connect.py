
"""
SQL Connection Script
----------------------------
Author: Ebelechukwu Igwagu
----------------------------
This module handles the connection to a MySQL database and provides functions for querying and 
manipulating data using the `pymysql` library.
"""

# Import dependencies
import pymysql
from config import username, password, database  # Import database credentials from config

# initializes the variable conn to none
conn = None

# Function to connect to the database
def connect_mysql():
    global conn  # Makes conn a global variable
    try:
        # Create connection
        conn = pymysql.connect(
            host='localhost',  # MySQL host
            user=username,
            password=password,
            database=database,  # SQL database name
            cursorclass=pymysql.cursors.DictCursor #sets the cursor to the dict cursor
        )
        #print("Connection to the database is succesful.")
        return conn  # return the connection
    except pymysql.MySQLError as e:
        print(f"Error connecting to database: {e}")
        conn = None  #sets conn to none if error occurs

def main():
    connect_mysql()  # Try to connect to the database

if __name__ == "__main__":
    main()
