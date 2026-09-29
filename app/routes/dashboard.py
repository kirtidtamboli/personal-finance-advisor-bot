from flask import Blueprint, render_template

dashboard = Blueprint('dashboard', __name__)

@dashboard.route('/')
def index():
    return "Landing Page"

@dashboard.route('/dashboard')
def main_dashboard():
    return "Dashboard Page"
