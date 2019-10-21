from threading import Thread

from flask import current_app
from flask import render_template
from flask_mail import Message

from app import mail


def send_async_email(msg, app):
    with app.app_context():
        mail.send(msg)


def send_email(to, subject, template, *args, **kwargs):
    app = current_app._get_current_object()
    msg = Message(f'{app.config["APPLICATION_MAIL_SUBJECT_PREFIX"]} {subject}',
                  sender=app.config["ADMINS"][0],
                  recipients=[to])
    msg.body = render_template(f'{template}.txt', **kwargs)
    msg.html = render_template(f'{template}.html', **kwargs)
    thr = Thread(target=send_async_email, args=(msg, app))
    thr.start()
    return thr
