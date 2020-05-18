from . import main
from app import db, cors, bcrypt
from flask import render_template, request, url_for, redirect, flash

@main.route('/', methods=['GET'])
def good():
    return render_template('hello.html')