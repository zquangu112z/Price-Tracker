from pricetracker.celery_worker import celery_app
from pricetracker.helper import getCurrentPrice, send_mail,\
    get_mail_instance, read_template, isDown, getNumericPrice
import os
from pricetracker.base import query_db
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
        submited_price, desired_price, submit_time, price_path, isdone')
    products = query_db('select * from product where isdone = 0')
    for product in map(ProductRecord._make, products):
        print(product.submited_price)
        current_price = getCurrentPrice(
            product.url_product, product.price_path)
        if isDown(current_price, product.desired_price):
            # Send mail
            print("the pprice is {}".format(current_price))
            receiver = query_db('select email from user \
where user_id = {}'.format(product.author_id))
            message = message_template.substitute(
                PRODUCT_URL=product.url_product,
                PRICE=current_price
            )

            print("Send email to {}".format(receiver[0][0]))
            send_mail(s, message, MAIL_USERNAME,
                      receiver[0][0])

            # Mark as task done in the database
            query_db(
                'update product set isdone = 1 where id = {}'.format(
                    product.id))
