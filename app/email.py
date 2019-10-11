from app import mail

from flask import current_app

from flask_mail import Message

from threading import Thread


def send_async_email(msg, app):
    with app.app_context():
        mail.send(msg)


def send_email(subject, sender, recipients, text_body, html_body):
    msg = Message(subject, sender=sender, recipients=recipients)
    msg.body = text_body
    msg.html = html_body
    Thread(target=send_async_email, args=(msg, current_app._get_current_object())).start()