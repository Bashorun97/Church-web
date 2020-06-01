from . import main
from app import db, cors, bcrypt
from flask import render_template, request, url_for, redirect, flash
from .forms import EditProfileForm
from flask_login import current_user, login_required
from models import User


@main.route('/', methods=['GET'])
def index():
    return render_template('/main/index.html')

@main.route('/profile/<username>')
@login_required
def profile(username):
    user = User.query.filter_by(username=username).first()
    return render_template('/main/profile.html', user=user)

@main.route('/edit-profile/<username>', methods = ['GET', 'POST'])
@login_required
def edit_profile(username):
    user = User.query.filter_by(username = username).first()
    form = EditProfileForm()
    if form.validate_on_submit():
        user.name = form.name.data
        user.surname = form.surname.data
        user.username = form.username.data
        user.house_address = form.house_address.data

        db.session.add(user)
        db.session.commit()
        flash('You have successfully updated your profile')
        return redirect(url_for('main.index'))
    return render_template('main/edit_profile.html', form=form, user=user)