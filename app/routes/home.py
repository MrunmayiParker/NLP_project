# app/routes/home.py

from flask import Blueprint, render_template
from flask_login import login_required

main_bp = Blueprint('main', __name__)

@main_bp.route('/')
def home():
    return render_template('home.html')

@main_bp.route('/search')
@login_required
def search():
    return render_template('search.html')

@main_bp.route('/chat')
@login_required
def chat():
    return render_template('chat.html')

@main_bp.route('/upload')
@login_required
def upload():
    return render_template('upload.html')
