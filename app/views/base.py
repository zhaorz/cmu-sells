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

# Define the blueprint: 'auth', set its url prefix: app.url/auth
mod_base = Blueprint('base', __name__, url_prefix='/')

# Set the route and accepted methods
@mod_base.route('/', methods=['GET', 'POST'])
def index():
    return render_template("index.html")
