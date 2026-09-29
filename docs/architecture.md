# Architecture

## Overview
The application uses the Flask Application Factory pattern, meaning the app is created using a `create_app()` function. This prevents circular imports and makes testing easier.

## Patterns
- **Blueprints**: The application is divided into logical blueprints (e.g., auth, dashboard, income, expenses, budgets, goals, reports, ai).
- **Service Layer**: The `app/services` directory contains business logic (e.g., `FinanceService`, `AIService`). This keeps the routes thin and makes logic reusable.
- **Data Access**: We use SQLAlchemy ORM.

## Why Flask?
Flask was chosen for its flexibility, simplicity, and modularity, making it an excellent choice for a mid-sized web application that requires custom service layers like AI integration.
