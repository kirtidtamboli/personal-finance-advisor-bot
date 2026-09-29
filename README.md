# Personal Finance Advisor Bot

An AI-powered personal finance management platform that allows individuals to manage income, expenses, budgets, savings, financial goals, analytics, and AI-powered financial recommendations.

## Project Overview
The Personal Finance Advisor Bot is designed for salaried professionals, students, freelancers, and household managers to track their finances and get AI-driven advice based on their spending habits, utilizing Google Gemini API.

## Key Features
- Record and manage monthly income and expenses
- Automatically track budget utilization
- Calculate monthly savings and savings rate
- Goal tracking (e.g., Emergency Fund)
- Financial Analytics Dashboard
- AI-Powered Recommendations (Gemini)
- Secure user authentication and data isolation

## Tech Stack
- **Backend:** Python, Flask, SQLAlchemy
- **Database:** SQLite (Development) / PostgreSQL (Production)
- **Frontend:** HTML5, CSS3 (Vanilla), JavaScript, Jinja2
- **AI Integration:** Google Gemini API
- **Testing:** Pytest

## Installation & Setup

1. Clone the repository:
   ```bash
   git clone https://github.com/kirtidtamboli/personal-finance-advisor-bot.git
   cd personal-finance-advisor-bot
   ```

2. Create a virtual environment and activate it:
   ```bash
   python -m venv venv
   # On Windows:
   venv\Scripts\activate
   # On Linux/macOS:
   source venv/bin/activate
   ```

3. Install dependencies:
   ```bash
   pip install -r requirements.txt
   ```

4. Configure environment variables:
   Copy `.env.example` to `.env` and update the values:
   ```bash
   cp .env.example .env
   ```

5. Initialize the database and run migrations:
   ```bash
   flask db init
   flask db migrate -m "Initial migration"
   flask db upgrade
   ```

6. Run the application:
   ```bash
   python run.py
   ```

## Live Demo
[Add deployed demo URL]
