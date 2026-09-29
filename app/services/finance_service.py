from app.models.income import Income
from app.models.expense import Expense, ExpenseCategory
from app.models.budget import Budget
from app.models.goal import SavingsGoal
from sqlalchemy import extract
from sqlalchemy.sql import func
from app import db
import datetime

class FinanceService:
    @staticmethod
    def total_income(user_id, month=None, year=None):
        query = Income.query.filter_by(user_id=user_id)
        if month and year:
            query = query.filter(extract('month', Income.date) == month, extract('year', Income.date) == year)
        return sum(i.amount for i in query.all())
        
    @staticmethod
    def total_expenses(user_id, month=None, year=None):
        query = Expense.query.filter_by(user_id=user_id)
        if month and year:
            query = query.filter(extract('month', Expense.date) == month, extract('year', Expense.date) == year)
        return sum(e.amount for e in query.all())
        
    @staticmethod
    def total_savings(user_id, month=None, year=None):
        income = FinanceService.total_income(user_id, month, year)
        expenses = FinanceService.total_expenses(user_id, month, year)
        return income - expenses
        
    @staticmethod
    def savings_rate(user_id, month=None, year=None):
        income = FinanceService.total_income(user_id, month, year)
        if income == 0:
            return 0
        savings = FinanceService.total_savings(user_id, month, year)
        return (savings / income) * 100
        
    @staticmethod
    def category_expenses(user_id, month=None, year=None):
        query = db.session.query(ExpenseCategory.name, func.sum(Expense.amount).label('total')).\
            join(Expense, Expense.category_id == ExpenseCategory.id).\
            filter(Expense.user_id == user_id)
        
        if month and year:
            query = query.filter(extract('month', Expense.date) == month, extract('year', Expense.date) == year)
            
        results = query.group_by(ExpenseCategory.name).all()
        return {r[0]: r[1] for r in results}
        
    @staticmethod
    def budget_utilization(user_id, month, year):
        budgets = Budget.query.filter_by(user_id=user_id, month=month, year=year).all()
        utilization = []
        for budget in budgets:
            spent = db.session.query(func.sum(Expense.amount)).filter(
                Expense.user_id == user_id,
                Expense.category_id == budget.category_id,
                extract('month', Expense.date) == month,
                extract('year', Expense.date) == year
            ).scalar() or 0.0
            
            utilization.append({
                'category': budget.category.name,
                'budgeted': budget.allocated_amount,
                'spent': spent,
                'remaining': budget.allocated_amount - spent,
                'is_over': (budget.allocated_amount - spent) < 0
            })
        return utilization
