from flask import Blueprint, render_template

ai_bp = Blueprint('ai', __name__, url_prefix='/ai')

@ai_bp.route('/advice')
def advice():
    return render_template('ai/advice.html')
