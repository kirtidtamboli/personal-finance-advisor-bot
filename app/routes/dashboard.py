from flask import Blueprint, render_template
from flask_login import login_required, current_user
from app.services.finance_service import FinanceService
from app.models.goal import SavingsGoal
import datetime

dashboard = Blueprint('dashboard', __name__)

@dashboard.route('/')
def index():
    return render_template('dashboard/index.html')

@dashboard.route('/dashboard')
@login_required
def main_dashboard():
    now = datetime.date.today()
    month = now.month
    year = now.year
    
    total_income = FinanceService.total_income(current_user.id, month, year)
    total_expenses = FinanceService.total_expenses(current_user.id, month, year)
    total_savings = FinanceService.total_savings(current_user.id, month, year)
    savings_rate = FinanceService.savings_rate(current_user.id, month, year)
    
    cat_expenses = FinanceService.category_expenses(current_user.id, month, year)
    top_category = max(cat_expenses, key=cat_expenses.get) if cat_expenses else "None"
    top_category_amount = cat_expenses.get(top_category, 0)
    
    budgets = FinanceService.budget_utilization(current_user.id, month, year)
    goals = SavingsGoal.query.filter_by(user_id=current_user.id).all()
    
    return render_template(
        'dashboard/main.html',
        month=month,
        year=year,
        total_income=total_income,
        total_expenses=total_expenses,
        total_savings=total_savings,
        savings_rate=savings_rate,
        top_category=top_category,
        top_category_amount=top_category_amount,
        budgets=budgets,
        goals=goals,
        cat_expenses=cat_expenses
    )

