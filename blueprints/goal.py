from flask import Blueprint, render_template, redirect, url_for, flash, request
from flask_login import login_required, current_user
from models.goal import Goal, db
from models.workout import Workout
from models.meal import Meal
from forms import GoalForm
from datetime import datetime, timedelta

# Create goal blueprint
goal = Blueprint('goal', __name__)

@goal.route('/goals')
@login_required
def index():
    """Display all goals for the current user"""
    # Get all goals (active and completed)
    active_goals = Goal.query.filter_by(user_id=current_user.id, is_active=True).all()
    completed_goals = Goal.query.filter_by(user_id=current_user.id, is_active=False).all()
    
    return render_template('goal/index.html', 
                         active_goals=active_goals,
                         completed_goals=completed_goals)

@goal.route('/goals/new', methods=['GET', 'POST'])
@login_required
def new():
    """Create a new goal"""
    form = GoalForm()
    
    if form.validate_on_submit():
        # Set unit based on goal type if not provided
        if not form.unit.data:
            units = Goal.get_units()
            form.unit.data = units.get(form.goal_type.data, '')
        
        # Create new goal
        goal = Goal(
            user_id=current_user.id,
            title=form.title.data,
            goal_type=form.goal_type.data,
            target_value=form.target_value.data,
            unit=form.unit.data,
            timeframe=form.timeframe.data,
            end_date=form.end_date.data
        )
        
        # Save to database
        db.session.add(goal)
        db.session.commit()
        
        flash('Goal created successfully!', 'success')
        return redirect(url_for('goal.index'))
    
    return render_template('goal/new.html', form=form)

@goal.route('/goals/<int:id>')
@login_required
def show(id):
    """Display a specific goal"""
    goal = Goal.query.filter_by(id=id, user_id=current_user.id).first_or_404()
    
    # Calculate current progress based on goal type
    current_progress = calculate_goal_progress(goal)
    
    return render_template('goal/show.html', goal=goal, current_progress=current_progress)

@goal.route('/goals/<int:id>/edit', methods=['GET', 'POST'])
@login_required
def edit(id):
    """Edit an existing goal"""
    goal = Goal.query.filter_by(id=id, user_id=current_user.id).first_or_404()
    form = GoalForm(obj=goal)
    
    if form.validate_on_submit():
        # Update goal data
        goal.title = form.title.data
        goal.goal_type = form.goal_type.data
        goal.target_value = form.target_value.data
        goal.unit = form.unit.data
        goal.timeframe = form.timeframe.data
        goal.end_date = form.end_date.data
        
        # Save changes
        db.session.commit()
        
        flash('Goal updated successfully!', 'success')
        return redirect(url_for('goal.show', id=goal.id))
    
    return render_template('goal/edit.html', form=form, goal=goal)

@goal.route('/goals/<int:id>/delete', methods=['POST'])
@login_required
def delete(id):
    """Delete a goal"""
    goal = Goal.query.filter_by(id=id, user_id=current_user.id).first_or_404()
    
    # Delete from database
    db.session.delete(goal)
    db.session.commit()
    
    flash('Goal deleted successfully!', 'success')
    return redirect(url_for('goal.index'))

@goal.route('/goals/<int:id>/complete', methods=['POST'])
@login_required
def complete(id):
    """Mark a goal as completed"""
    goal = Goal.query.filter_by(id=id, user_id=current_user.id).first_or_404()
    
    # Mark as completed
    goal.is_completed = True
    goal.is_active = False
    db.session.commit()
    
    flash('Goal marked as completed!', 'success')
    return redirect(url_for('goal.show', id=goal.id))

@goal.route('/goals/<int:id>/reactivate', methods=['POST'])
@login_required
def reactivate(id):
    """Reactivate a completed goal"""
    goal = Goal.query.filter_by(id=id, user_id=current_user.id).first_or_404()
    
    # Reactivate goal
    goal.is_completed = False
    goal.is_active = True
    goal.current_value = 0.0  # Reset progress
    db.session.commit()
    
    flash('Goal reactivated!', 'success')
    return redirect(url_for('goal.show', id=goal.id))

def calculate_goal_progress(goal):
    """Calculate current progress for a goal based on its type and timeframe"""
    today = datetime.now()
    
    # Determine the start date based on timeframe
    if goal.timeframe == 'daily':
        start_date = today.replace(hour=0, minute=0, second=0, microsecond=0)
    elif goal.timeframe == 'weekly':
        start_date = today - timedelta(days=today.weekday())
        start_date = start_date.replace(hour=0, minute=0, second=0, microsecond=0)
    elif goal.timeframe == 'monthly':
        start_date = today.replace(day=1, hour=0, minute=0, second=0, microsecond=0)
    else:
        start_date = goal.start_date
    
    # Calculate progress based on goal type
    if goal.goal_type == 'calories':
        # Count calories burned from workouts
        workouts = Workout.query.filter(
            Workout.user_id == current_user.id,
            Workout.date >= start_date
        ).all()
        progress = sum(w.calories for w in workouts)
    
    elif goal.goal_type == 'workouts':
        # Count number of workouts
        workouts = Workout.query.filter(
            Workout.user_id == current_user.id,
            Workout.date >= start_date
        ).all()
        progress = len(workouts)
    
    elif goal.goal_type == 'weight':
        # For weight goals, we'd need a separate weight tracking model
        # For now, return the current value stored in the goal
        progress = goal.current_value
    
    elif goal.goal_type == 'distance':
        # Count distance from workouts (would need distance field in workout model)
        # For now, return current value
        progress = goal.current_value
    
    elif goal.goal_type == 'duration':
        # Count total duration from workouts
        workouts = Workout.query.filter(
            Workout.user_id == current_user.id,
            Workout.date >= start_date
        ).all()
        progress = sum(w.duration for w in workouts)
    
    else:
        progress = goal.current_value
    
    # Update the goal's current value
    goal.current_value = progress
    
    # Check if goal is completed
    if progress >= goal.target_value and not goal.is_completed:
        goal.is_completed = True
        goal.is_active = False
    
    db.session.commit()
    
    return progress 