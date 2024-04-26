import json
import requests as requestsLib
from app.views.main import generate_phone_number, generate_unique_id, generate_unique_upc
from flask import Blueprint, render_template
import random


requests = Blueprint('requests', __name__)


@requests.route('/request1')
def request1():
    active_tab = 'request1'
    data = requestsLib.get('http://127.0.0.1:5000/query/1?min-amount=1')

    if all(response.status_code == 200 for response in [data]):
        data = data.json()
        print(data)
    else: 
        data = []

    return render_template('pages/requests.html', data=data, active_tab=active_tab)


@requests.route('/request2')
def request2():
    active_tab = 'request2'
    data = requestsLib.get('http://127.0.0.1:5000/query/2')

    if all(response.status_code == 200 for response in [data]):
        data = data.json()
        print(data)
    else: 
        data = []

    return render_template('pages/requests.html', data=data, active_tab=active_tab)
