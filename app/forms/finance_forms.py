from flask_wtf import FlaskForm
from wtforms import StringField, FloatField, DateField, SelectField, SubmitField
from wtforms.validators import DataRequired, NumberRange, Length

class IncomeForm(FlaskForm):
    source = StringField('Income Source', validators=[DataRequired(), Length(max=100)])
    amount = FloatField('Amount', validators=[DataRequired(), NumberRange(min=0.01)])
    date = DateField('Date', validators=[DataRequired()])
    description = StringField('Description', validators=[Length(max=255)])
    submit = SubmitField('Save Income')

class ExpenseCategoryForm(FlaskForm):
    name = StringField('Category Name', validators=[DataRequired(), Length(max=100)])
    submit = SubmitField('Save Category')

class ExpenseForm(FlaskForm):
    category_id = SelectField('Category', coerce=int, validators=[DataRequired()])
    amount = FloatField('Amount', validators=[DataRequired(), NumberRange(min=0.01)])
    date = DateField('Date', validators=[DataRequired()])
    description = StringField('Description', validators=[Length(max=255)])
    payment_method = StringField('Payment Method', validators=[Length(max=50)])
    submit = SubmitField('Save Expense')

class BudgetForm(FlaskForm):
    category_id = SelectField('Category', coerce=int, validators=[DataRequired()])
    month = SelectField('Month', coerce=int, choices=[(i, str(i)) for i in range(1, 13)], validators=[DataRequired()])
    year = SelectField('Year', coerce=int, choices=[(i, str(i)) for i in range(2020, 2030)], validators=[DataRequired()])
    allocated_amount = FloatField('Allocated Amount', validators=[DataRequired(), NumberRange(min=0.0)])
    submit = SubmitField('Save Budget')

class SavingsGoalForm(FlaskForm):
    name = StringField('Goal Name', validators=[DataRequired(), Length(max=100)])
    target_amount = FloatField('Target Amount', validators=[DataRequired(), NumberRange(min=0.01)])
    current_amount = FloatField('Current Amount', default=0.0, validators=[NumberRange(min=0.0)])
    deadline = DateField('Deadline (Optional)', validators=[])
    submit = SubmitField('Save Goal')
