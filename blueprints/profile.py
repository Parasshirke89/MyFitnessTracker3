from flask import Blueprint, render_template, request, flash, redirect, url_for
from flask_login import login_required, current_user
from werkzeug.security import generate_password_hash, check_password_hash
from models.user import db, User
from forms import ProfileUpdateForm, PasswordChangeForm

profile = Blueprint('profile', __name__)

@profile.route('/profile')
@login_required
def view_profile():
    """Display user profile page"""
    return render_template('profile/index.html', user=current_user)

@profile.route('/profile/edit', methods=['GET', 'POST'])
@login_required
def edit_profile():
    """Edit user profile information"""
    form = ProfileUpdateForm()
    
    if form.validate_on_submit():
        current_user.username = form.username.data
        current_user.email = form.email.data
        current_user.first_name = form.first_name.data
        current_user.last_name = form.last_name.data
        current_user.age = form.age.data
        current_user.weight = form.weight.data
        current_user.height = form.height.data
        current_user.gender = form.gender.data
        current_user.activity_level = form.activity_level.data
        
        db.session.commit()
        flash('Profile updated successfully!', 'success')
        return redirect(url_for('profile.view_profile'))
    
    elif request.method == 'GET':
        form.username.data = current_user.username
        form.email.data = current_user.email
        form.first_name.data = current_user.first_name
        form.last_name.data = current_user.last_name
        form.age.data = current_user.age
        form.weight.data = current_user.weight
        form.height.data = current_user.height
        form.gender.data = current_user.gender
        form.activity_level.data = current_user.activity_level
    
    return render_template('profile/edit.html', form=form)

@profile.route('/profile/change-password', methods=['GET', 'POST'])
@login_required
def change_password():
    """Change user password"""
    form = PasswordChangeForm()
    
    if form.validate_on_submit():
        if check_password_hash(current_user.password_hash, form.current_password.data):
            current_user.password_hash = generate_password_hash(form.new_password.data)
            db.session.commit()
            flash('Password changed successfully!', 'success')
            return redirect(url_for('profile.view_profile'))
        else:
            flash('Current password is incorrect.', 'error')
    
    return render_template('profile/change_password.html', form=form)

@profile.route('/profile/statistics')
@login_required
def statistics():
    """Display detailed user statistics"""
    from models.workout import Workout
    from models.meal import Meal
    from models.goal import Goal
    from datetime import datetime, timedelta
    
    # Get date range for statistics
    end_date = datetime.now()
    start_date = end_date - timedelta(days=30)
    
    # Workout statistics
    workouts = Workout.query.filter(
        Workout.user_id == current_user.id,
        Workout.date >= start_date,
        Workout.date <= end_date
    ).all()
    
    total_workouts = len(workouts)
    total_calories_burned = sum(w.calories_burned for w in workouts)
    total_duration = sum(w.duration for w in workouts)
    
    # Meal statistics
    meals = Meal.query.filter(
        Meal.user_id == current_user.id,
        Meal.date >= start_date,
        Meal.date <= end_date
    ).all()
    
    total_meals = len(meals)
    total_calories_consumed = sum(m.calories for m in meals)
    total_protein = sum(m.protein for m in meals)
    total_carbs = sum(m.carbohydrates for m in meals)
    total_fats = sum(m.fats for m in meals)
    
    # Goal statistics
    active_goals = Goal.query.filter(
        Goal.user_id == current_user.id,
        Goal.completed == False
    ).all()
    
    completed_goals = Goal.query.filter(
        Goal.user_id == current_user.id,
        Goal.completed == True
    ).all()
    
    stats = {
        'workouts': {
            'total': total_workouts,
            'calories_burned': total_calories_burned,
            'duration': total_duration,
            'avg_calories_per_workout': total_calories_burned / total_workouts if total_workouts > 0 else 0
        },
        'meals': {
            'total': total_meals,
            'calories_consumed': total_calories_consumed,
            'protein': total_protein,
            'carbs': total_carbs,
            'fats': total_fats,
            'avg_calories_per_meal': total_calories_consumed / total_meals if total_meals > 0 else 0
        },
        'goals': {
            'active': len(active_goals),
            'completed': len(completed_goals),
            'completion_rate': len(completed_goals) / (len(active_goals) + len(completed_goals)) * 100 if (len(active_goals) + len(completed_goals)) > 0 else 0
        }
    }
    
    return render_template('profile/statistics.html', stats=stats) 