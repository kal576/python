from flask import Flask, jsonify, request, render_template
from flask_cors import CORS
from database import db, CoffeeOrder, init_db  # Import database functions

app = Flask(__name__)
CORS(app)

# Database Configuration
app.config['SQLALCHEMY_DATABASE_URI'] = 'sqlite:///coffee_machine.db'
app.config['SQLALCHEMY_TRACK_MODIFICATIONS'] = False

# Initialize database
init_db(app)

# Coffee Menu
menu = {
    "latte": {"ingredients": {"water": 20, "milk": 10, "coffee": 10}, "cost": 250},
    "espresso": {"ingredients": {"water": 10, "coffee": 10}, "cost": 200},
    "cappuccino": {"ingredients": {"water": 20, "milk": 15, "coffee": 10}, "cost": 300}
}

resources = {"water": 5000, "milk": 2000, "coffee": 1000}
profit = 0

# Route to serve frontend
@app.route('/')
def home():
    return render_template("index.html")

# Order Processing Route
@app.route('/order', methods=['POST'])
def process_order():
    data = request.json
    coffee_type = data.get('coffee_type')
    amount_paid = data.get('amount_paid')

    if coffee_type not in menu:
        return jsonify({"error": "Invalid coffee type"}), 400

    coffee_cost = menu[coffee_type]["cost"]

    if amount_paid < coffee_cost:
        return jsonify({"error": "Insufficient funds"}), 400

    change = amount_paid - coffee_cost

    # Deduct Resources
    for item, amount in menu[coffee_type]["ingredients"].items():
        if resources[item] < amount:
            return jsonify({"error": f"Sorry, not enough {item}."}), 400
        resources[item] -= amount

    # Save order in database
    new_order = CoffeeOrder(coffee_type=coffee_type, amount_paid=amount_paid, change_given=change)
    db.session.add(new_order)
    db.session.commit()

    return jsonify({"message": f"Enjoy your {coffee_type}!", "change": change})

# Fetch Order History
@app.route('/orders', methods=['GET'])
def get_orders():
    orders = CoffeeOrder.query.all()
    return jsonify([
        {"id": order.id, "coffee_type": order.coffee_type, "amount_paid": order.amount_paid, "change_given": order.change_given, "status": order.status}
        for order in orders
    ])

# Get Resources Report
@app.route('/report', methods=['GET'])
def get_report():
    return jsonify({
        "water": resources["water"],
        "milk": resources["milk"],
        "coffee": resources["coffee"],
        "profit": profit
    })

if __name__ == '__main__':
    app.run(debug=True)
