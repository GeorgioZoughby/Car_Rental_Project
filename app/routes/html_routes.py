from flask import Blueprint, render_template 
import requests

html_bp = Blueprint('template', __name__)

@html_bp.route('/')
def home():
    data = [1,2,3]
    return render_template('index.html')

@html_bp.route('/categories', methods=['GET'])
def categories_page():
    response = requests.get('http://localhost:5000/api/categories')
    if response.status_code == 200:
        categories = response.json()
        # [(1, "Luxury"),(2, "Economic")]
    else:
        categories = []
    return render_template('categories.html', categories=categories)


@html_bp.route('/dashboard')
def admin_dashboard():
    return render_template('dashboard.html')

