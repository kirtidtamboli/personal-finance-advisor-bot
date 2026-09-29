from flask import Blueprint, render_template, redirect, url_for, flash, request
from flask_login import login_required, current_user
from app import db
from app.models.goal import SavingsGoal
from app.forms.finance_forms import SavingsGoalForm

goals_bp = Blueprint('goals', __name__, url_prefix='/goals')

@goals_bp.route('/', methods=['GET'])
@login_required
def index():
    goals = SavingsGoal.query.filter_by(user_id=current_user.id).all()
    
    goal_data = []
    for goal in goals:
        percentage = (goal.current_amount / goal.target_amount * 100) if goal.target_amount > 0 else 0
        percentage = min(percentage, 100) # Cap at 100% for display
        goal_data.append({
            'goal': goal,
            'percentage': percentage
        })
        
    return render_template('goals/index.html', goal_data=goal_data)

@goals_bp.route('/add', methods=['GET', 'POST'])
@login_required
def add():
    form = SavingsGoalForm()
    if form.validate_on_submit():
        goal = SavingsGoal(
            user_id=current_user.id,
            name=form.name.data,
            target_amount=form.target_amount.data,
            current_amount=form.current_amount.data,
            deadline=form.deadline.data
        )
        db.session.add(goal)
        db.session.commit()
        flash('Savings goal created successfully.', 'success')
        return redirect(url_for('goals.index'))
        
    return render_template('goals/form.html', form=form, title="Create Savings Goal")

@goals_bp.route('/<int:id>/edit', methods=['GET', 'POST'])
@login_required
def edit(id):
    goal = SavingsGoal.query.get_or_404(id)
    if goal.user_id != current_user.id:
        flash('Access denied.', 'danger')
        return redirect(url_for('goals.index'))
        
    form = SavingsGoalForm()
    if form.validate_on_submit():
        goal.name = form.name.data
        goal.target_amount = form.target_amount.data
        goal.current_amount = form.current_amount.data
        goal.deadline = form.deadline.data
        db.session.commit()
        flash('Savings goal updated successfully.', 'success')
        return redirect(url_for('goals.index'))
    elif request.method == 'GET':
        form.name.data = goal.name
        form.target_amount.data = goal.target_amount
        form.current_amount.data = goal.current_amount
        form.deadline.data = goal.deadline
        
    return render_template('goals/form.html', form=form, title="Edit Savings Goal")

@goals_bp.route('/<int:id>/delete', methods=['POST'])
@login_required
def delete(id):
    goal = SavingsGoal.query.get_or_404(id)
    if goal.user_id == current_user.id:
        db.session.delete(goal)
        db.session.commit()
        flash('Savings goal deleted.', 'success')
    return redirect(url_for('goals.index'))
