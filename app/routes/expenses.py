from flask import Blueprint, render_template, redirect, url_for, flash, request
from flask_login import login_required, current_user
from app import db
from app.models.expense import Expense, ExpenseCategory
from app.forms.finance_forms import ExpenseForm, ExpenseCategoryForm
import datetime

expenses_bp = Blueprint('expenses', __name__, url_prefix='/expenses')

@expenses_bp.route('/', methods=['GET'])
@login_required
def index():
    expenses = Expense.query.filter_by(user_id=current_user.id).order_by(Expense.date.desc()).all()
    total = sum(e.amount for e in expenses)
    return render_template('expenses/index.html', expenses=expenses, total=total)

@expenses_bp.route('/add', methods=['GET', 'POST'])
@login_required
def add():
    form = ExpenseForm()
    categories = ExpenseCategory.query.filter((ExpenseCategory.user_id == current_user.id) | (ExpenseCategory.user_id.is_(None))).all()
    form.category_id.choices = [(c.id, c.name) for c in categories]
    
    if form.validate_on_submit():
        expense = Expense(
            user_id=current_user.id,
            category_id=form.category_id.data,
            amount=form.amount.data,
            date=form.date.data,
            description=form.description.data,
            payment_method=form.payment_method.data
        )
        db.session.add(expense)
        db.session.commit()
        flash('Expense added successfully.', 'success')
        return redirect(url_for('expenses.index'))
        
    if request.method == 'GET':
        form.date.data = datetime.date.today()
    return render_template('expenses/form.html', form=form, title="Add Expense")

@expenses_bp.route('/<int:id>/edit', methods=['GET', 'POST'])
@login_required
def edit(id):
    expense = Expense.query.get_or_404(id)
    if expense.user_id != current_user.id:
        flash('Access denied.', 'danger')
        return redirect(url_for('expenses.index'))
        
    form = ExpenseForm()
    categories = ExpenseCategory.query.filter((ExpenseCategory.user_id == current_user.id) | (ExpenseCategory.user_id.is_(None))).all()
    form.category_id.choices = [(c.id, c.name) for c in categories]
    
    if form.validate_on_submit():
        expense.category_id = form.category_id.data
        expense.amount = form.amount.data
        expense.date = form.date.data
        expense.description = form.description.data
        expense.payment_method = form.payment_method.data
        db.session.commit()
        flash('Expense updated successfully.', 'success')
        return redirect(url_for('expenses.index'))
    elif request.method == 'GET':
        form.category_id.data = expense.category_id
        form.amount.data = expense.amount
        form.date.data = expense.date
        form.description.data = expense.description
        form.payment_method.data = expense.payment_method
    return render_template('expenses/form.html', form=form, title="Edit Expense")

@expenses_bp.route('/<int:id>/delete', methods=['POST'])
@login_required
def delete(id):
    expense = Expense.query.get_or_404(id)
    if expense.user_id == current_user.id:
        db.session.delete(expense)
        db.session.commit()
        flash('Expense deleted.', 'success')
    return redirect(url_for('expenses.index'))

@expenses_bp.route('/categories', methods=['GET', 'POST'])
@login_required
def categories():
    form = ExpenseCategoryForm()
    if form.validate_on_submit():
        category = ExpenseCategory(name=form.name.data, user_id=current_user.id)
        db.session.add(category)
        db.session.commit()
        flash('Category created.', 'success')
        return redirect(url_for('expenses.categories'))
        
    user_categories = ExpenseCategory.query.filter_by(user_id=current_user.id).all()
    default_categories = ExpenseCategory.query.filter_by(user_id=None).all()
    return render_template('expenses/categories.html', form=form, user_categories=user_categories, default_categories=default_categories)
