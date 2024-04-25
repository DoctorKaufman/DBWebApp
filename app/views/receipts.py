import json
import requests
from app.views.main import generate_phone_number, generate_unique_id, generate_unique_upc
from flask import Blueprint, render_template
import random


receipts = Blueprint('receipts', __name__)


@receipts.route('/receipts')
def checks():
    active_tab = 'receipts'
    data = requests.get('http://127.0.0.1:5000/receipt/')

    if data.status_code == 200:
        receipts = data.json()

    return render_template('pages/receipts.html',
    active_tab=active_tab, receipts=receipts)


# def workers():
    # active_tab = 'workers'
    # positions = ["Manager", "Cashier", "Cleaner", "Consultant", "Security"]
    # data = requests.get('http://127.0.0.1:5000/employee/')
    # columns = requests.get('http://127.0.0.1:5000/employee/columns')
    # key_column = requests.get('http://127.0.0.1:5000/employee/pk')

    # if all(response.status_code == 200 for response in [data, columns, key_column]):
    #     people = data.json()
    #     columns = columns.json()
    #     columns_json = json.dumps(columns)
    #     key_column = key_column.json()
    #     return render_template('pages/staff_and_clients.html',
    #                            active_tab=active_tab, people=people, columns=columns,
    #                              columns_json=columns_json, key_column=key_column, positions=positions)
    # else:
    #     people = []
    #     columns = {
    #     }
    #     columns_json = json.dumps(columns)
    #     key_column = "ID"
    #     error_message = "Failed to fetch workers"
    #     return render_template('pages/goods_and_categories.html',
    #                            active_tab=active_tab, people=people, columns=columns, key_column=key_column, 
    #                            columns_json=columns_json, error_message=error_message, positions=positions)