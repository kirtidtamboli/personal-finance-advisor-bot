# Personal Finance Advisor Bot

An AI-powered personal finance management platform that helps individuals manage income, expenses, budgets, savings, financial goals, analytics, and receive AI-powered financial recommendations.

**GitHub Repository:** [https://github.com/kirtidtamboli/personal-finance-advisor-bot](https://github.com/kirtidtamboli/personal-finance-advisor-bot)
**Live Demo:** [Add deployed demo URL]

## 📊 Project Metrics
- **Major Modules:** Authentication, Income/Expense Tracking, Budgeting, Goal Tracking, AI Insights, Monthly Reports
- **Supported Databases:** SQLite (Local/Dev) & PostgreSQL (Production)
- **AI Integration:** Google Gemini API (gemini-2.5-flash)
- **Test Suite:** Pytest (Authentication, Finance logic, User isolation)

## ✨ Key Features
- **Income & Expense Management:** Track daily transactions with categories.
- **Budgeting System:** Set categorical limits and monitor utilization.
- **Savings Goals:** Track progress toward financial targets (e.g., Emergency Fund).
- **Financial Analytics Dashboard:** Visualize spending with modern charts (Chart.js).
- **AI-Powered Advisor:** Context-aware financial recommendations using Google Gemini.
- **Monthly Reports:** Generate and preserve snapshots of financial performance.

## 🛠 Tech Stack
- **Backend:** Python, Flask, SQLAlchemy ORM
- **Database:** SQLite / PostgreSQL
- **Frontend:** HTML5, CSS3, JavaScript (Vanilla), Jinja2 Templating
- **AI Integration:** Google Gemini API
- **Testing:** Pytest

## 📸 Screenshots
*(See `docs/screenshots/` for full images)*
- [Dashboard Placeholder]
- [Income/Expense Placeholder]
- [AI Advisor Placeholder]

## 🚀 Installation & Setup

1. **Clone the repository:**
   ```bash
   git clone https://github.com/kirtidtamboli/personal-finance-advisor-bot.git
   cd personal-finance-advisor-bot
   ```

2. **Create a virtual environment:**
   ```bash
   python -m venv venv
   # Windows:
   venv\Scripts\activate
   # Linux/Mac:
   source venv/bin/activate
   ```

3. **Install dependencies:**
   ```bash
   pip install -r requirements.txt
   ```

4. **Environment Variables:**
   ```bash
   cp .env.example .env
   # Edit .env and add your GEMINI_API_KEY
   ```

5. **Initialize Database:**
   ```bash
   flask db init
   flask db migrate -m "Initial migration"
   flask db upgrade
   ```

6. **Run the app:**
   ```bash
   python run.py
   ```

## 🧪 Testing
Run the comprehensive test suite using Pytest:
```bash
# Windows
$env:PYTHONPATH="."
pytest tests/
```

## 🌐 Demo & Ngrok Deployment
To run a local public demo:
1. Start the Flask server: `python run.py`
2. In a separate terminal run: `ngrok http 5000`
3. Access via the provided `https://*.ngrok.io` link.

## Demo Video Link
https://drive.google.com/file/d/1IWzu3noswOBVfgx4LeuFMykp4c09Y5jE/view?usp=drivesdk

## 📚 Documentation
For detailed insights into design decisions, see the `docs/` folder:
- [Architecture](docs/architecture.md)
- [Database](docs/database.md)
- [API](docs/api.md)
- [AI Integration](docs/ai.md)
- [Testing](docs/testing.md)
- [Deployment](docs/deployment.md)

## ⚠️ Disclaimer
This application provides informational guidance and is not a substitute for a qualified financial professional. It does not make guaranteed investment promises.
