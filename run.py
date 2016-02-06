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
            photo='/path/to/item0.jpg',
            price=10.0,
            sold=False,
            hold=False)

    richardz.items = [item0]

    db.session.add(richardz)
    db.session.add(item0)

    db.session.commit()


if __name__ == '__main__':
    manager.run()

