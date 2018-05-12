from urllib.request import urlopen
from lxml import etree
from io import BytesIO
import re
import smtplib
from string import Template
from email.mime.multipart import MIMEMultipart
from email.mime.text import MIMEText
import os
import logging as logger


def get_Path(price, url_product):
    '''
        Testing purpose only
    '''
    page = urlopen(url_product)

    parser = etree.HTMLParser()
    tree = etree.parse(BytesIO(page.read()), parser)

    for e in tree.iter():
        if e.text and price in e.text:
            path = tree.getpath(e)
            print("PATH: ", path)
            current_price = getNumericPrice(tree.xpath(path)[0].text)

            print("CONTENT: ", current_price)
            return


def getPath(price, url_product):
    '''
            save the path of the price at an url of a product
    '''
    page = urlopen(url_product)

    parser = etree.HTMLParser()
    tree = etree.parse(BytesIO(page.read()), parser)

    for e in tree.iter():
        # @TODO: normalize price
        if e.text and price in e.text:
            path = tree.getpath(e)
            return path


def checkPrice(url_product, path, desired_price):
    page = urlopen(url_product)
    parser = etree.HTMLParser()
    tree = etree.parse(BytesIO(page.read()), parser)

    # get current price
    current_price = getNumericPrice(tree.xpath(path)[0].text)
    # nomalize desired price
    desired_price = getNumericPrice(desired_price)

    print(">>>>>>>Current: ", current_price, ". Desired: ", desired_price)

    if current_price <= desired_price:
        return 7
    else:
        return False


def isDown(current_price, desired_price):
    return int(getNumericPrice(current_price)) < int(getNumericPrice(desired_price))


def getCurrentPrice(url_product, path):
    page = urlopen(url_product)
    parser = etree.HTMLParser()
    tree = etree.parse(BytesIO(page.read()), parser)

    # get current price
    current_price = tree.xpath(path)[0].text
    return current_price


def getNumericPrice(price):
    '''
        Nomalize price @TODO
    '''
    price = str(price)
    price = price.replace(".", "")
    try:
        return re.findall(r'\d+', price)[0]
    except IndexError:
        return price


def read_template(filename):
    with open(filename, 'r', encoding='utf-8') as template_file:
        template_file_content = template_file.read()
    return Template(template_file_content)


def get_mail_instance(username,
                      password,
                      host='smtp.googlemail.com',
                      port=587):
    s = smtplib.SMTP(host, port)
    s.starttls()
    s.login(username, password)
    return s


def send_mail(s, message_template, sender, receiver, url, current_price):
    # @TODO: refactor this function arcoding to tifl
    try:
        msg = MIMEMultipart()
        # add in the actual person name to the message template
        message = message_template.substitute(
            PRODUCT_URL=url,
            PRICE=current_price
        )

        # setup the parameters of the message
        msg['From'] = sender
        msg['To'] = receiver
        msg['Subject'] = "The product you are watching has down its price."

        # add in the message body
        msg.attach(MIMEText(message, 'plain'))

        # send the message via the server set up earlier.
        s.send_message(msg)
        logger.warning("Send mail successful to receiver {}".format(receiver))
    except Exception as e:
        raise e
