from . import auth
from app import db, cors, bcrypt
from flask import render_template, request, url_for, redirect, flash
from flask_login import login_required, login_user, logout_user, current_user

@auth.route('/')
def hello():
    return '<h1>Hello world</h1>'