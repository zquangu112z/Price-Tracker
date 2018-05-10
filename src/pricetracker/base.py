from celery import Celery
from sqlite3 import dbapi2 as sqlite3
from flask import Flask, session, g, _app_ctx_stack
from flask_mail import Mail
from . import my_config


app = Flask(__name__)
app.config.from_object(my_config)

mail = Mail(app)

celery = Celery(__name__, broker=app.config['CELERY_BROKER_URL'])
celery.conf.update(app.config)


def get_db():
    """Opens a new database connection if there is none yet for the
    current application context.
    """
    top = _app_ctx_stack.top
    # Support calling this function from check_price.py @TODO: document it
    if not top:
        top = app.app_context()

    if not hasattr(top, 'sqlite_db'):
        print(">>>>>>>>>>>>>> ", app.config['DATABASE'])
        top.sqlite_db = sqlite3.connect(app.config['DATABASE'])
        top.sqlite_db.row_factory = sqlite3.Row
    return top.sqlite_db


@app.teardown_appcontext
def close_database(exception):
    """Closes the database again at the end of the request."""
    top = _app_ctx_stack.top
    if hasattr(top, 'sqlite_db'):
        top.sqlite_db.close()


def init_db():
    """Initializes the database."""
    db = get_db()
    with app.open_resource(
            app.config['DATABASE_SCHEMA_FILENAME'],
            mode='r') as f:
        db.cursor().executescript(f.read())
    db.commit()


@app.cli.command('initdb')
def initdb_command():
    """Creates the database tables."""
    init_db()
    print('Initialized the database.')


def get_author_id():
    user_id = session['user_id']
    return user_id


def query_db(query, args=(), one=False):
    """Queries the database and returns a list of dictionaries."""
    cur = get_db().execute(query, args)
    rv = cur.fetchall()
    return (rv[0] if rv else None) if one else rv


@app.before_request
def before_request():
    g.user = None
    if 'user_id' in session:
        g.user = query_db('select * from user where user_id = ?',
                          [session['user_id']], one=True)


def get_user_id(username):
    """Convenience method to look up the id for a username."""
    rv = query_db('select user_id from user where username = ?',
                  [username], one=True)
    return rv[0] if rv else None


if __name__ == '__main__':
    app.run()
