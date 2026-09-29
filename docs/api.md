# API Design

While this is primarily a server-side rendered application, it is structured to support RESTful API endpoints in the future by reusing the `FinanceService`.

Current integrations:
- `FinanceService.category_expenses()` and `budget_utilization()` return structured dictionary data that can be easily jsonified for an API endpoint if needed.
- `AIService` already consumes JSON data to talk to the Gemini API.
