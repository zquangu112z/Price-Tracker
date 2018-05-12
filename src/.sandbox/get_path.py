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
        return True
    else:
        return False


def getCurrentPrice(url_product, path):
    page = urlopen(url_product)
    parser = etree.HTMLParser()
    tree = etree.parse(BytesIO(page.read()), parser)

    # get current price
    current_price = getNumericPrice(tree.xpath(path)[0].text)
    return current_price


def getNumericPrice(price):
    '''
        Nomalize price
    '''
    price = price.replace(".", "")
    return re.findall(r'\d+', price)[0]


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


def send_mail(s, message_template, sender, receiver):
    # @TODO: refactor this function arcoding to tifl
    try:
        msg = MIMEMultipart()
        # add in the actual person name to the message template
        message = message_template.substitute(
            PRODUCT_URL=url,
            PRICE=getCurrentPrice(url, path))

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


if __name__ == "__main__":
    url = "https://www.lazada.vn/products/combo-2-kem-danh-rang-closeup-white-attraction-natural-glow-180g-va-2-ban-chai-danh-rang-charcol-tang-1-durex-fetherlite-12-bao-i209600911-s261456452.html?spm=a2o4n.home.flashSale.4.19056afe7LuGzf&search=1&mp=1&scm=1003.4.icms-zebra-5000410-2735658.ITEM_209600911_2393200"
    price = "135.000"

    path = getPath(price, url)  # @TODO: save path to db
    print(path)
    print(getCurrentPrice(url, path))
    # checked = checkPrice(url, path, "400.000")
    # print(checked)  # run this task everyday
    # # You can also pass the price with currency like this way
    # # print(checkPrice(url, path, "150.000VND"))

    # # @TODO: if TRUE, then send the notification to email
    # # this task is notify the current price
    # MAIL_USERNAME = os.environ.get('MAIL_USERNAME')
    # MAIL_PASSWORD = os.environ.get('MAIL_PASSWORD')
    # s = get_mail_instance(MAIL_USERNAME, MAIL_PASSWORD)

    # message_template = read_template('message_letbuyit.txt')

    # receiver = "zquangu112z@gmail.com"

    # send_mail(s, message_template, MAIL_USERNAME, receiver)
