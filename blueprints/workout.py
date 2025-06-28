from flask import Blueprint, render_template, redirect, url_for, flash, request, jsonify
from flask_login import login_required, current_user
from models.workout import Workout, db
from forms import WorkoutForm, FilterForm
from datetime import datetime

# Create workout blueprint
workout = Blueprint('workout', __name__)

@workout.route('/workouts')
@login_required
def index():
    """Display all workouts for the current user"""
    # Get filter parameters
    start_date = request.args.get('start_date')
    end_date = request.args.get('end_date')
    exercise_type = request.args.get('exercise_type')
    
    # Build query
    query = Workout.query.filter(Workout.user_id == current_user.id)
    
    # Apply filters
    if start_date:
        try:
            start_date_obj = datetime.strptime(start_date, '%Y-%m-%d')
            query = query.filter(Workout.date >= start_date_obj)
        except ValueError:
            pass
    
    if end_date:
        try:
            end_date_obj = datetime.strptime(end_date, '%Y-%m-%d')
            query = query.filter(Workout.date <= end_date_obj)
        except ValueError:
            pass
    
    if exercise_type and exercise_type != '':
        query = query.filter(Workout.exercise_type == exercise_type)
    
    # Order by date (newest first)
    workouts = query.order_by(Workout.date.desc()).all()
    
    # Create filter form
    form = FilterForm()
    form.exercise_type.choices = [('', 'All Types')] + [(t, t) for t in Workout.get_exercise_types()]
    
    return render_template('workout/index.html', workouts=workouts, form=form)

@workout.route('/workouts/new', methods=['GET', 'POST'])
@login_required
def new():
    """Create a new workout"""
    form = WorkoutForm()
    
    # Set exercise type choices
    form.exercise_type.choices = [(t, t) for t in Workout.get_exercise_types()]
    
    if form.validate_on_submit():
        # Create new workout
        workout = Workout(
            user_id=current_user.id,
            exercise_type=form.exercise_type.data,
            duration=form.duration.data,
            intensity=form.intensity.data,
            calories=form.calories.data,
            notes=form.notes.data,
            date=form.date.data
        )
        
        # Save to database
        db.session.add(workout)
        db.session.commit()
        
        flash('Workout added successfully!', 'success')
        return redirect(url_for('workout.index'))
    
    return render_template('workout/new.html', form=form)

@workout.route('/workouts/<int:id>')
@login_required
def show(id):
    """Display a specific workout"""
    workout = Workout.query.filter_by(id=id, user_id=current_user.id).first_or_404()
    return render_template('workout/show.html', workout=workout)

@workout.route('/workouts/<int:id>/edit', methods=['GET', 'POST'])
@login_required
def edit(id):
    """Edit an existing workout"""
    workout = Workout.query.filter_by(id=id, user_id=current_user.id).first_or_404()
    form = WorkoutForm(obj=workout)
    
    # Set exercise type choices
    form.exercise_type.choices = [(t, t) for t in Workout.get_exercise_types()]
    
    if form.validate_on_submit():
        # Update workout data
        workout.exercise_type = form.exercise_type.data
        workout.duration = form.duration.data
        workout.intensity = form.intensity.data
        workout.calories = form.calories.data
        workout.notes = form.notes.data
        workout.date = form.date.data
        
        # Save changes
        db.session.commit()
        
        flash('Workout updated successfully!', 'success')
        return redirect(url_for('workout.show', id=workout.id))
    
    return render_template('workout/edit.html', form=form, workout=workout)

@workout.route('/workouts/<int:id>/delete', methods=['POST'])
@login_required
def delete(id):
    """Delete a workout"""
    workout = Workout.query.filter_by(id=id, user_id=current_user.id).first_or_404()
    
    # Delete from database
    db.session.delete(workout)
    db.session.commit()
    
    flash('Workout deleted successfully!', 'success')
    return redirect(url_for('workout.index'))

@workout.route('/workouts/export')
@login_required
def export():
    """Export workouts as CSV"""
    import csv
    from io import StringIO
    from flask import make_response
    
    # Get all workouts for current user
    workouts = Workout.query.filter_by(user_id=current_user.id).order_by(Workout.date.desc()).all()
    
    # Create CSV data
    si = StringIO()
    cw = csv.writer(si)
    
    # Write header
    cw.writerow(['Date', 'Exercise Type', 'Duration (min)', 'Intensity', 'Calories', 'Notes'])
    
    # Write workout data
    for w in workouts:
        cw.writerow([
            w.date.strftime('%Y-%m-%d'),
            w.exercise_type,
            w.duration,
            w.intensity,
            w.calories,
            w.notes or ''
        ])
    
    # Create response
    output = make_response(si.getvalue())
    output.headers["Content-Disposition"] = f"attachment; filename=workouts_{datetime.now().strftime('%Y%m%d')}.csv"
    output.headers["Content-type"] = "text/csv"
    
    return output 