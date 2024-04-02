from app.views.main import generate_unique_id, generate_unique_upc
from flask import Blueprint, render_template
import json
import random
import requests


goods_and_categories = Blueprint('goods_and_categories', __name__)


@goods_and_categories.route('/goods-in-store')
def goods_in_store():
    active_tab = 'goods_in_store'
    categories = ["Fruit", "Vegetable", "Snack", "Meat & Meat products", "Beverage", "Dairy"]
    columns = {
        "name": True,
        "upc": False,
        "amount": True,
        "category": True,
        "price": True,
    }
    columns_json = json.dumps(columns)
    items = [
        {
            "name": f"Product {i}",
            "upc": generate_unique_upc(),
            "amount": random.randint(10, 1000),
            "category": random.choice(["Fruit", "Vegetable", "Snack", "Meat & Meat products", "Beverage", "Dairy"]),
            "price": f"${random.uniform(0.99, 50.99):.2f}"
        } for i in range(1, 26)
    ]
    user = {'username': 'John Doe'} 
    return render_template('pages/goods_and_categories.html',
                           categories=categories, active_tab=active_tab, items=items, columns=columns, columns_json=columns_json, user=user)


@goods_and_categories.route('/goods')
def goods():
    active_tab = 'goods'
    columns = {
    "name": True,
    "ID": False,
    "producer": True,
    "characteristics": True,
    }
    columns_json = json.dumps(columns)
    items = [
        {
            "name": f"Product {i}",
            "ID": generate_unique_id(),
            "producer": f"Producer {i}",
            "characteristics": f"Characteristics {i}",
        } for i in range(1, 16)
    ]
    user = {'username': 'John Doe'} 
    return render_template('pages/goods_and_categories.html',
                           active_tab=active_tab, items=items, columns=columns, columns_json=columns_json, user=user)


@goods_and_categories.route('/categories')
def categories():
    active_tab = 'categories'
    user = {'username': 'John Doe'}
    columns = requests.get('http://127.0.0.1:5000/category/columns')
    data = requests.get('http://127.0.0.1:5000/category/')

    if data.status_code == 200 & columns.status_code == 200:
        items = data.json()
        columns = columns.json()
        columns_json = json.dumps(columns)
        return render_template('pages/goods_and_categories.html',
                               active_tab=active_tab, items=items, columns=columns, columns_json=columns_json, user=user)
    else:
        items = []
        columns = {
            "category_name": True,
            "category_number": False
        }
        columns_json = json.dumps(columns)
        error_message = "Failed to fetch categories"
        return render_template('pages/goods_and_categories.html',
                               active_tab=active_tab, items=items, columns=columns, columns_json=columns_json, user=user, error_message=error_message)