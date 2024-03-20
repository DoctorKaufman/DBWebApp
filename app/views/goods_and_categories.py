from app.views.main import generate_unique_id, generate_unique_upc
from flask import Blueprint, render_template
import json
import random


goods_and_categories = Blueprint('goods_and_categories', __name__)


@goods_and_categories.route('/goods-in-store')
def goods_in_store():
    active_tab = 'goods_in_store'
    categories = ["Fruit", "Vegetable", "Snack", "Meat & Meat products", "Beverage", "Dairy"]
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
    return render_template('pages/goods_and_categories.html',categories=categories, active_tab=active_tab, items=items, user=user)


@goods_and_categories.route('/goods')
def goods():
    active_tab = 'goods'
    items = [
        {
            "name": f"Product {i}",
            "ID": generate_unique_id(),
            "producer": f"Producer {i}",
            "characteristics": f"Characteristics {i}",
        } for i in range(1, 16)
    ]
    user = {'username': 'John Doe'} 
    return render_template('pages/goods_and_categories.html',active_tab=active_tab, items=items, user=user)


@goods_and_categories.route('/categories')
def categories():
    active_tab = 'categories'
    items = [
        {
            "name": f"Category {i}",
            "category_id": generate_unique_id(),
        } for i in range(1, 6)
    ]
    user = {'username': 'John Doe'}
    return render_template('pages/goods_and_categories.html',active_tab=active_tab, items=items, user=user)