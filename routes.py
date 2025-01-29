from flask import Blueprint, render_template
from menu import menu_items

bp_routes = Blueprint('routes', __name__)

@bp_routes.route('/')
def index():
    return render_template('index.html', menu_items=menu_items)

@bp_routes.route('/datasource')
def configs():
    return render_template('datasource.html', menu_items=menu_items)

@bp_routes.route('/about')
def about():
    return render_template('about.html', menu_items=menu_items)
