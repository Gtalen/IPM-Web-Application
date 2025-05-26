"""
-----------------------------------
TRANSACTION DATA GENERATION SCRIPT
-----------------------------------
Author: Ebelechukwu Igwagu
-----------------------------------
This script generates random transaction data for users in the IPM
Price simulation was done using current market prices from Yahoo Screener
which was used to populate the transactions table.
"""

from datetime import datetime
import random
from faker import Faker
import pymysql
import sql_connect
import stocks_data

# Initialize Faker
fake = Faker(["en_IE", "en_US", "en_GB"])
Faker.seed(10)
def generate_transaction_data():
    stocks = stocks_data.load_stocks_json()  # Load stock data from JSON file
    conn = sql_connect.connect_mysql()  # Connect to MySQL

    if not conn:
        print("Failed to connect to the database.")
        return

    try:
        with conn.cursor() as cursor:
            # Get user IDs and creation dates
            cursor.execute("SELECT user_id, created_at FROM users ORDER BY user_id;")
            user_data = cursor.fetchall()
            user_creation_dates = {row["user_id"]: row["created_at"] for row in user_data}

            # Get stock IDs
            cursor.execute("SELECT stock_id FROM stocks ORDER BY stock_id;")
            stock_ids = [row["stock_id"] for row in cursor.fetchall()]

            # Get prices from loaded json stock data
            stock_prices = [stock.get("regularMarketPrice") for stock in stocks]
            stock_price_map = dict(zip(stock_ids, stock_prices))  # Create a mapping of stock_id to price

            transactions = []

            for user_id, created_at in user_creation_dates.items():
                num_transactions = random.randint(5, 10)  # Generate 5 to 10 transactions per user

                for _ in range(num_transactions):
                    stock_id = random.choice(stock_ids)

                    # Weighted random choice: 60% buy, 40% sell
                    transaction_type = random.choices(["buy", "sell"], weights=[0.6, 0.4])[0]

                    quantity = random.randint(1, 100)

                    # Price simulation ±30%
                    base_price = stock_price_map.get(stock_id, 100)
                    price_per_share = round(base_price * random.uniform(0.7, 1.3), 2)

                    # Generate a transaction date between account creation date and now
                    transaction_date = fake.date_time_between(
                        start_date=created_at, end_date=datetime.now()
                    )

                    # Store transaction
                    transactions.append((
                        user_id,
                        stock_id,
                        transaction_type,
                        quantity,
                        price_per_share,
                        transaction_date
                    ))

            # Insert data into the transactions table
            query = """
                INSERT INTO transactions (user_id, stock_id, transaction_type, quantity, price_per_share, transaction_date)
                VALUES (%s, %s, %s, %s, %s, %s)
            """
            cursor.executemany(query, transactions)
            conn.commit()
            print(f"Added {len(transactions)} transactions to the transaction table successfully.")

    except pymysql.MySQLError as e:
        print(f"Database error: {e}")
    finally:
        conn.close()


def main():
    generate_transaction_data()  # Call the function to generate transaction data

if __name__ == "__main__":
    main()
