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
