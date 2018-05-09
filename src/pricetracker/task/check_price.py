from pricetracker.celery_worker import app
import sqlite3
from pricetracker.task.helper import getCurrentPrice, send_mail,\
    get_mail_instance, read_template
import os


class ExternalDataContext():
    def __init__(self, db_filepath):
        self.conn = sqlite3.connect(db_filepath)

    def __enter__(self):
        self.c = self.conn.cursor()
        return self.c

    def __exit__(self, *args):
        self.conn.close()


@app.task
def say_hello():
    print("Hello Ngu Quang Truong")


@app.task
def check():
    # Get email instance
    MAIL_USERNAME = os.environ.get('MAIL_USERNAME')
    MAIL_PASSWORD = os.environ.get('MAIL_PASSWORD')
    s = get_mail_instance(MAIL_USERNAME, MAIL_PASSWORD)
    # @TODO: get message, not message template
    message_template = read_template(
        'data/message_template/message_letbuyit.txt')

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
