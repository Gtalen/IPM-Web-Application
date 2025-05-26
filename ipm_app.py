"""
---------------------------------------------------
INVESTMENT PORTFOLIO MANAGEMENT APPLICATION SERVER
---------------------------------------------------
Author: Ebelechukwu Igwagu
------------------------------------
This module sets up the Flask application for the Investment Portfolio Management System (IPM).
It includes routes for user management, stock management, and transaction management.
"""

from flask import Flask, request, jsonify, render_template
from flask_cors import CORS
from users_dao import UsersDAO
from stocks_dao import StocksDAO
from transactions_dao import TransactionsDAO
from werkzeug.security import generate_password_hash


app = Flask(__name__)
CORS(app) # Enable CORS for all routes
#CORS(app, resources={r"/api/*": {"origins": "*"}}, supports_credentials=True)


users_dao = UsersDAO()
stocks_dao = StocksDAO()
transactions_dao = TransactionsDAO()

# curl http://127.0.0.1:5000/
@app.route("/", methods=['GET'])
def home():
    return render_template("ipm_base.html")



# USER ROUTES

@app.route("/user", methods=['GET'])
def user():
    return render_template("ipm_user.html")

# Get all users
# curl "http://127.0.0.1:5000/api/users"
@app.route("/api/users", methods=["GET"])
def get_all_users():
    users = users_dao.get_all_users()
    if users is None:
        return jsonify({"error": "Failed to fetch users"}), 500
    return jsonify(users), 200

# Get user by ID
# curl "http://127.0.0.1:5000/api/users/1"
@app.route("/api/users/<int:user_id>", methods=["GET"])
def get_user_by_id(user_id):
    user = users_dao.get_user_by_id(user_id)
    if user is None:
        return jsonify({"error": "User not found"}), 404
    return jsonify(user), 200

# Get User by email
# curl "http://127.0.0.1:5000/api/users/email?email=ryan.olson@hotmail.com"
@app.route("/api/users/email", methods=["GET"])
def get_user_by_email():
    email = request.args.get("email")
    if not email:
        return jsonify({"error": "Missing email"}), 400
    user = users_dao.get_user_by_email(email)
    if user is None:
        return jsonify({"error": "User not found"}), 404
    return jsonify(user), 200


# Create new user

@app.route("/api/users/new-user", methods=["GET", "POST"])
def create_user():
    if request.method == 'POST':
        firstname = request.form.get('firstname')
        lastname = request.form.get('lastname')
        fullname = f"{firstname} {lastname}"
        username = request.form.get('username')
        password = request.form.get('password')
        email = request.form.get('email')
        dob = request.form.get('dob')

        if not password:
            return jsonify({"message": "Error: Password is required."}), 400

        password_hash = generate_password_hash(password)

        user_data = {
            "fullname": fullname,
            "username": username,
            "email": email,
            "password_hash": password_hash,
            "dob": dob
        }

        new_user_id = users_dao.create_user(user_data)
        if new_user_id is None:
            return jsonify({"message": "Error: Could not create user."}), 500

        return jsonify({"message": "User account created successfully!"}), 200

    # For GET requests, render the form page
    return render_template("ipm_user.html")


# update user
# curl -i -H "Content-Type: application/json" -X PUT -d '{"email": "jowen@hotmail.com", "new_password": "SuperSecure456"}' http://127.0.0.1:5000/api/users/reset_password
@app.route("/api/users/reset_password", methods=["PUT"])
def reset_password():
    data = request.json

    if not data:
        return jsonify({"error": "Missing JSON data"}), 400

    username = data.get("username")
    email = data.get("email")
    new_password = data.get("new_password")

    if not all([username, email, new_password]):
        return jsonify({"error": "Missing required fields"}), 400

    updated = users_dao.update_user_password(username, email, new_password)

    if updated:
        return jsonify({"message": "Password updated successfully"}), 200
    else:
        return jsonify({"error": "User not found or update failed"}), 404

