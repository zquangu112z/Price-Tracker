from celery import Celery

app = Celery(__name__,
             broker='redis://localhost:6379/0',
             include=['pricetracker.task.check_price'])
