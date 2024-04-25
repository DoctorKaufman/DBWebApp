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
        receipts = json.dumps(receipts)

    else:
        receipts = []

    return render_template('pages/receipts.html',
    active_tab=active_tab, receipts=receipts)