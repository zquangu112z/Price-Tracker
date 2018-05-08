import os

os.path.abspath(__file__)

# configuration
DATABASE = 'pricetracker.db'
PER_PAGE = 30
DEBUG = True
SECRET_KEY = b'_5#yjkhdjkfhasd2L"F4Q8z\n\xec]/'

# email server
MAIL_SERVER = 'smtp.googlemail.com'
MAIL_PORT = 587
# MAIL_USE_SSL = True
MAIL_USERNAME = os.environ.get('MAIL_USERNAME')
MAIL_PASSWORD = os.environ.get('MAIL_PASSWORD')

# administrator list
admin_acc = os.environ.get('MAIL_USERNAME')
ADMIN = admin_acc
# ADMINS = [admin_acc]
# MAIL_DEFAULT_SENDER = admin_acc


CELERY_BROKER_URL = 'redis://localhost:6379/0'
CELERY_RESULT_BACKEND = 'redis://localhost:6379/0'
