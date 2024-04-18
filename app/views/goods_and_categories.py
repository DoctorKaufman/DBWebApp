from app.views.main import generate_unique_id, generate_unique_upc
from flask import Blueprint, render_template
import json
import random
import requests


goods_and_categories = Blueprint('goods_and_categories', __name__)


@goods_and_categories.route('/goods-in-store')
def goods_in_store():
    active_tab = 'goods_in_store'
    columns = requests.get('http://127.0.0.1:5000/store-product/columns')
    data = requests.get('http://127.0.0.1:5000/store-product/')
    key_column = requests.get('http://127.0.0.1:5000/store-product/pk')

    if all(response.status_code == 200 for response in [data, columns, key_column]):
        items = data.json()
        items = json.dumps(items)
        columns = columns.json()
        columns_json = json.dumps(columns)
        key_column = key_column.json()
        return render_template('pages/goods_and_categories.html',
                               active_tab=active_tab, items=items, columns=columns,
                                 columns_json=columns_json, key_column=key_column)
    else:
        items = []
        columns = {
            "id_product": True,
            "products_number": True,
            "promotional_product": True,
            "selling_price": True,
            "upc": False,
            "upc_prom": True
        }
        columns_json = json.dumps(columns)
        key_column = "UPC"
        error_message = "Failed to fetch categories"
        return render_template('pages/goods_and_categories.html',
                               active_tab=active_tab, items=items, columns=columns, key_column=key_column, 
                               columns_json=columns_json, error_message=error_message)


@goods_and_categories.route('/goods')
def goods():
    active_tab = 'goods'
    columns = requests.get('http://127.0.0.1:5000/product/columns')
    data = requests.get('http://127.0.0.1:5000/product/')
    key_column = requests.get('http://127.0.0.1:5000/product/pk')

    if all(response.status_code == 200 for response in [data, columns, key_column]):
        items = data.json()
        columns = columns.json()
        columns_json = json.dumps(columns)
        key_column = key_column.json()
        return render_template('pages/goods_and_categories.html',
                               active_tab=active_tab, items=items, columns=columns,
                                 columns_json=columns_json, key_column=key_column)
    else:
        items = []
        columns = {
            "category_number": True,
            "id_product": False,
            "p_characteristics": True,
            "product_name": False
        }
        columns_json = json.dumps(columns)
        key_column = "ID" 
        error_message = "Failed to fetch categories"
        return render_template('pages/goods_and_categories.html',
                               active_tab=active_tab, items=items, columns=columns, key_column=key_column, 
                               columns_json=columns_json, error_message=error_message)


@goods_and_categories.route('/categories')
def categories():
    active_tab = 'categories'
    columns = requests.get('http://127.0.0.1:5000/category/columns')
    data = requests.get('http://127.0.0.1:5000/category/')
    key_column = requests.get('http://127.0.0.1:5000/category/pk')

    if all(response.status_code == 200 for response in [data, columns, key_column]):
        items = data.json()
        columns = columns.json()
        columns_json = json.dumps(columns)
        key_column = key_column.json()
        return render_template('pages/goods_and_categories.html',
                               active_tab=active_tab, items=items, columns=columns,
                                 columns_json=columns_json, key_column=key_column)
    else:
        items = []
        columns = {
            "category_name": True,
            "category_number": False
        }
        columns_json = json.dumps(columns)
        key_column = "ID"
        error_message = "Failed to fetch categories"
        return render_template('pages/goods_and_categories.html',
                               active_tab=active_tab, items=items, columns=columns, key_column=key_column, 
                               columns_json=columns_json, error_message=error_message)