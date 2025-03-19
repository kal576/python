from flask import Flask, request, jsonify

app = Flask(__name__)

menu = {
    "latte": {"ingredients": {"water": 20, "milk": 10, "coffee": 10}, "cost": 250},
    "espresso": {"ingredients": {"water": 10, "coffee": 10}, "cost": 200},
    "cappuccino": {"ingredients": {"water": 20, "milk": 15, "coffee": 10}, "cost": 300},
}

profit = 0
resources = {"water": 5000, "milk": 2000, "coffee": 1000}

def check_resources(ordered_ingredients):
    for item in ordered_ingredients:
        if ordered_ingredients[item] > resources[item]:
            return False, f"Sorry, not enough {item}."
    return True, ""

def process_payment(money_received, coffee_cost):
    global profit
    if money_received >= coffee_cost:
        profit += coffee_cost
        change = money_received - coffee_cost
        return True, change
    return False, 0

def make_coffee(coffee_name, coffee_ingredients):
    for item in coffee_ingredients:
        resources[item] -= coffee_ingredients[item]
    return f"Here is your {coffee_name}. Enjoy! ☕"

@app.route("/menu", methods=["GET"])
def get_menu():
    return jsonify(menu)

@app.route("/order", methods=["POST"])
def order_coffee():
    data = request.json
    coffee_type = data.get("coffee")
    money_inserted = data.get("money")
    
    if coffee_type not in menu:
        return jsonify({"error": "Invalid coffee type."}), 400
    
    coffee_details = menu[coffee_type]
    enough_resources, message = check_resources(coffee_details["ingredients"])
    if not enough_resources:
        return jsonify({"error": message}), 400
    
    success, change = process_payment(money_inserted, coffee_details["cost"])
    if not success:
        return jsonify({"error": "Not enough money. Money refunded."}), 400
    
    coffee_message = make_coffee(coffee_type, coffee_details["ingredients"])
    return jsonify({"message": coffee_message, "change": change})

if __name__ == "__main__":
    app.run(debug=True)
