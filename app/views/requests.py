import json
import requests as requestsLib
from app.views.main import generate_phone_number, generate_unique_id, generate_unique_upc
from flask import Blueprint, render_template
import random


requests = Blueprint('requests', __name__)


@requests.route('/request1')
def request1():
    active_tab = 'request1'

    return render_template('pages/requests.html', active_tab=active_tab)


@requests.route('/request2')
def request2():
    active_tab = 'request2'

    return render_template('pages/requests.html', active_tab=active_tab)
