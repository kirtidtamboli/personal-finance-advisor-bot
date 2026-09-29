# AI Integration

## Gemini Integration
The application uses the Google Gemini API (via `google-genai` package) to act as a financial advisor.

## AIService
The logic lives in `app/services/ai_service.py`. It accepts strict JSON financial records:
- Income
- Expenses
- Budget status
- Goal status

## Principles
1. **Deterministic Math First**: Fundamental calculations (savings rate, totals) are done in Python, NOT by the AI.
2. **Context Window**: Only essential numerical data is serialized and sent in the prompt to reduce latency and token usage.
3. **Structured Outputs**: The prompt instructs Gemini to output strict JSON which the application parses and renders.
4. **Failsafe**: If the API fails or the key is missing, a friendly fallback message is shown without breaking the app.
