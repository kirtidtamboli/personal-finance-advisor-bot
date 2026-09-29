import os
import json
from google import genai
from google.genai import types
from flask import current_app
from app.services.finance_service import FinanceService
from app.models.goal import SavingsGoal

class AIService:
    @staticmethod
    def get_financial_advice(user_id, month, year):
        # 1. Gather financial data
        total_income = FinanceService.total_income(user_id, month, year)
        total_expenses = FinanceService.total_expenses(user_id, month, year)
        savings = FinanceService.total_savings(user_id, month, year)
        cat_expenses = FinanceService.category_expenses(user_id, month, year)
        budgets = FinanceService.budget_utilization(user_id, month, year)
        goals = SavingsGoal.query.filter_by(user_id=user_id).all()
        
        # Serialize data
        budget_data = { b['category']: {'budgeted': b['budgeted'], 'spent': b['spent']} for b in budgets }
        goal_data = [{'name': g.name, 'target': g.target_amount, 'current': g.current_amount} for g in goals]
        
        financial_context = {
            "monthly_income": total_income,
            "monthly_expenses": total_expenses,
            "savings": savings,
            "category_spending": cat_expenses,
            "budgets": budget_data,
            "goals": goal_data
        }
        
        # 2. Prepare Prompt
        prompt = f"""
You are an expert Personal Finance Advisor. Analyze the following financial data and provide structured advice.
Do not invent any numbers. Only use the provided data.
Provide practical, actionable advice. Avoid guarantees. State clearly that this is for informational purposes.

Financial Data:
{json.dumps(financial_context, indent=2)}

Format the response strictly as a JSON object with the following keys:
- summary (string): A brief summary of the financial situation.
- financial_health (string): "Excellent", "Good", "Fair", or "Poor", with a short explanation.
- overspending_categories (list of strings): Categories where spending exceeds budget.
- budget_recommendations (list of strings): Actionable budget advice.
- saving_recommendations (list of strings): How to improve savings.
- goal_recommendations (list of strings): Advice on reaching savings goals.
- emergency_fund_guidance (string): Specific advice on emergency funds.
- next_month_actions (list of strings): 3 to 5 clear actions for next month.
"""

        # 3. Call Gemini
        api_key = current_app.config.get('GEMINI_API_KEY')
        if not api_key:
            return {"error": "AI insights are temporarily unavailable (Missing API Key). Your financial calculations and tracking are still available."}
            
        try:
            client = genai.Client(api_key=api_key)
            response = client.models.generate_content(
                model='gemini-2.5-flash',
                contents=prompt,
                config=types.GenerateContentConfig(
                    response_mime_type="application/json",
                ),
            )
            return json.loads(response.text)
        except Exception as e:
            # Fallback failsafe
            return {"error": f"AI insights are temporarily unavailable. Your financial calculations and tracking are still available. (Error: {str(e)})"}