# Delete user
# curl -i -X DELETE http://127.0.0.1:5000/api/users/1
@app.route("/api/users/<int:user_id>", methods=["DELETE"])
def delete_user(user_id):
    if not user_id:
        return jsonify({"error": "Missing user ID"}), 400

    deleted = users_dao.delete_user(user_id)
    if deleted:
        return jsonify({"message": "User deleted successfully"}), 200
    else:
        return jsonify({"error": "User not found or could not be deleted"}), 404


# STOCK ROUTES

# Render stocks
@app.route("/stocks", methods=['GET'])
def stocks():
    return render_template("ipm_stock.html")

# Create a new stock
# curl -X POST http://127.0.0.1:5000/api/stocks -H "Content-Type: application/json" -d '{"stock_symbol": "BIRG", "stock_short_name": "BOI BIRG", "stock_company_name": "BANK OF IRELAND GP"}'
@app.route("/api/stocks", methods=["POST"])
def create_stock():
    data = request.get_json()
    required_fields = ["stock_symbol", "stock_short_name", "stock_company_name"]

    if not all(field in data for field in required_fields):
        return jsonify({"error": "Missing stock fields"}), 400

    stock_data = (
        data["stock_symbol"],
        data["stock_short_name"],
        data["stock_company_name"],
    )
    stock_id = stocks_dao.create_stock(stock_data)

    if stock_id is None:
        return jsonify({"error": "Failed to create stock"}), 500

    return jsonify({"stock_id": stock_id}), 201


# Read a stock by ID
# curl http://127.0.0.1:5000/api/stocks/1
@app.route("/api/stocks/<int:stock_id>", methods=["GET"])
def get_stock_by_id(stock_id):
    stock = stocks_dao.get_stock_by_id(stock_id)
    if not stock:
        return jsonify({"error": "Stock not found"}), 404
    return jsonify(stock)


# Read a stock by symbol
# curl http://127.0.0.1:5000/api/stocks/symbol/AAPL
@app.route("/api/stocks/symbol/<string:symbol>", methods=["GET"])
def get_stock_by_symbol(symbol):
    stock = stocks_dao.get_stock_by_symbol(symbol)
    if not stock:
        return jsonify({"error": "Stock not found"}), 404
    return jsonify(stock)


# Get all stocks
# curl -X GET http://localhost:5000/api/stocks
@app.route("/api/stocks", methods=["GET"])
def list_all_stocks():
    stocks = stocks_dao.list_all_stocks()
    return jsonify(stocks)

# Get user stock holding
# curl "http://127.0.0.1:5000/api/user_stock_holding?user_id=1&stock_id=2"
@app.route("/api/user_stock_holding", methods=["GET"])
def get_user_stock_holding():
    user_id = request.args.get("user_id", type=int)
    stock_id = request.args.get("stock_id", type=int)

    if user_id is None or stock_id is None:
        return jsonify({"error": "Missing user_id or stock_id"}), 400

    quantity = stocks_dao.get_user_stock_holding(user_id, stock_id)
    return jsonify({"holding": quantity})

# Update a stock
# curl -X PUT http:///127.0.0.1:5000/api/stocks/1
@app.route("/api/stocks/<int:stock_id>", methods=["PUT"])
def update_stock(stock_id):
    data = request.get_json()
    if not data:
        return jsonify({"error": "Missing required stock data"}), 400

    updated = stocks_dao.update_stock(stock_id, (
        data["stock_symbol"],
        data["stock_short_name"],
        data["stock_company_name"]
    ))
    
    if not updated:
        return jsonify({"error": "Stock not found or could not be updated"}), 404

    return jsonify({"message": "Stock updated successfully"}), 200


