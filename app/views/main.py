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

@main.route('/goods-and-categories')
def goods_and_categories():
    active_tab = 'goods_and_categories'
    products_in_store = [
        {
            "name": f"Product {i}",
            "upc": generate_unique_upc(),
            "amount": random.randint(10, 1000),
            "category": random.choice(["Fruit", "Vegetable", "Snack", "Meat & Meat Products", "Beverage", "Dairy"]),
            "price": f"${random.uniform(0.99, 50.99):.2f}"
        } for i in range(1, 26)
    ]
    products = [
        {
            "name": f"Product {i}",
            "upc": generate_unique_id(),
            "producer": f"Producer {i}",
            "characteristics": f"Characteristics {i}",
        } for i in range(1, 16)
    ]
    categories = [
        {
            "name": f"Category {i}",
            "category_id": generate_unique_id(),
        } for i in range(1, 6)
    ]
    user = {'username': 'John Doe'} 
    return render_template(
        'pages/goods_and_categories.html',
        active_tab=active_tab, 
        products_in_store=products_in_store, 
        products=products,
        categories=categories, 
        user=user
        )

@main.route('/staff-and-clients')
def staff_and_clients():
    user = {'username': 'John Doe'} 
    return render_template('pages/staff_and_clients.html', user=user)


@main.route('/login')
def login():
    user = {'username': 'John Doe'} 
    return render_template('pages/login.html', user=user)
