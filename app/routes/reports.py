from flask import Blueprint, render_template, redirect, url_for, flash, request
from flask_login import login_required, current_user
from app import db
from app.models.report import FinancialReport
from app.services.finance_service import FinanceService
from app.services.ai_service import AIService
import datetime
import json

reports_bp = Blueprint('reports', __name__, url_prefix='/reports')

@reports_bp.route('/')
@login_required
def index():
    reports = FinancialReport.query.filter_by(user_id=current_user.id).order_by(FinancialReport.year.desc(), FinancialReport.month.desc()).all()
    return render_template('reports/index.html', reports=reports)

@reports_bp.route('/generate', methods=['POST'])
@login_required
def generate():
    month = request.form.get('month', type=int)
    year = request.form.get('year', type=int)
    
    if not month or not year:
        flash('Invalid month or year.', 'danger')
        return redirect(url_for('reports.index'))
        
    # Check if report already exists
    existing_report = FinancialReport.query.filter_by(user_id=current_user.id, month=month, year=year).first()
    
    total_income = FinanceService.total_income(current_user.id, month, year)
    total_expenses = FinanceService.total_expenses(current_user.id, month, year)
    total_savings = FinanceService.total_savings(current_user.id, month, year)
    savings_rate = FinanceService.savings_rate(current_user.id, month, year)
    
    # Get AI advice summary
    advice = AIService.get_financial_advice(current_user.id, month, year)
    summary_text = advice.get('summary', 'Summary not available.') if not advice.get('error') else advice.get('error')
    
    if existing_report:
        existing_report.total_income = total_income
        existing_report.total_expenses = total_expenses
        existing_report.total_savings = total_savings
        existing_report.savings_rate = savings_rate
        existing_report.generated_summary = summary_text
        db.session.commit()
        flash('Report updated successfully.', 'success')
        return redirect(url_for('reports.view', id=existing_report.id))
        
    report = FinancialReport(
        user_id=current_user.id,
        month=month,
        year=year,
        total_income=total_income,
        total_expenses=total_expenses,
        total_savings=total_savings,
        savings_rate=savings_rate,
        generated_summary=summary_text
    )
    
    db.session.add(report)
    db.session.commit()
    flash('Report generated successfully.', 'success')
    return redirect(url_for('reports.view', id=report.id))

@reports_bp.route('/<int:id>')
@login_required
def view(id):
    report = FinancialReport.query.get_or_404(id)
    if report.user_id != current_user.id:
        flash('Access denied.', 'danger')
        return redirect(url_for('reports.index'))
        
    cat_expenses = FinanceService.category_expenses(current_user.id, report.month, report.year)
    budgets = FinanceService.budget_utilization(current_user.id, report.month, report.year)
    
    return render_template('reports/view.html', report=report, cat_expenses=cat_expenses, budgets=budgets)
