from flask import Blueprint, render_template, redirect, url_for, flash, request, jsonify
from flask_login import login_required, current_user
from models.meal import Meal, db
from forms import MealForm, FilterForm
from datetime import datetime, timedelta

# Create meal blueprint
meal = Blueprint('meal', __name__)

@meal.route('/meals')
@login_required
def index():
    """Display all meals for the current user"""
    # Get filter parameters
    start_date = request.args.get('start_date')
    end_date = request.args.get('end_date')
    meal_type = request.args.get('meal_type')
    
    # Build query
    query = Meal.query.filter(Meal.user_id == current_user.id)
    
    # Apply filters
    if start_date:
        try:
            start_date_obj = datetime.strptime(start_date, '%Y-%m-%d')
            query = query.filter(Meal.date >= start_date_obj)
        except ValueError:
            pass
    
    if end_date:
        try:
            end_date_obj = datetime.strptime(end_date, '%Y-%m-%d')
            query = query.filter(Meal.date <= end_date_obj)
        except ValueError:
            pass
    
    if meal_type and meal_type != '':
        query = query.filter(Meal.meal_type == meal_type)
    
    # Order by date (newest first)
    meals = query.order_by(Meal.date.desc()).all()
    
    # Create filter form
    form = FilterForm()
    form.meal_type.choices = [('', 'All Meals')] + [(t, t) for t in Meal.get_meal_types()]
    
    return render_template('meal/index.html', meals=meals, form=form)

@meal.route('/meals/new', methods=['GET', 'POST'])
@login_required
def new():
    """Create a new meal"""
    form = MealForm()
    
    if form.validate_on_submit():
        # Create new meal
        meal = Meal(
            user_id=current_user.id,
            food_name=form.food_name.data,
            calories=form.calories.data,
            protein=form.protein.data,
            carbs=form.carbs.data,
            fats=form.fats.data,
            meal_type=form.meal_type.data,
            date=form.date.data
        )
        
        # Save to database
        db.session.add(meal)
        db.session.commit()
        
        flash('Meal added successfully!', 'success')
        return redirect(url_for('meal.index'))
    
    return render_template('meal/new.html', form=form)

@meal.route('/meals/<int:id>')
@login_required
def show(id):
    """Display a specific meal"""
    meal = Meal.query.filter_by(id=id, user_id=current_user.id).first_or_404()
    return render_template('meal/show.html', meal=meal)

@meal.route('/meals/<int:id>/edit', methods=['GET', 'POST'])
@login_required
def edit(id):
    """Edit an existing meal"""
    meal = Meal.query.filter_by(id=id, user_id=current_user.id).first_or_404()
    form = MealForm(obj=meal)
    
    if form.validate_on_submit():
        # Update meal data
        meal.food_name = form.food_name.data
        meal.calories = form.calories.data
        meal.protein = form.protein.data
        meal.carbs = form.carbs.data
        meal.fats = form.fats.data
        meal.meal_type = form.meal_type.data
        meal.date = form.date.data
        
        # Save changes
        db.session.commit()
        
        flash('Meal updated successfully!', 'success')
        return redirect(url_for('meal.show', id=meal.id))
    
    return render_template('meal/edit.html', form=form, meal=meal)

@meal.route('/meals/<int:id>/delete', methods=['POST'])
@login_required
def delete(id):
    """Delete a meal"""
    meal = Meal.query.filter_by(id=id, user_id=current_user.id).first_or_404()
    
    # Delete from database
    db.session.delete(meal)
    db.session.commit()
    
    flash('Meal deleted successfully!', 'success')
    return redirect(url_for('meal.index'))

@meal.route('/meals/daily')
@login_required
def daily():
    """Display daily meal log view"""
    # Get date parameter or use today
    date_str = request.args.get('date')
    if date_str:
        try:
            selected_date = datetime.strptime(date_str, '%Y-%m-%d')
        except ValueError:
            selected_date = datetime.now()
    else:
        selected_date = datetime.now()
    
    # Get start and end of selected date
    start_of_day = selected_date.replace(hour=0, minute=0, second=0, microsecond=0)
    end_of_day = start_of_day + timedelta(days=1)
    
    # Get meals for the selected date
    meals = Meal.query.filter(
        Meal.user_id == current_user.id,
        Meal.date >= start_of_day,
        Meal.date < end_of_day
    ).order_by(Meal.date).all()
    
    # Calculate daily totals
    daily_totals = {
        'calories': sum(m.calories for m in meals),
        'protein': sum(m.protein for m in meals),
        'carbs': sum(m.carbs for m in meals),
        'fats': sum(m.fats for m in meals)
    }
    
    # Group meals by meal type
    meals_by_type = {}
    for meal_type in Meal.get_meal_types():
        meals_by_type[meal_type] = [m for m in meals if m.meal_type == meal_type]
    
    return render_template('meal/daily.html', 
                         meals=meals, 
                         meals_by_type=meals_by_type,
                         daily_totals=daily_totals,
                         selected_date=selected_date)

@meal.route('/meals/weekly')
@login_required
def weekly():
    """Display weekly nutritional summary"""
    # Get current week
    today = datetime.now()
    start_of_week = today - timedelta(days=today.weekday())
    start_of_week = start_of_week.replace(hour=0, minute=0, second=0, microsecond=0)
    end_of_week = start_of_week + timedelta(days=7)
    
    # Get meals for the current week
    meals = Meal.query.filter(
        Meal.user_id == current_user.id,
        Meal.date >= start_of_week,
        Meal.date < end_of_week
    ).order_by(Meal.date).all()
    
    # Calculate weekly totals
    weekly_totals = {
        'calories': sum(m.calories for m in meals),
        'protein': sum(m.protein for m in meals),
        'carbs': sum(m.carbs for m in meals),
        'fats': sum(m.fats for m in meals)
    }
    
    # Calculate daily breakdown
    daily_breakdown = []
    for i in range(7):
        date = start_of_week + timedelta(days=i)
        end_date = date + timedelta(days=1)
        
        day_meals = [m for m in meals if m.date >= date and m.date < end_date]
        day_totals = {
            'date': date,
            'day_name': date.strftime('%A'),
            'calories': sum(m.calories for m in day_meals),
            'protein': sum(m.protein for m in day_meals),
            'carbs': sum(m.carbs for m in day_meals),
            'fats': sum(m.fats for m in day_meals)
        }
        daily_breakdown.append(day_totals)
    
    return render_template('meal/weekly.html', 
                         meals=meals,
                         weekly_totals=weekly_totals,
                         daily_breakdown=daily_breakdown,
                         start_of_week=start_of_week)

@meal.route('/meals/export')
@login_required
def export():
    """Export meals as CSV"""
    import csv
    from io import StringIO
    from flask import make_response
    
    # Get all meals for current user
    meals = Meal.query.filter_by(user_id=current_user.id).order_by(Meal.date.desc()).all()
    
    # Create CSV data
    si = StringIO()
    cw = csv.writer(si)
    
    # Write header
    cw.writerow(['Date', 'Meal Type', 'Food Name', 'Calories', 'Protein (g)', 'Carbs (g)', 'Fats (g)'])
    
    # Write meal data
    for m in meals:
        cw.writerow([
            m.date.strftime('%Y-%m-%d'),
            m.meal_type,
            m.food_name,
            m.calories,
            m.protein,
            m.carbs,
            m.fats
        ])
    
    # Create response
    output = make_response(si.getvalue())
    output.headers["Content-Disposition"] = f"attachment; filename=meals_{datetime.now().strftime('%Y%m%d')}.csv"
    output.headers["Content-type"] = "text/csv"
    
    return output 