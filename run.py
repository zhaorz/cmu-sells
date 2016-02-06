from flask.ext.script import Manager
from flask_migrate import Migrate, MigrateCommand

from app import app, db

from app.models import *

migrate = Migrate(app, db)

manager = Manager(app)
manager.add_command('db', MigrateCommand)

@manager.command
def run():
    app.run(host='0.0.0.0', port=8080, debug=True)

@manager.command
def db_populate():
    richardz = User(
            name='Richard Zhao',
            email='richardz@andrew.cmu.edu',
            facebook_url='https://www.facebook.com/richard.zhao7')

    item0 = Item(
            name='Timex Watch',
            description='Timex Weekender watch, brown leather strap',
            category='Jewlery',
            photo='img/item0.jpg',
            price=10.0,
            sold=False,
            hold=False)

    item1 = Item(
            name='Macbook Pro Retina 13"',
            description='Late 2015 version.',
            category='Electronics',
            photo='img/item1.jpg',
            price=1000.0,
            sold=False,
            hold=False)

    item2 = Item(
            name='Rin\'s Drawing',
            description='It\'s beautiful.',
            category='Artwork',
            photo='img/item2.jpg',
            price=2500000.0,
            sold=True,
            hold=False)

    richardz.items = [item0, item1, item2]

    db.session.add(richardz)
    db.session.add(item0)

    db.session.commit()


if __name__ == '__main__':
    manager.run()

