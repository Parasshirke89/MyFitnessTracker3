from flask_sqlalchemy import SQLAlchemy
from datetime import datetime

# Import the shared db instance
from .user import db

class Workout(db.Model):
    """Workout model for tracking exercise sessions"""
    
    # Database table name
    __tablename__ = 'workouts'
    
    # Primary key - unique identifier for each workout
    id = db.Column(db.Integer, primary_key=True)
    
    # Foreign key to link workout to user
    user_id = db.Column(db.Integer, db.ForeignKey('users.id'), nullable=False)
    
    # Workout details
    exercise_type = db.Column(db.String(100), nullable=False)  # e.g., "Running", "Weight Training"
    duration = db.Column(db.Integer, nullable=False)  # Duration in minutes
    intensity = db.Column(db.String(20), nullable=False)  # "Low", "Medium", "High"
    calories = db.Column(db.Integer, nullable=False)  # Calories burned
    notes = db.Column(db.Text)  # Optional notes about the workout
    date = db.Column(db.DateTime, nullable=False, default=datetime.utcnow)
    
    # Timestamps for creation and updates
    created_at = db.Column(db.DateTime, default=datetime.utcnow)
    updated_at = db.Column(db.DateTime, default=datetime.utcnow, onupdate=datetime.utcnow)
    
    def __repr__(self):
        """String representation of the Workout object"""
        return f'<Workout {self.exercise_type} - {self.date.strftime("%Y-%m-%d")}>'
    
    def to_dict(self):
        """Convert workout to dictionary for JSON serialization"""
        return {
            'id': self.id,
            'exercise_type': self.exercise_type,
            'duration': self.duration,
            'intensity': self.intensity,
            'calories': self.calories,
            'notes': self.notes,
            'date': self.date.strftime('%Y-%m-%d %H:%M:%S'),
            'created_at': self.created_at.strftime('%Y-%m-%d %H:%M:%S')
        }
    
    @staticmethod
    def get_intensity_options():
        """Get available intensity levels"""
        return ['Low', 'Medium', 'High']
    
    @staticmethod
    def get_exercise_types():
        """Get common exercise types"""
        return [
            'Running', 'Walking', 'Cycling', 'Swimming', 'Weight Training',
            'Yoga', 'Pilates', 'HIIT', 'CrossFit', 'Basketball', 'Soccer',
            'Tennis', 'Golf', 'Hiking', 'Dancing', 'Boxing', 'Martial Arts',
            'Rowing', 'Elliptical', 'Stair Climber', 'Other'
        ] 