from flask_sqlalchemy import SQLAlchemy
from datetime import datetime

# Import the shared db instance
from .user import db

class Meal(db.Model):
    """Meal model for tracking nutrition and food intake"""
    
    # Database table name
    __tablename__ = 'meals'
    
    # Primary key - unique identifier for each meal
    id = db.Column(db.Integer, primary_key=True)
    
    # Foreign key to link meal to user
    user_id = db.Column(db.Integer, db.ForeignKey('users.id'), nullable=False)
    
    # Meal details
    food_name = db.Column(db.String(200), nullable=False)  # Name of the food/meal
    calories = db.Column(db.Integer, nullable=False)  # Total calories
    protein = db.Column(db.Float, nullable=False)  # Protein in grams
    carbs = db.Column(db.Float, nullable=False)  # Carbohydrates in grams
    fats = db.Column(db.Float, nullable=False)  # Fats in grams
    meal_type = db.Column(db.String(20), nullable=False)  # "Breakfast", "Lunch", "Dinner", "Snack"
    date = db.Column(db.DateTime, nullable=False, default=datetime.utcnow)
    
    # Timestamps for creation and updates
    created_at = db.Column(db.DateTime, default=datetime.utcnow)
    updated_at = db.Column(db.DateTime, default=datetime.utcnow, onupdate=datetime.utcnow)
    
    def __repr__(self):
        """String representation of the Meal object"""
        return f'<Meal {self.food_name} - {self.date.strftime("%Y-%m-%d")}>'
    
    def to_dict(self):
        """Convert meal to dictionary for JSON serialization"""
        return {
            'id': self.id,
            'food_name': self.food_name,
            'calories': self.calories,
            'protein': self.protein,
            'carbs': self.carbs,
            'fats': self.fats,
            'meal_type': self.meal_type,
            'date': self.date.strftime('%Y-%m-%d %H:%M:%S'),
            'created_at': self.created_at.strftime('%Y-%m-%d %H:%M:%S')
        }
    
    @staticmethod
    def get_meal_types():
        """Get available meal types"""
        return ['Breakfast', 'Lunch', 'Dinner', 'Snack']
    
    def get_total_macros(self):
        """Get total macronutrients for this meal"""
        return {
            'calories': self.calories,
            'protein': self.protein,
            'carbs': self.carbs,
            'fats': self.fats
        } 