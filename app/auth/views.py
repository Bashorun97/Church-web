from . import auth
from flask import render_template, redirect, request, url_for, flash, make_response
from app import db, cors, bcrypt
from app.extensions import emailcheck
#from sqlalchemy.exc import IntegrityError
from flask_login import login_required, login_user, logout_user, current_user
from .forms import (
    RegistrationForm, LoginForm, ChangePasswordForm, ResetPasswordForm,
    ResetPasswordRequestForm
)
from models import User, Article
from app.email import send_email

#A registered but unconfirmed user can only view auth and static routes
@auth.before_app_request
def before_request():
    if current_user.is_authenticated \
        and not current_user.confirmed \
        and request.blueprint != 'auth' \
        and request.endpoint != 'static' \
        and request.endpoint  != 'main.index':
        return redirect(url_for('auth.unconfirmed'))

@auth.route('/unconfirmed')
def unconfirmed():
    if current_user.is_anonymous or current_user.confirmed:
        return redirect(url_for('main.index'))
    return render_template('auth/unconfirmed.html')

@auth.route('/register', methods=['GET', 'POST'])
def registration():
    if current_user.is_authenticated:
        return redirect(url_for('main.index'))
    form = RegistrationForm()
    if form.validate_on_submit():
        user = User(
            name = form.name.data,
            surname = form.surname.data,
            username = form.username.data,
            email = form.email.data,
            password = form.password.data,
            telephone = form.telephone.data,
            house_address = form.house_address.data
        )
        db.session.add(user)
        db.session.commit()
        token = user.generate_json_web_confirmation_token()
        send_email(user.email, 'Confirm Your Account', 'auth/email/confirm', user=user, token=token)
        flash('Please check your mail inbox for a confirmation message before logging in')
        return redirect(url_for('auth.login'))
    return render_template('auth/registration.html', form=form)


@auth.route('/login', methods=['GET', 'POST'])
def login():
    if current_user.is_authenticated:
        flash('You\'re logged in already. Log out to relogin')
        return redirect(url_for('main.index'))
    form = LoginForm()
    if form.validate_on_submit():
        user = User.query.filter_by(username=form.username.data).first() or User.query.filter_by(email=form.username.data).first()
        if user is not None and user.verify_password(form.password.data):
            login_user(user, form.remember_me.data)
            next = request.args.get('next')
            if next is None or not next.startswith('/'):
                next = url_for('main.index')
            return redirect(next)
        flash('Invalid email or password.')
    return render_template('/auth/login.html', form=form)


@auth.route('/confirm/<token>')
@login_required
def confirm(token):
    if current_user.confirmed():
        return redirect(url_for('main.index'))
    if current_user.confirm_token(token):
        db.session.commit()
        flash('Congratulations! You have successfully confirmed your account')
    else:
        flash('Your confirmation link is expired')
    return redirect(url_for('main.index'))

@auth.route('/confirm')
@login_required
def resend_confirmation():
    token = current_user.generate_json_web_confirmation_token()
    send_email(current_user, 'Confirm Your Account', 'auth/email/confirm', user=current_user, token=token)
    flash('Please check your mail inbox for a confirmation message to complete your registration')
    return redirect(url_for('auth.login'))


@auth.route('/logout', methods=['GET', 'POST'])
@login_required
def logout():
    logout_user()
    return redirect(url_for('auth.login'))


@auth.route('change-password', methods=['GET', 'POST', 'PUT'])
@login_required
def change_password():
    form = ChangePasswordForm()
    if form.validate_on_submit():
        if current_user.verify_password(form.oldpassword.data):
            current_user.password = form.password.data
            db.session.add(current_user)
            db.session.commit()
            flash('Password successfully changed. Please re-login to continue accessing the site.')
            return redirect(url_for('auth.logout'))
        else:
            flash('Invalid old password is wrong')
    return render_template("auth/change_password.html", form=form)


@auth.route('/reset-password-request', methods=['GET', 'POST'])
def reset_password_request():
    if not current_user.is_anonymous:
        return redirect(url_for('main.index'))
    form  = ResetPasswordRequestForm()
    if form.validate_on_submit():
        user = User.query.filter_by(email=form.email.data.lower()).first()
        if user:
            token = current_user.generate_json_web_token_for_password_reset()
            send_mail(user.email, 'Password Reset', 'auth/email/reset_password',\
                user=user, token=token)
        flash('An email with instructions on how to reset your password has\
            been sent to your inbox')
        return redirect(url_for('auth.login'))
    return render_template('/auth/reset_password.html', form=form)

@auth.route('/reset-password/<token>', methods=['GET', 'PUT'])
def reset_password(token):
    if not current_user.is_anonymous:
        return redirect(url_for('main.index'))
    form = ResetPasswordForm()
    if form.validate_on_submit():
        if User.reset_password(token, form.password.data):
            db.session.commit()
            flash('Password successfully changed')
            return redirect(url_for('auth.login'))
        else:
            return redirect(url_for('main.index'))
    return render_template('auth/reset_password.html')