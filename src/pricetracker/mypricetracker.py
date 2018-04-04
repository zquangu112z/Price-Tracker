import time
from sqlite3 import dbapi2 as sqlite3
from hashlib import md5
from datetime import datetime
from flask import Flask, request, session, url_for, redirect, \
    render_template, abort, g, flash, _app_ctx_stack
from werkzeug import check_password_hash, generate_password_hash


# configuration
DATABASE = '/Users/kilia/Desktop/pricetracker.db'
PER_PAGE = 30
DEBUG = True
SECRET_KEY = b'_5#yjkhdjkfhasd2L"F4Q8z\n\xec]/'


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


def get_author_id():
    user_id = session['user_id']
    return user_id


@app.route('/home', methods=['GET', 'POST'])
def home():
    if not g.user:
        return redirect(url_for('login'))

    status = None
    if request.method == 'POST':
        author_id = get_author_id()
        url_product = request.form['url_product']
        current_price = request.form['current_price']
        desired_price = request.form['desired_price']
        # email = request.form['email']
        query_str = "INSERT INTO product(author_id, url_product, current_price, \
        desired_price) VALUES ('%s', '%s', '%s', '%s');" % (
            author_id, url_product, current_price, desired_price)
        try:
            print(query_str)

            db = get_db()
            db.execute(query_str)
            db.commit()

            flash("We have received your request successful. \
            If the price meet your desired value, \
            we will send a notification to your email.")
        except Exception as e:
            status = "Opps! We cannot complete the work for you. " + str(e)
        # return redirect(url_for('timeline'))
    return render_template('home.html', status=status)


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


def format_datetime(timestamp):
    """Format a timestamp for display."""
    return datetime.utcfromtimestamp(timestamp).strftime('%Y-%m-%d @ %H:%M')


def gravatar_url(email, size=80):
    """Return the gravatar image for the given email address."""
    return 'https://www.gravatar.com/avatar/%s?d=identicon&s=%d' % \
        (md5(email.strip().lower().encode('utf-8')).hexdigest(), size)


@app.route('/')
def root_page():
    if g.user:
        return redirect(url_for('home'))
    else:
        return redirect(url_for('login'))


@app.route('/login', methods=['GET', 'POST'])
def login():
    """Logs the user in."""
    if g.user:
        return redirect(url_for('home'))
    error = None
    if request.method == 'POST':
        user = query_db('''select * from user where
            username = ?''', [request.form['username']], one=True)
        if user is None:
            error = 'Invalid username'
        elif not check_password_hash(user['pw_hash'],
                                     request.form['password']):
            error = 'Invalid password'
        else:
            flash('You were logged in')
            session['user_id'] = user['user_id']
            return redirect(url_for('home'))
    return render_template('login.html', error=error)


@app.route('/register', methods=['GET', 'POST'])
def register():
    """Registers the user."""
    if g.user:
        return redirect(url_for('home'))
    error = None
    if request.method == 'POST':
        if not request.form['username']:
            error = 'You have to enter a username'
        elif not request.form['email'] or \
                '@' not in request.form['email']:
            error = 'You have to enter a valid email address'
        elif not request.form['password']:
            error = 'You have to enter a password'
        elif request.form['password'] != request.form['password2']:
            error = 'The two passwords do not match'
        elif get_user_id(request.form['username']) is not None:
            error = 'The username is already taken'
        else:
            db = get_db()
            db.execute('''insert into user (
              username, email, pw_hash) values (?, ?, ?)''',
                       [request.form['username'], request.form['email'],
                        generate_password_hash(request.form['password'])])
            db.commit()
            flash('You were successfully registered and can login now')
            return redirect(url_for('login'))
    return render_template('register.html', error=error)


@app.route('/following')
def user_following():
    """ List user's following products"""
    if not g.user:
        return redirect(url_for('login'))

    user_id = get_author_id()
    if user_id:
        following_product = query_db(
            "SELECT * FROM product as p where p.author_id=?",
            [user_id])
        print(">>>>>>>>>", len(following_product))
    else:
        redirect(url_for('login'))
    return render_template('following.html',
                           following_products=following_product)


@app.route('/logout')
def logout():
    """Logs the user out."""
    flash('You were logged out')
    session.pop('user_id', None)
    return redirect(url_for('login'))


# add some filters to jinja
app.jinja_env.filters['datetimeformat'] = format_datetime
