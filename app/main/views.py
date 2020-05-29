from . import main
from app import db, cors, bcrypt
from flask import render_template, request, url_for, redirect, flash
from .forms import LoginForm


@main.route('/', methods=['GET'])
def index():
    form = LoginForm()
    return render_template('/main/index.html')