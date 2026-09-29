from flask import Blueprint, render_template, request
from flask_login import login_required, current_user
from app.services.ai_service import AIService
import datetime

ai_bp = Blueprint('ai', __name__, url_prefix='/ai')

@ai_bp.route('/advice')
@login_required
def advice():
    now = datetime.date.today()
    month = request.args.get('month', now.month, type=int)
    year = request.args.get('year', now.year, type=int)
    
    advice_data = AIService.get_financial_advice(current_user.id, month, year)
    
    return render_template('ai/advice.html', advice=advice_data, month=month, year=year)
