from . import auth
from flask import render_template, redirect, request, url_for, flash, make_response
from app import db, cors, bcrypt
from app.extensions import emailcheck
from sqlalchemy.exc import IntegrityError
from flask_login import login_required, login_user, logout_user, current_user
from .forms import (
    RegistrationForm, LoginForm, ChangePasswordForm, ResetPasswordForm,
    ResetPasswordRequestForm
)
from models import User, Article


@auth.route('/register', methods=['GET', 'POST'])
def registration():
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
        flash('Please check the confirmation email has been sent to you for complete registration')
        return redirect(url_for('auth.login'))
    return render_template('auth/registration.html', form=form)

@auth.route('/login', methods=['GET', 'POST'])
def login():
    form = LoginForm()
    if form.validate_on_submit():
        user = User.query.filter_by(username=form.username.data).first() or User.query.filter_by(email=form.username.data).first()
        print(user)
        if user is not None and user.verify_password(form.password.data):
            login_user(user, form.remember_me.data)
            next = request.args.get('next')
            if next is None or not next.startswith('/'):
                next = url_for('main.index')
            return redirect(next)
        flash('Invalid email or password.')
    return render_template('/auth/login.html', form=form)

@auth.route('/logout', methods=['GET', 'POST'])
def logout():
    logout_user()
    flash('You have been logged out.')
    return redirect(url_for('main.index'))

@auth.route('change-password', methods=['GET', 'POST'])
def change_password():
    form = ChangePasswordForm()
    return render_template('/auth/change_password.html', form=form)
    
@auth.route('/reset-password', methods=['GET', 'POST'])
def reset_password():
    form = ResetPasswordForm()
    return render_template('/auth/change_password.html', form=form)

@auth.route('/reset-password-request', methods=['GET', 'POST'])
def reset_password_request():
    form  = ResetPasswordRequestForm()
    return render_template('/auth/reset_password.html', form=form)