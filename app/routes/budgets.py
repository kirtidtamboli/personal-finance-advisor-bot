from flask import Blueprint, render_template, redirect, url_for, flash, request
from flask_login import login_required, current_user
from app import db
from app.models.budget import Budget
from app.models.expense import ExpenseCategory, Expense
from app.forms.finance_forms import BudgetForm
import datetime
from sqlalchemy import extract

budgets_bp = Blueprint('budgets', __name__, url_prefix='/budgets')

@budgets_bp.route('/', methods=['GET'])
@login_required
def index():
    current_month = datetime.date.today().month
    current_year = datetime.date.today().year
    
    month = request.args.get('month', current_month, type=int)
    year = request.args.get('year', current_year, type=int)
    
    budgets = Budget.query.filter_by(user_id=current_user.id, month=month, year=year).all()
    
    # Calculate utilization
    budget_data = []
    for budget in budgets:
        # Get actual spending for this category in the given month/year
        spent = db.session.query(db.func.sum(Expense.amount)).filter(
            Expense.user_id == current_user.id,
            Expense.category_id == budget.category_id,
            extract('month', Expense.date) == month,
            extract('year', Expense.date) == year
        ).scalar() or 0.0
        
        remaining = budget.allocated_amount - spent
        percentage = (spent / budget.allocated_amount * 100) if budget.allocated_amount > 0 else 0
        
        budget_data.append({
            'budget': budget,
            'spent': spent,
            'remaining': remaining,
            'percentage': percentage,
            'is_over': remaining < 0
        })
        
    return render_template('budgets/index.html', budget_data=budget_data, month=month, year=year)

@budgets_bp.route('/add', methods=['GET', 'POST'])
@login_required
def add():
    form = BudgetForm()
    categories = ExpenseCategory.query.filter((ExpenseCategory.user_id == current_user.id) | (ExpenseCategory.user_id.is_(None))).all()
    form.category_id.choices = [(c.id, c.name) for c in categories]
    
    if request.method == 'GET':
        form.month.data = datetime.date.today().month
        form.year.data = datetime.date.today().year
        
    if form.validate_on_submit():
        # Check if budget already exists for this category, month, year
        existing = Budget.query.filter_by(
            user_id=current_user.id, 
            category_id=form.category_id.data,
            month=form.month.data,
            year=form.year.data
        ).first()
        
        if existing:
            flash('Budget for this category and month already exists.', 'warning')
            return redirect(url_for('budgets.index', month=form.month.data, year=form.year.data))
            
        budget = Budget(
            user_id=current_user.id,
            category_id=form.category_id.data,
            month=form.month.data,
            year=form.year.data,
            allocated_amount=form.allocated_amount.data
        )
        db.session.add(budget)
        db.session.commit()
        flash('Budget created successfully.', 'success')
        return redirect(url_for('budgets.index', month=form.month.data, year=form.year.data))
        
    return render_template('budgets/form.html', form=form, title="Create Budget")

@budgets_bp.route('/<int:id>/edit', methods=['GET', 'POST'])
@login_required
def edit(id):
    budget = Budget.query.get_or_404(id)
    if budget.user_id != current_user.id:
        flash('Access denied.', 'danger')
        return redirect(url_for('budgets.index'))
        
    form = BudgetForm()
    categories = ExpenseCategory.query.filter((ExpenseCategory.user_id == current_user.id) | (ExpenseCategory.user_id.is_(None))).all()
    form.category_id.choices = [(c.id, c.name) for c in categories]
    
    if form.validate_on_submit():
        budget.category_id = form.category_id.data
        budget.month = form.month.data
        budget.year = form.year.data
        budget.allocated_amount = form.allocated_amount.data
        db.session.commit()
        flash('Budget updated successfully.', 'success')
        return redirect(url_for('budgets.index', month=budget.month, year=budget.year))
    elif request.method == 'GET':
        form.category_id.data = budget.category_id
        form.month.data = budget.month
        form.year.data = budget.year
        form.allocated_amount.data = budget.allocated_amount
        
    return render_template('budgets/form.html', form=form, title="Edit Budget")

@budgets_bp.route('/<int:id>/delete', methods=['POST'])
@login_required
def delete(id):
    budget = Budget.query.get_or_404(id)
    if budget.user_id == current_user.id:
        db.session.delete(budget)
        db.session.commit()
        flash('Budget deleted.', 'success')
    return redirect(url_for('budgets.index'))
