from flask import Blueprint, render_template

main = Blueprint('main', __name__)

@main.route('/')
def home():
    user = {'username': 'John Doe'}  # Data to be passed to the template
    return render_template('home.html', user=user)
