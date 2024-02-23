from flask import Blueprint, render_template

main = Blueprint('main', __name__)

@main.route('/')
def home():
    user = {'username': 'John Doe'} 
    return render_template('pages/home.html', user=user)

@main.route('/goods')
def goods():
    user = {'username': 'John Doe'} 
    return render_template('pages/goods.html', user=user)

@main.route('/login')
def login():
    user = {'username': 'John Doe'} 
    return render_template('pages/login.html', user=user)
