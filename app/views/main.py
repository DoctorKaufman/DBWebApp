from flask import Blueprint, render_template
import json
import random

main = Blueprint('main', __name__)

def generate_unique_upc():
    """Generate a unique UPC code consisting of # followed by 10 random digits."""
    return "#" + "".join([str(random.randint(0, 9)) for _ in range(10)])

@main.route('/')
def home():
    user = {'username': 'John Doe'} 
    return render_template('pages/home.html', user=user)

@main.route('/goods')
def goods():
    products = [
        {
            "name": f"Product {i}",
            "upc": generate_unique_upc(),
            "amount": random.randint(10, 1000),
            "category": random.choice(["Fruit", "Vegetable", "Snack", "Meat & Meat Products", "Beverage", "Dairy"]),
            "price": f"${random.uniform(0.99, 50.99):.2f}"
        } for i in range(1, 26)
    ]
    user = {'username': 'John Doe'} 
    return render_template('pages/goods.html', products=products, user=user)

@main.route('/login')
def login():
    user = {'username': 'John Doe'} 
    return render_template('pages/login.html', user=user)
