from flask import Blueprint, render_template
from flask_login import login_required, current_user

dashboard = Blueprint('dashboard', __name__)

@dashboard.route('/')
def index():
    return render_template('dashboard/index.html')

@dashboard.route('/dashboard')
@login_required
def main_dashboard():
    return render_template('dashboard/main.html')

