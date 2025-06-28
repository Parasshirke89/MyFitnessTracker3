from flask import Blueprint, render_template
from flask_login import login_required, current_user
from datetime import datetime, timedelta
from models.workout import Workout
from models.meal import Meal
from models.goal import Goal

# Create dashboard blueprint
dashboard = Blueprint('dashboard', __name__)

@dashboard.route('/')
@dashboard.route('/dashboard')
@login_required
def index():
    """Main dashboard view with user statistics and charts"""
    
    # Get current date and calculate date ranges
    today = datetime.now()
    start_of_week = today - timedelta(days=today.weekday())
    start_of_week = start_of_week.replace(hour=0, minute=0, second=0, microsecond=0)
    start_of_month = today.replace(day=1, hour=0, minute=0, second=0, microsecond=0)
    
    # Get user statistics
    total_workouts = current_user.get_total_workouts()
    calories_burned_week = current_user.get_calories_burned_this_week()
    calories_burned_month = current_user.get_calories_burned_this_month()
    
    # Get recent workouts (last 7 days)
    recent_workouts = Workout.query.filter(
        Workout.user_id == current_user.id,
        Workout.date >= start_of_week
    ).order_by(Workout.date.desc()).limit(5).all()
    
    # Get recent meals (last 7 days)
    recent_meals = Meal.query.filter(
        Meal.user_id == current_user.id,
        Meal.date >= start_of_week
    ).order_by(Meal.date.desc()).limit(5).all()
    
    # Get active goals
    active_goals = Goal.query.filter(
        Goal.user_id == current_user.id,
        Goal.is_active == True
    ).all()
    
    # Calculate daily calories for the past 7 days for chart
    daily_calories_data = []
    for i in range(7):
        date = start_of_week + timedelta(days=i)
        end_date = date + timedelta(days=1)
        
        # Get calories burned on this day
        day_workouts = Workout.query.filter(
            Workout.user_id == current_user.id,
            Workout.date >= date,
            Workout.date < end_date
        ).all()
        calories_burned = sum(w.calories for w in day_workouts)
        
        # Get calories consumed on this day
        day_meals = Meal.query.filter(
            Meal.user_id == current_user.id,
            Meal.date >= date,
            Meal.date < end_date
        ).all()
        calories_consumed = sum(m.calories for m in day_meals)
        
        daily_calories_data.append({
            'date': date.strftime('%Y-%m-%d'),
            'day': date.strftime('%a'),
            'calories_burned': calories_burned,
            'calories_consumed': calories_consumed,
            'net_calories': calories_consumed - calories_burned
        })
    
    # Calculate total calories consumed this week
    weekly_meals = Meal.query.filter(
        Meal.user_id == current_user.id,
        Meal.date >= start_of_week
    ).all()
    calories_consumed_week = sum(m.calories for m in weekly_meals)
    
    # Calculate total calories consumed this month
    monthly_meals = Meal.query.filter(
        Meal.user_id == current_user.id,
        Meal.date >= start_of_month
    ).all()
    calories_consumed_month = sum(m.calories for m in monthly_meals)
    
    return render_template('dashboard/index.html',
                         total_workouts=total_workouts,
                         calories_burned_week=calories_burned_week,
                         calories_burned_month=calories_burned_month,
                         calories_consumed_week=calories_consumed_week,
                         calories_consumed_month=calories_consumed_month,
                         recent_workouts=recent_workouts,
                         recent_meals=recent_meals,
                         active_goals=active_goals,
                         daily_calories_data=daily_calories_data) 