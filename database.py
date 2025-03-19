from flask import Flask
from flask_sqlalchemy import SQLAlchemy

app = Flask(__name__)

# Database configuration
app.config['SQLALCHEMY_DATABASE_URI'] = 'sqlite:///coffee_machine.db'
app.config['SQLALCHEMY_TRACK_MODIFICATIONS'] = False

db = SQLAlchemy(app)

# Define Coffee Order Model
class CoffeeOrder(db.Model):
    id = db.Column(db.Integer, primary_key=True)
    coffee_type = db.Column(db.String(50), nullable=False)
    amount_paid = db.Column(db.Integer, nullable=False)
    change_given = db.Column(db.Integer, nullable=False)
    status = db.Column(db.String(20), nullable=False, default="Completed")

# Create database and tables
with app.app_context():
    print(" Attempting to create database...")
    db.create_all()
    print(" Database created successfully!")

# Confirm script execution
if __name__ == "__main__":
    print(" database.py executed successfully!")
