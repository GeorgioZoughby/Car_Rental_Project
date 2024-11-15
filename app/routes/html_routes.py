from flask import Blueprint, render_template 
import requests

html_bp = Blueprint('template', __name__)

@html_bp.route('/')
def home():
    data = {
        'title': 'Welcome to My Flask App',
        'message': 'This is a simple HTML page rendered by Flask.',
        'items': ['Item 1', 'Item 2', 'Item 3']
    }
    username = "Georgio"
    return render_template('index.html', data=data, name=username)

@html_bp.route('/categories', methods=['GET'])
def categories_page():
    response = requests.get('http://localhost:5000/api/categories')
    if response.status_code == 200:
        categories = response.json()
    else:
        categories = []
    return render_template('categories.html', categories=categories)

