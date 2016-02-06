# Import the database object (db) from the main application module
# We will define this inside /app/__init__.py in the next sections.
from app import db

# Define a base model for other database tables to inherit
class Base(db.Model):

    __abstract__  = True

    id            = db.Column(db.Integer, primary_key=True)
    date_created  = db.Column(db.DateTime, default=db.func.current_timestamp())
    date_modified = db.Column(db.DateTime, default=db.func.current_timestamp(),
                                          onupdate=db.func.current_timestamp())


watch_table = db.Table('watchers',
    db.Column('user_id', db.Integer, db.ForeignKey('user.id')),
    db.Column('item_id', db.Integer, db.ForeignKey('item.id'))
)

class User(Base):

    __tablename__ = 'user'

    name    = db.Column(db.String(128),  nullable=False)
    email    = db.Column(db.String(128),  nullable=False,
                                            unique=True)
    facebook_url    = db.Column(db.String(128),  nullable=False,
                                            unique=True)

    items = db.relationship('Item', backref='seller', lazy='dynamic')

    watching = db.relationship(
            'Item',
            secondary=watch_table,
            back_populates='watchers')

    def __repr__(self):
        return '<User %r>' % (self.name)

class Item(Base):

    __tablename__ = 'item'

    name = db.Column(db.String(256), nullable=False)
    description = db.Column(db.String(1024), nullable=False)
    category = db.Column(db.String(128), nullable=False)
    photo = db.Column(db.String(1024), nullable=False)
    facebook_id = db.Column(db.String(256))

    price = db.Column(db.String(128))

    sold = db.Column(db.Boolean)
    hold = db.Column(db.Boolean)

    seller_id = db.Column(db.Integer, db.ForeignKey('user.id'))

    watchers = db.relationship(
            'User',
            secondary=watch_table,
            back_populates='watching')

    def __repr__(self):
        return '<Item %r>' % (self.name)