# Delete a stock by ID
# curl -X DELETE http://127.0.0.1:5000/api/stocks/51
@app.route("/api/stocks/<int:stock_id>", methods=["DELETE"])
def delete_stock(stock_id):
    deleted = stocks_dao.delete_stock(stock_id)
    if deleted:
        return jsonify({"message": "Stock deleted successfully"}), 200
    else:
        return jsonify({"error": "Stock not found or could not be deleted"}), 404


# TRANSACTION ROUTES

# Render transaction form
@app.route("/transactions", methods=['GET'])
def transactions():
    return render_template("ipm_transaction.html")

# Create transaction
# curl curl -X POST http://127.0.0.1:5000/api/transactions -H "Content-Type: application/json" -d '{"user_id":1,"stock_id":2,"transaction_type":"buy","quantity":10,"price_per_share":150.50}'

@app.route("/api/transactions", methods=["POST"])
def create_transaction():
    if not request.json:
        return jsonify({"error": "Invalid input"}), 400
    
    data = request.json
    user_id = data.get("user_id")
    stock_id = data.get("stock_id")
    transaction_type = data.get("transaction_type")
    quantity = data.get("quantity")
    price_per_share = data.get("price_per_share")

    if transaction_type == 'sell':
        current_qty = stocks_dao.get_user_stock_holding(user_id, stock_id)
        if quantity > current_qty:
            return jsonify({"error": "Insufficient shares to sell"}), 400

    transaction_data = (
        user_id,
        stock_id,
        transaction_type,
        quantity,
        price_per_share
    )
    new_id = transactions_dao.create_transaction(transaction_data)
    if new_id:
        return jsonify({"message": "Transaction created", "transaction_id": new_id}), 201
    return jsonify({"error": "Failed to create transaction"}), 500

# Get transaction by ID
# curl http://127.0.0.1:5000/api/transactions/1
@app.route("/api/transactions/<int:transaction_id>", methods=["GET"])
def get_transaction(transaction_id):
    tx = transactions_dao.get_transaction_by_id(transaction_id)
    if tx:
        return jsonify(tx)
    return jsonify({"error": "Transaction not found"}), 404

# Get transactions by user ID
# curl http://127.0.0.1:5000/api/transactions/user/1
@app.route("/api/transactions/user/<int:user_id>", methods=["GET"])
def get_transactions_by_user(user_id):
    transactions = transactions_dao.get_transactions_by_user_id(user_id)
    if transactions is None:
        return jsonify({"error": "Database error occurred"}), 500
    return jsonify(transactions)

# Get transactions by stock ID
# curl http://127.0.0.1:5000/api/transactions/stock/2
@app.route("/api/transactions/stock/<int:stock_id>", methods=["GET"])
def get_transactions_by_stock(stock_id):
    transactions = transactions_dao.get_transactions_by_stock_id(stock_id)
    return jsonify(transactions)

# Update transaction quantity
# curl -X PUT http://127.0.0.1:5000/api/transactions/1/quantity -H "Content-Type: application/json" -d '{"quantity":20}'
@app.route("/api/transactions/<int:transaction_id>/quantity", methods=["PUT"])
def update_quantity(transaction_id):
    data = request.json
    new_quantity = data.get("quantity")
    updated = transactions_dao.update_transaction_quantity(transaction_id, new_quantity)
    return jsonify({"updated": updated})

#  Update transaction price
# PUT http://127.0.0.1:5000/api/transactions/1/price
@app.route("/api/transactions/<int:transaction_id>/price", methods=["PUT"])
def update_price(transaction_id):
    data = request.json
    new_price = data.get("price_per_share")
    updated = transactions_dao.update_transaction_price(transaction_id, new_price)
    return jsonify({"updated": updated})

# Delete transaction
# curl -X DELETE http://127.0.0.1:5000/api/transactions/1
@app.route("/api/transactions/<int:transaction_id>", methods=["DELETE"])
def delete_transaction(transaction_id):
    deleted = transactions_dao.delete_transaction(transaction_id)
    return jsonify({"deleted": deleted})


if __name__ == "__main__":
    app.run(debug=True)