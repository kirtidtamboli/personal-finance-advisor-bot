from app import create_app, db
from app.models.expense import ExpenseCategory

def seed_categories():
    app = create_app('default')
    with app.app_context():
        # List of categories to add
        new_categories = [
            'Housing', 'Transportation', 'Food & Dining', 'Utilities',
            'Insurance', 'Healthcare', 'Saving, Investing & Debt Payments',
            'Personal Spending', 'Recreation & Entertainment', 'Miscellaneous',
            'Education', 'Gifts & Donations'
        ]
        
        added = 0
        for cat_name in new_categories:
            # Check if exists
            exists = ExpenseCategory.query.filter_by(name=cat_name, user_id=None).first()
            if not exists:
                new_cat = ExpenseCategory(name=cat_name, user_id=None)
                db.session.add(new_cat)
                added += 1
                
        db.session.commit()
        print(f"Added {added} new default categories.")

if __name__ == '__main__':
    seed_categories()
