from flask import request, session, url_for, redirect, \
    render_template, g, flash
from werkzeug import check_password_hash, generate_password_hash
import time

from .base import app, get_author_id, get_db, get_user_id, query_db
from .helper import getPath, nomalizePrice


@app.route('/')
def root_page():
    if g.user:
        return redirect(url_for('home'))
    else:
        return redirect(url_for('login'))


@app.route('/home', methods=['GET', 'POST'])
def home():
    if not g.user:
        return redirect(url_for('login'))

    status = None
    if request.method == 'POST':
        author_id = get_author_id()
        url_product = request.form['url_product']
        submited_price = nomalizePrice(request.form['current_price'])
        desired_price = nomalizePrice(request.form['desired_price'])
        print(">>>>>>>>>>>>>", submited_price, ">>>>>>>>", desired_price)
        price_path = getPath(submited_price, url_product)
        if not price_path:
            not_found_msg = "Please re-check the current price, \
we cannot allocate it"
            return render_template('home.html', status=not_found_msg)
        query_str = "INSERT INTO product(author_id, url_product, submited_price, \
        desired_price, submit_time, price_path, isdone) VALUES ('%s', '%s', \
        '%s', '%s', %d, '%s', %d);" % (
            author_id,
            url_product,
            submited_price,
            desired_price,
            int(time.time()),
            price_path,
            0)  # 0 means the task has not been done yet
        try:
            print(query_str)

            db = get_db()
            db.execute(query_str)
            db.commit()

            success_msg = "We have received your request successful. \
            If the price meet your desired value, \
            we will send a notification to your email."

            flash(success_msg)

        except Exception as e:
            status = "Opps! We cannot complete the work for you. " + str(e)
        # return redirect(url_for('timeline'))
    return render_template('home.html', status=status)


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


@app.route('/following', methods=['GET'])
def user_following():
    """ List user's following products"""
    if not g.user:
        return redirect(url_for('login'))

    user_id = get_author_id()
    if user_id:
        following_product = query_db(
            "SELECT * FROM product as p where p.author_id=?",
            [user_id])
        print("user {} is following {} products".format(
            user_id, len(following_product)))
    else:
        redirect(url_for('login'))
    return render_template('following.html',
                           following_products=following_product)


@app.route('/stop_follow/<product_id>', methods=['POST'])
def stop_follow():
    return user_following()


@app.route('/logout')
def logout():
    """Logs the user out."""
    flash('You were logged out')
    session.pop('user_id', None)
    return redirect(url_for('login'))
