from pricetracker.celery_worker import celery_app
import sqlite3
from pricetracker.helper import getCurrentPrice, send_mail,\
    get_mail_instance, read_template, isDown
import os
from pricetracker.base import app, query_db
from collections import namedtuple


@celery_app.task
def say_hello():
    print("Hello Ngu Quang Truong")


@celery_app.task
def check():
    # Get email instance
    MAIL_USERNAME = os.environ.get('MAIL_USERNAME')
    MAIL_PASSWORD = os.environ.get('MAIL_PASSWORD')
    s = get_mail_instance(MAIL_USERNAME, MAIL_PASSWORD)
    # @TODO: get message, not message template
    message_template = read_template(
        'data/message_template/message_letbuyit.txt')

    ProductRecord = namedtuple('ProductRecord', 'id, author_id, url_product, \
        submited_price, desired_price, submit_time, price_path')
    products = query_db('select * from product')
    for product in map(ProductRecord._make, products):
        print(product.submited_price)
        current_price = getCurrentPrice(
            product.url_product, product.price_path)
        if isDown(current_price, product.desired_price):
            # Send mail
            print("the pprice is {}".format(current_price))
            receiver = query_db('select email from user \
where user_id = {}'.format(product.author_id))
            print("Send email to {}".format(receiver[0][0]))
            send_mail(s, message_template, MAIL_USERNAME,
                      receiver[0][0], product.url_product, current_price)


'''
    # Connect db
    with ExternalDataContext('pricetracker.db') as c:
        products_query_string = 'select * from product'
        c.execute(products_query_string)
        products = c.fetchall()
        for product in products:
            # Refactor the app
            # app:@TODO: init the db again
            # app:@TODO: get path of prodct and save to db

            # get price_path from db
            url_product = product[2]
            price_path = product[6]
            desired_price = product[4]
            receiver = 'zquangu112z@gmail.com'
            # get current price
            current_price = getCurrentPrice(url_product, price_path)
            if desired_price <= current_price:
                # @TODO: function send_mail must be failed \
                # due to the un formatted message_template
                send_mail(s, message_template, MAIL_USERNAME, receiver)
'''
