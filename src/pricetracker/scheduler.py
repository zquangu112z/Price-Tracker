from pricetracker.celery_worker import celery_app
from pricetracker.task.check_price import say_hello, check


@celery_app.on_after_configure.connect
def setup_periodic_tasks(sender, **kwargs):
    # sender.add_periodic_task(2.0, say_hello.s(),
    #                          name='Say hello every 5 seconds')
    sender.add_periodic_task(5.0, check.s(),
                             name='Check price')
