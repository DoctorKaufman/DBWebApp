from flask import Blueprint, render_template

main = Blueprint('main', __name__)

@main.route('/')
def home():
    user = {'username': 'John Doe'}  # Data to be passed to the template
    return render_template('home.html', user=user)

@main.route('/login')
def login():
    user = {'username': 'John Doe'} 
    return render_template('login.html', user=user)
