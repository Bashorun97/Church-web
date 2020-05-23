from . import main
from app import db, cors, bcrypt
from flask import render_template, request, url_for, redirect, flash

@main.route('/<name>', methods=['GET'])
def good(name):
    return render_template('main/index.html', name=name)