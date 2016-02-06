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

# Import forms
from app.forms import RefreshForm

from app.helpers import *
import json
import datetime
import requests

from sqlalchemy import desc

# Define the blueprint: 'auth', set its url prefix: app.url/auth
mod_fb = Blueprint('fb', __name__, url_prefix='')

# OAuth
oauth = OAuth()

facebook = oauth.remote_app('facebook',
    base_url='https://graph.facebook.com/',
    request_token_url=None,
    access_token_url='/oauth/access_token',
    access_token_method='GET',
    authorize_url='https://www.facebook.com/dialog/oauth',
    consumer_key=app.config['FACEBOOK_APP_ID'],
    consumer_secret=app.config['FACEBOOK_APP_SECRET'],
    request_token_params={'scope': 'email'}
)

@mod_fb.route('/', methods=['POST'])
def refresh():
    form = RefreshForm()
    if form.validate_on_submit():
        flash('Refreshed')
        feed = facebook.get('/580647781993254/feed')
        if feed.status == 200:
            feed_ids = { post['id'] for post in feed.data['data'] }
            db_ids = { item.facebook_id for item in Item.query.all() }
            # Save pagination
            session['paginate_previous'] = feed.data['paging']['previous']
            session['paginate_next'] = feed.data['paging']['next']
            # Insert new items
            for feed_id in feed_ids.difference(db_ids):
                post = facebook.get('/' + feed_id + '?' +
                        'fields=id,updated_time,message,from,picture,' +
                        'full_picture')
                if post.status == 200:
                    data = post.data
                    message = data['message'] if 'message' in data else ""
                    if not message:
                        continue
                    db.session.add(Item(
                        name=title(message),
                        description=message,
                        category='Uncategorized',
                        photo=data['full_picture'] if 'full_picture' in data else "",
                        facebook_id=data['id'],
                        updated_time=datetime.datetime.strptime(data['updated_time'],
                            '%Y-%m-%dT%H:%M:%S+0000'),
                        price=price(message),
                        sold=False,
                        hold=False,
                        seller_id=None))
                else:
                    flash('Refresh failed')
        else:
            flash('Refresh failed')
        db.session.commit()
        return redirect(url_for('base.index'))
    return redirect(url_for('base.index'))

@mod_fb.route('/next')
def next():
    if not ('paginate_next' in session and session['paginate_next']):
        return 'No next page'
    print 'paginate_next:', session['paginate_next']
    feed = facebook.get(session['paginate_next'])
    print "status:", feed.status
    if feed.status == 200:
        data = feed.data
        print data
        feed_ids = { post['id'] for post in data['data'] }
        db_ids = { item.facebook_id for item in Item.query.all() }
        # Save pagination
        session['paginate_previous'] = data['paging']['previous']
        session['paginate_next'] = data['paging']['next']
        # Insert new items
        for feed_id in feed_ids.difference(db_ids):
            post = facebook.get('/' + feed_id + '?' +
                    'fields=id,updated_time,message,from,picture,' +
                    'full_picture')
            if post.status == 200:
                data = post.data
                message = data['message'] if 'message' in data else ""
                if not message:
                    continue
                db.session.add(Item(
                    name=title(message),
                    description=message,
                    category='Uncategorized',
                    photo=data['full_picture'] if 'full_picture' in data else "",
                    facebook_id=data['id'],
                    updated_time=datetime.datetime.strptime(data['updated_time'],
                        '%Y-%m-%dT%H:%M:%S+0000'),
                    price=price(message),
                    sold=False,
                    hold=False,
                    seller_id=None))
            else:
                return 'Refresh failed'
    else:
        return 'Refresh failed'
    db.session.commit()

    # Render items
    items = [ {
        'name' : item.name,
        'description' : item.description,
        'category' : item.category,
        'facebook_id' : item.facebook_id,
        'photo' : item.photo,
        'price' : item.price,
        'sold' : item.sold,
        'hold' : item.hold,
        'seller' : item.seller,
        } for item in Item.query.filter(
            Item.facebook_id.in_(feed_ids)).order_by(desc(Item.updated_time)).all() ]

    return render_template("page.html", items=items)


@mod_fb.route('/login')
def login():
    return facebook.authorize(callback=url_for('fb.facebook_authorized',
        next=request.args.get('next') or request.referrer or None,
        _external=True))

@mod_fb.route('/logout')
def logout():
    session.pop('oauth_token', None)
    flash('Logged out.')
    return redirect(url_for('base.index'))

@mod_fb.route('/login/authorized')
@facebook.authorized_handler
def facebook_authorized(resp):
    if resp is None:
        return 'Access denied: reason=%s error=%s' % (
            request.args['error_reason'],
            request.args['error_description']
        )
    session['oauth_token'] = (resp['access_token'], '')
    #me = facebook.get('/me')
    #return 'Logged in as id=%s name=%s redirect=%s' % \
    #    (me.data['id'], me.data['name'], request.args.get('next'))
    flash("Logged in.")
    return redirect(url_for('base.index'))


@facebook.tokengetter
def get_facebook_oauth_token():
    return session.get('oauth_token')


