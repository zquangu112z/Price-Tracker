import time
from sqlite3 import dbapi2 as sqlite3
from hashlib import md5
from datetime import datetime
from flask import Flask, request, session, url_for, redirect, \
    render_template, abort, g, flash, _app_ctx_stack
from werkzeug import check_password_hash, generate_password_hash


# configuration
DATABASE = '/tmp/pricetracker.db'
PER_PAGE = 30
DEBUG = True
SECRET_KEY = b'_5#yjkhdjkfhasd2L"F4Q8z\n\xec]/'

# create our little application :)
app = Flask('pricetracker')
app.config.from_object(__name__)


def get_db():
    """Opens a new database connection if there is none yet for the
    current application context.
    """
    top = _app_ctx_stack.top
    if not hasattr(top, 'sqlite_db'):
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
    with app.open_resource('schema.sql', mode='r') as f:
        db.cursor().executescript(f.read())
    db.commit()


@app.cli.command('initdb')
def initdb_command():
    """Creates the database tables."""
    init_db()
    print('Initialized the database.')


@app.route('/home', methods=['GET', 'POST'])
def home():
    status = None
    if request.method == 'POST':
        url_product = request.form['url_product']
        current_price = request.form['current_price']
        desired_price = request.form['desired_price']
        email = request.form['email']
        query_str = "INSERT INTO product(url_product, current_price, \
        desired_price, email) VALUES ('%s', '%s', '%s', '%s');" % (
            url_product, current_price, desired_price, email)
        try:
            print(query_str)

            db = get_db()
            db.execute(query_str)
            db.commit()

            status = "We have received your request successful. \
            If the price meet your desired value, \
            we will send a notification to your email."
        except Exception as e:
            status = "Opps! We cannot complete the work for you. " + str(e)
        # return redirect(url_for('timeline'))
    return render_template('home.html', status=status)


def query_db(query, args=(), one=False):
    """Queries the database and returns a list of dictionaries."""
    cur = get_db().execute(query, args)
    rv = cur.fetchall()
    return (rv[0] if rv else None) if one else rv


def format_datetime(timestamp):
    """Format a timestamp for display."""
    return datetime.utcfromtimestamp(timestamp).strftime('%Y-%m-%d @ %H:%M')


def gravatar_url(email, size=80):
    """Return the gravatar image for the given email address."""
    return 'https://www.gravatar.com/avatar/%s?d=identicon&s=%d' % \
        (md5(email.strip().lower().encode('utf-8')).hexdigest(), size)


@app.route('/')
def root_page():
    return redirect(url_for('home'))

# todo: list product arcording to email


# add some filters to jinja
app.jinja_env.filters['datetimeformat'] = format_datetime
