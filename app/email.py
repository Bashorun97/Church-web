from threading import Thread
from flask import current_app, render_template
from flask_mail import Message
from . import mail

def asynchronously_send_email(app, msg):
    with app.context():
        mail.send(msg)

def send_email(to, subject, template, **kwargs):
    app = current_app._get_current_object()
    msg = Message(app.config['RCCG_HOS_MAIL_SUBJECT_PREFIX'] + ' ' + subject,\
        sender=app.config['RCCG_HOS_MAIL_SENDER'], recipients=[to])
    msg.body = render_template(template + '.txt', **kwargs)
    msg.body = render_template(template + '.html', **kwargs)
    thr = Thread(target=asynchronously_send_email, args=[app, msg])
    thr.start()
    return thr
