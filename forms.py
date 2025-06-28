from flask_wtf import FlaskForm
from wtforms import StringField, PasswordField, SubmitField, IntegerField, TextAreaField, SelectField, FloatField, DateField, BooleanField
from wtforms.validators import DataRequired, Email, Length, EqualTo, NumberRange, Optional
from datetime import datetime

class RegistrationForm(FlaskForm):
    """Form for user registration"""
    username = StringField('Username', validators=[
        DataRequired(message='Username is required'),
        Length(min=3, max=80, message='Username must be between 3 and 80 characters')
    ])
    email = StringField('Email', validators=[
        DataRequired(message='Email is required'),
        Email(message='Please enter a valid email address')
    ])
    password = PasswordField('Password', validators=[
        DataRequired(message='Password is required'),
        Length(min=6, message='Password must be at least 6 characters long')
    ])
    confirm_password = PasswordField('Confirm Password', validators=[
        DataRequired(message='Please confirm your password'),
        EqualTo('password', message='Passwords must match')
    ])
    submit = SubmitField('Register')

class LoginForm(FlaskForm):
    """Form for user login"""
    username = StringField('Username', validators=[
        DataRequired(message='Username is required')
    ])
    password = PasswordField('Password', validators=[
        DataRequired(message='Password is required')
    ])
    submit = SubmitField('Login')

class WorkoutForm(FlaskForm):
    """Form for adding/editing workouts"""
    exercise_type = SelectField('Exercise Type', validators=[
        DataRequired(message='Please select an exercise type')
    ], choices=[])
    duration = IntegerField('Duration (minutes)', validators=[
        DataRequired(message='Duration is required'),
        NumberRange(min=1, max=1000, message='Duration must be between 1 and 1000 minutes')
    ])
    intensity = SelectField('Intensity', validators=[
        DataRequired(message='Please select intensity level')
    ], choices=[
        ('Low', 'Low'),
        ('Medium', 'Medium'),
        ('High', 'High')
    ])
    calories = IntegerField('Calories Burned', validators=[
        DataRequired(message='Calories burned is required'),
        NumberRange(min=1, max=5000, message='Calories must be between 1 and 5000')
    ])
    notes = TextAreaField('Notes (Optional)')
    date = DateField('Date', validators=[
        DataRequired(message='Date is required')
    ], default=datetime.utcnow)
    submit = SubmitField('Save Workout')

class MealForm(FlaskForm):
    """Form for adding/editing meals"""
    food_name = StringField('Food Name', validators=[
        DataRequired(message='Food name is required'),
        Length(max=200, message='Food name must be less than 200 characters')
    ])
    calories = IntegerField('Calories', validators=[
        DataRequired(message='Calories is required'),
        NumberRange(min=1, max=5000, message='Calories must be between 1 and 5000')
    ])
    protein = FloatField('Protein (grams)', validators=[
        DataRequired(message='Protein is required'),
        NumberRange(min=0, max=500, message='Protein must be between 0 and 500 grams')
    ])
    carbs = FloatField('Carbohydrates (grams)', validators=[
        DataRequired(message='Carbohydrates is required'),
        NumberRange(min=0, max=1000, message='Carbohydrates must be between 0 and 1000 grams')
    ])
    fats = FloatField('Fats (grams)', validators=[
        DataRequired(message='Fats is required'),
        NumberRange(min=0, max=200, message='Fats must be between 0 and 200 grams')
    ])
    meal_type = SelectField('Meal Type', validators=[
        DataRequired(message='Please select a meal type')
    ], choices=[
        ('Breakfast', 'Breakfast'),
        ('Lunch', 'Lunch'),
        ('Dinner', 'Dinner'),
        ('Snack', 'Snack')
    ])
    date = DateField('Date', validators=[
        DataRequired(message='Date is required')
    ], default=datetime.utcnow)
    submit = SubmitField('Save Meal')

class GoalForm(FlaskForm):
    """Form for adding/editing goals"""
    title = StringField('Goal Title', validators=[
        DataRequired(message='Goal title is required'),
        Length(max=200, message='Goal title must be less than 200 characters')
    ])
    goal_type = SelectField('Goal Type', validators=[
        DataRequired(message='Please select a goal type')
    ], choices=[
        ('calories', 'Calories Burned'),
        ('workouts', 'Number of Workouts'),
        ('weight', 'Weight Goal'),
        ('distance', 'Distance'),
        ('duration', 'Duration')
    ])
    target_value = FloatField('Target Value', validators=[
        DataRequired(message='Target value is required'),
        NumberRange(min=0.1, message='Target value must be greater than 0')
    ])
    unit = StringField('Unit', validators=[
        DataRequired(message='Unit is required')
    ])
    timeframe = SelectField('Timeframe', validators=[
        DataRequired(message='Please select a timeframe')
    ], choices=[
        ('daily', 'Daily'),
        ('weekly', 'Weekly'),
        ('monthly', 'Monthly')
    ])
    end_date = DateField('End Date (Optional)', validators=[
        Optional()
    ])
    submit = SubmitField('Save Goal')

class FilterForm(FlaskForm):
    """Form for filtering workouts and meals"""
    start_date = DateField('Start Date', validators=[Optional()])
    end_date = DateField('End Date', validators=[Optional()])
    exercise_type = SelectField('Exercise Type', validators=[Optional()], choices=[('', 'All Types')])
    meal_type = SelectField('Meal Type', validators=[Optional()], choices=[('', 'All Meals')])
    submit = SubmitField('Filter') 