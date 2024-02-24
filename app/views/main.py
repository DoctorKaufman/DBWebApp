from flask import Blueprint, render_template
import json
import random

main = Blueprint('main', __name__)

def generate_unique_upc():
    return "#" + "".join([str(random.randint(0, 9)) for _ in range(10)])

def generate_unique_id():
    return "#" + "".join([str(random.randint(0, 9)) for _ in range(10)])

def generate_phone_number():
    return "+380 " + " ".join(["".join([str(random.randint(0, 9)) for _ in range(3)]) for _ in range(3)])

@main.route('/')
def home():
    user = {'username': 'John Doe'} 
    return render_template('pages/home.html', user=user)

@main.route('/goods')
def goods():
    categories = ["Fruit", "Vegetable", "Snack", "Meat & Meat Products", "Beverage", "Dairy"]
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
    return render_template('pages/goods.html', categories=categories, products=products, user=user)

@main.route('/workers')
def workers():
    positions = ["Manager", "Cashier", "Cleaner", "Consultant", "Security"]
    workers = [
        {
            "name": f"Worker {i}",
            "id": generate_unique_id(),
            "position": random.choice(["Manager", "Cashier", "Cleaner", "Consultant", "Security"]),
            "salary": f"${random.uniform(500, 900):.0f}",
            "employment_date": f"2021-{random.randint(10, 12)}-{random.randint(10, 28)}",
            "birth_date": f"{random.randint(1980, 2005)}-{random.randint(10, 12)}-{random.randint(10, 28)}",
            "phone_number": generate_phone_number(),
            "address": f"City, Street, {random.randint(1, 100)}",
        } for i in range(1, 13)
    ]
    user = {'username': 'John Doe'} 
    return render_template('pages/workers.html', positions=positions, workers=workers, user=user)


@main.route('/login')
def login():
    user = {'username': 'John Doe'} 
    return render_template('pages/login.html', user=user)
