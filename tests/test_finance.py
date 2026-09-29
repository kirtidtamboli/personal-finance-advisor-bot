import pytest
from app import db
from app.models.income import Income
from app.models.expense import Expense, ExpenseCategory
from app.models.budget import Budget
from app.models.goal import SavingsGoal
from app.services.finance_service import FinanceService
import datetime

def login(client, email, password):
    return client.post('/login', data={'email': email, 'password': password}, follow_redirects=True)

def test_add_income(client, test_user, app):
    login(client, 'test@example.com', 'password123')
    response = client.post('/income/add', data={
        'source': 'Salary',
        'amount': 5000.0,
        'date': datetime.date.today().strftime('%Y-%m-%d'),
        'description': 'Monthly salary'
    }, follow_redirects=True)
    assert b'Income added successfully' in response.data
    
    with app.app_context():
        income = Income.query.filter_by(user_id=test_user.id).first()
        assert income.amount == 5000.0

def test_finance_service_calculations(app, test_user):
    with app.app_context():
        # Setup data
        inc = Income(user_id=test_user.id, source='Job', amount=1000.0, date=datetime.date(2026, 1, 15))
        cat = ExpenseCategory(user_id=test_user.id, name='Food')
        db.session.add_all([inc, cat])
        db.session.commit()
        
        exp = Expense(user_id=test_user.id, category_id=cat.id, amount=300.0, date=datetime.date(2026, 1, 16))
        db.session.add(exp)
        db.session.commit()
        
        # Test calculations
        assert FinanceService.total_income(test_user.id, 1, 2026) == 1000.0
        assert FinanceService.total_expenses(test_user.id, 1, 2026) == 300.0
        assert FinanceService.total_savings(test_user.id, 1, 2026) == 700.0
        assert FinanceService.savings_rate(test_user.id, 1, 2026) == 70.0

def test_budget_utilization(app, test_user):
    with app.app_context():
        cat = ExpenseCategory(user_id=test_user.id, name='Rent')
        db.session.add(cat)
        db.session.commit()
        
        budget = Budget(user_id=test_user.id, category_id=cat.id, month=1, year=2026, allocated_amount=1000.0)
        db.session.add(budget)
        
        exp1 = Expense(user_id=test_user.id, category_id=cat.id, amount=400.0, date=datetime.date(2026, 1, 10))
        exp2 = Expense(user_id=test_user.id, category_id=cat.id, amount=700.0, date=datetime.date(2026, 1, 15))
        db.session.add_all([exp1, exp2])
        db.session.commit()
        
        utils = FinanceService.budget_utilization(test_user.id, 1, 2026)
        rent_util = utils[0]
        
        assert rent_util['budgeted'] == 1000.0
        assert rent_util['spent'] == 1100.0
        assert rent_util['remaining'] == -100.0
        assert rent_util['is_over'] == True

def test_security_user_isolation(client, app, test_user):
    with app.app_context():
        from app.models.user import User
        user2 = User(name="User 2", email="user2@example.com")
        user2.set_password("password123")
        db.session.add(user2)
        db.session.commit()
        
        inc = Income(user_id=user2.id, source='Secret', amount=9999.0, date=datetime.date.today())
        db.session.add(inc)
        db.session.commit()
        inc_id = inc.id
        
    login(client, 'test@example.com', 'password123')
    
    # Try to edit user2's income
    response = client.get(f'/income/{inc_id}/edit', follow_redirects=True)
    assert b'Access denied' in response.data
