# Import flask dependencies
from flask import Blueprint, request, render_template, \
                  flash, g, session, redirect, url_for
from flask_oauth import OAuth

# Import password / encryption helper tools
from werkzeug import check_password_hash, generate_password_hash

# Import the database object from the main app module
from app import app
from app import db

# Import module models (i.e. User)
from app.models import User
from app.models import Item

# Define the blueprint: 'auth', set its url prefix: app.url/auth
mod_auth = Blueprint('auth', __name__, url_prefix='')

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


@mod_auth.route('/login')
def login():
    return facebook.authorize(callback=url_for('auth.facebook_authorized',
        next=request.args.get('next') or request.referrer or None,
        _external=True))

@mod_auth.route('/logout')
def logout():
    session.pop('oauth_token', None)
    flash('Logged out.')
    return redirect(url_for('base.index'))

@mod_auth.route('/login/authorized')
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


