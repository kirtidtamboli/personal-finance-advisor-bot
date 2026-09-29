# Database

## Models
- **User**: Handles authentication and isolates user data.
- **Income**: Tracks income events with sources and amounts.
- **ExpenseCategory**: Groups expenses. Can be user-specific or system-wide (when `user_id` is null).
- **Expense**: Tracks individual expenses.
- **Budget**: Allocates limits to specific categories per month/year.
- **SavingsGoal**: Tracks long-term financial targets.
- **FinancialReport**: Stores generated monthly snapshots.

## Development vs Production
- **Local**: Uses SQLite for quick setup without a server requirement.
- **Production**: Designed to use PostgreSQL. Set the `DATABASE_URL` environment variable.
