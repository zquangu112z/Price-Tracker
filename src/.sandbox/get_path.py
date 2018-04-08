from urllib.request import urlopen
from lxml import etree
from io import BytesIO
import re


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

    print(">>>>>>>Current: ", current_price,  ". Desired: ", desired_price)

    if current_price <= desired_price:
        return True
    else:
        return False


def getNumericPrice(price):
    '''
        Nomalize price
    '''
    price = price.replace(".", "")
    return re.findall(r'\d+', price)[0]


if __name__ == "__main__":
    url = "https://tiki.vn/ly-giu-nhiet-bang-thep-khong-gi-lock-lock-clip-tumb\
ler-lhc4151blk-540ml-den-p1453915.html?spid=1454601&src=lp-locknlock"
    price = "199.000"

    path = getPath(price, url)  # save to db
    print(checkPrice(url, path, "400.000"))  # run this task everyday
    print(checkPrice(url, path, "150.000VND"))
