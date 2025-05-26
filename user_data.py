"""
-----------------------------------------------------------------------
Data Generation for the Financial Investment Portfolio database tables
-----------------------------------------------------------------------
Author: Ebelechukwu Igwagu
--------------------------------
This script generates data using the Faker library for the user table and
data from the  stocks table.
"""

import random
import pymysql
from faker import Faker
import sql_connect
from werkzeug.security import generate_password_hash



# Initialize Faker
fake = Faker(["en_IE", "en_US", "en_GB"])
Faker.seed(10)

email_domains = ["example.com", "yahoo.com", "hotmail.com", "gmail.com", "outlook.com"]

def generate_user_data(num_users=50):
    conn = sql_connect.connect_mysql()  # Connect to MySQL
    if conn:
        try:
            users = []
            for _ in range(num_users):
                first_name = fake.unique.first_name()
                last_name = fake.unique.last_name()
                fullname = f"{first_name} {last_name}"
                username = fake.unique.user_name()
                email = f"{first_name.lower()}.{last_name.lower()}@{random.choice(email_domains)}"
                plain_password = fake.password(length=12)
                password_hash = generate_password_hash(plain_password)
                dob = fake.date_of_birth(minimum_age=18, maximum_age=70)
                created_at = fake.date_time_between(start_date='-2y', end_date='now')

                users.append((fullname, username, email, password_hash, dob, created_at))

            with conn.cursor() as cursor:
                query = """
                INSERT IGNORE INTO users (fullname, username, email, password_hash, dob, created_at)
                VALUES (%s, %s, %s, %s, %s, %s)
                """
                cursor.executemany(query, users)
                conn.commit()
                print("User data inserted successfully and duplicates were ignored.")
        except pymysql.MySQLError as e:
            print(f"Error inserting user data: {e}")
        finally:
            conn.close()
    else:
        print("Failed to connect to the database.")



def main():
    generate_user_data()  # Generate and insert user data
    
if __name__ == "__main__":
    main()

"""
---------------------------------------
References:
---------------------------------------

- DataCamp. (n.d.). *Creating Synthetic Data with Python and Faker*. [online] Available at: https://www.datacamp.com/tutorial/creating-synthetic-data-with-python-faker-tutorial [Accessed 18 May 2025].

- Faker (2025). *Using the Faker Class*. [online] Available at: https://pypi.org/project/Faker/ [Accessed 18 May 2025].

- Faker documentation. (n.d.). *Faker 37.3.0 Documentation*. [online] Available at: https://faker.readthedocs.io/en/master/fakerclass.html [Accessed 18 May 2025].
"""
