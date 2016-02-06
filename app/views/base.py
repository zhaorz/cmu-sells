# Import flask dependencies
from flask import Blueprint, request, render_template, \
                  flash, g, session, redirect, url_for

# Import password / encryption helper tools
from werkzeug import check_password_hash, generate_password_hash

# Import the database object from the main app module
from app import db

# Import module forms

# Import module models (i.e. User)
from app.models import User
from app.models import Item

# Define the blueprint: 'auth', set its url prefix: app.url/auth
mod_base = Blueprint('base', __name__, url_prefix='')

@mod_base.route('/', methods=['GET', 'POST'])
def index():
    items = [ {
        'name' : item.name,
        'description' : item.description,
        'category' : item.category,
        'photo' : item.photo,
        'price' : item.price,
        'sold' : item.sold,
        'hold' : item.hold,
        'seller' : item.seller,
        } for item in Item.query.all()]

    return render_template("index.html", items=items)

@mod_base.route('/about', methods=['GET'])
def about():
    return render_template("about.html")

@mod_base.route('/item', methods=['GET', 'POST'])
def item():
    return render_template("item.html")

@mod_base.route('/new-item', methods=['GET', 'POST'])
def new_item():
    return render_template("new-item.html")

@mod_base.route('/user', methods=['GET', 'POST'])
def user():
    return render_template("user.html")

@mod_base.route('/test', methods=['GET', 'POST'])
def test():
    return render_template("test.html")
