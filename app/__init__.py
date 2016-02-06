# Import flask and template operators
from flask import Flask, render_template, redirect, url_for, session, \
        request, flash

# Import extensions
from flask.ext.sqlalchemy import SQLAlchemy
from flask_oauth import OAuth

# Define the WSGI application object
app = Flask(__name__)

# Configurations
app.config.from_object('config')

# OAuth
oauth = OAuth()

facebook = oauth.remote_app('facebook',
    base_url='https://graph.facebook.com/',
    request_token_url=None,
    access_token_url='/oauth/access_token',
    authorize_url='https://www.facebook.com/dialog/oauth',
    consumer_key=app.config['FACEBOOK_APP_ID'],
    consumer_secret=app.config['FACEBOOK_APP_SECRET'],
    request_token_params={'scope': 'email'}
)


@app.route('/login')
def login():
    return facebook.authorize(callback=url_for('facebook_authorized',
        next=request.args.get('next') or request.referrer or None,
        _external=True))

@app.route('/logout')
def logout():
    session.pop('oauth_token', None)
    flash('Logged out.')
    return redirect(url_for('base.index'))


@app.route('/login/authorized')
@facebook.authorized_handler
def facebook_authorized(resp):
    if resp is None:
        return 'Access denied: reason=%s error=%s' % (
            request.args['error_reason'],
            request.args['error_description']
        )
    session['oauth_token'] = (resp['access_token'], '')
    print("token", session['oauth_token'])
    #me = facebook.get('/me')
    #return 'Logged in as id=%s name=%s redirect=%s' % \
    #    (me.data['id'], me.data['name'], request.args.get('next'))
    flash("Logged in.")
    return redirect(url_for('base.index'))


@facebook.tokengetter
def get_facebook_oauth_token():
    return session.get('oauth_token')


# Define the database object which is imported
# by modules and controllers
db = SQLAlchemy(app)

# Sample HTTP error handling
@app.errorhandler(404)
def not_found(error):
    return render_template('404.html'), 404

# Import a module / component using its blueprint handler variable (mod_auth)
from app.views.base import mod_base as base_module

# Register blueprint(s)
app.register_blueprint(base_module)
# app.register_blueprint(xyz_module)
# ..

# Build the database:
# This will create the database file using SQLAlchemy
db.create_all()

