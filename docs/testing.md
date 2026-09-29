# Testing

## Pytest Suite
We use Pytest to execute tests covering:
- Authentication
- Database Models (Income, Expense, etc.)
- Services (`FinanceService`)

## Running Tests
Ensure your virtual environment is active.
```bash
# On Windows
$env:PYTHONPATH="."
pytest tests/

# On Linux/Mac
PYTHONPATH="." pytest tests/
```

## Security Testing
- `test_security_user_isolation` ensures that one user cannot edit/view the records of another user.
