from flask import Blueprint, render_template, redirect, url_for, flash, request
from flask_login import login_required, current_user
from app import db
from app.models.income import Income
from app.forms.finance_forms import IncomeForm
from sqlalchemy import extract
import datetime

income_bp = Blueprint('income', __name__, url_prefix='/income')

@income_bp.route('/', methods=['GET'])
@login_required
def index():
    incomes = Income.query.filter_by(user_id=current_user.id).order_by(Income.date.desc()).all()
    total = sum(i.amount for i in incomes)
    return render_template('income/index.html', incomes=incomes, total=total)

@income_bp.route('/add', methods=['GET', 'POST'])
@login_required
def add():
    form = IncomeForm()
    if form.validate_on_submit():
        income = Income(
            user_id=current_user.id,
            source=form.source.data,
            amount=form.amount.data,
            date=form.date.data,
            description=form.description.data
        )
        db.session.add(income)
        db.session.commit()
        flash('Income added successfully.', 'success')
        return redirect(url_for('income.index'))
    # Set default date to today
    if request.method == 'GET':
        form.date.data = datetime.date.today()
    return render_template('income/form.html', form=form, title="Add Income")

@income_bp.route('/<int:id>/edit', methods=['GET', 'POST'])
@login_required
def edit(id):
    income = Income.query.get_or_404(id)
    if income.user_id != current_user.id:
        flash('Access denied.', 'danger')
        return redirect(url_for('income.index'))
        
    form = IncomeForm()
    if form.validate_on_submit():
        income.source = form.source.data
        income.amount = form.amount.data
        income.date = form.date.data
        income.description = form.description.data
        db.session.commit()
        flash('Income updated successfully.', 'success')
        return redirect(url_for('income.index'))
    elif request.method == 'GET':
        form.source.data = income.source
        form.amount.data = income.amount
        form.date.data = income.date
        form.description.data = income.description
    return render_template('income/form.html', form=form, title="Edit Income")

@income_bp.route('/<int:id>/delete', methods=['POST'])
@login_required
def delete(id):
    income = Income.query.get_or_404(id)
    if income.user_id == current_user.id:
        db.session.delete(income)
        db.session.commit()
        flash('Income deleted.', 'success')
    return redirect(url_for('income.index'))
