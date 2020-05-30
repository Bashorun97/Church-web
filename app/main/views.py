from . import main
from app import db, cors, bcrypt
from flask import render_template, request, url_for, redirect, flash
from .forms import LoginForm
from flask_login import current_user, login_required


@main.route('/', methods=['GET'])
def index():
    form = LoginForm()
    return render_template('/main/index.html')

@main.route('/profile')
@login_required
def profile():
    return render_template('/main/profile.html')