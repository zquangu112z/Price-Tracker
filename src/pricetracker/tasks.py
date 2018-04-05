from .base import celery
import logging as logger
# from flask_mail import Mail, Message


@celery.task
def send_async_email(msg):
    """Background task to send an email with Flask-Mail."""
    # mail = Mail()
    # msg = Message("this is a message",
    #               sender=app.config['ADMIN'],
    #               recipients="zquangu112z@gmail.com")
    # mail.send(msg)
    logger.warning(">>>>>>>>>>>>>>>>a new message<<<<<<<<<<<<<<<<")


@celery.on_after_configure.connect
def setup_periodic_tasks(sender, **kwargs):
    # Calls test('hello') every 5 seconds.
    sender.add_periodic_task(5.0, send_async_email.s('hello'),
                             name='add every 5')
