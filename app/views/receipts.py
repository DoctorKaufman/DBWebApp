from app.views.main import generate_phone_number, generate_unique_id, generate_unique_upc
from flask import Blueprint, render_template
import random


receipts = Blueprint('receipts', __name__)


@receipts.route('/receipts')
def checks():
    receipts = [
        {
            "name": f"Customer {i}",
            "card number": generate_unique_id(),
            "percent": f"{random.randint(1, 100)}%",
            "phone_number": generate_phone_number(),
            "address": f"City, Street, {random.randint(1, 100)}",
        } for i in range(1, 9)
    ]
    active_tab = 'receipts'
    return render_template('pages/receipts.html', receipts=receipts, active_tab=active_tab)
