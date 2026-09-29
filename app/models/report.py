from app import db
from datetime import datetime

class FinancialReport(db.Model):
    __tablename__ = 'financial_reports'
    
    id = db.Column(db.Integer, primary_key=True)
    user_id = db.Column(db.Integer, db.ForeignKey('users.id'), nullable=False)
    month = db.Column(db.Integer, nullable=False)
    year = db.Column(db.Integer, nullable=False)
    total_income = db.Column(db.Float, nullable=False)
    total_expenses = db.Column(db.Float, nullable=False)
    total_savings = db.Column(db.Float, nullable=False)
    savings_rate = db.Column(db.Float, nullable=False)
    generated_summary = db.Column(db.Text, nullable=True)
    created_at = db.Column(db.DateTime, default=datetime.utcnow)
