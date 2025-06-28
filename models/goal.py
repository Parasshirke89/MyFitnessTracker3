from flask_sqlalchemy import SQLAlchemy
from datetime import datetime

# Import the shared db instance
from .user import db

class Goal(db.Model):
    """Goal model for tracking fitness goals and progress"""
    
    # Database table name
    __tablename__ = 'goals'
    
    # Primary key - unique identifier for each goal
    id = db.Column(db.Integer, primary_key=True)
    
    # Foreign key to link goal to user
    user_id = db.Column(db.Integer, db.ForeignKey('users.id'), nullable=False)
    
    # Goal details
    title = db.Column(db.String(200), nullable=False)  # Goal title/description
    goal_type = db.Column(db.String(50), nullable=False)  # "calories", "workouts", "weight", etc.
    target_value = db.Column(db.Float, nullable=False)  # Target value to achieve
    current_value = db.Column(db.Float, default=0.0)  # Current progress value
    unit = db.Column(db.String(20), nullable=False)  # Unit of measurement (kcal, workouts, lbs, etc.)
    timeframe = db.Column(db.String(20), nullable=False)  # "daily", "weekly", "monthly"
    start_date = db.Column(db.DateTime, nullable=False, default=datetime.utcnow)
    end_date = db.Column(db.DateTime)  # Optional end date
    is_active = db.Column(db.Boolean, default=True)  # Whether the goal is still active
    is_completed = db.Column(db.Boolean, default=False)  # Whether the goal has been achieved
    
    # Timestamps for creation and updates
    created_at = db.Column(db.DateTime, default=datetime.utcnow)
    updated_at = db.Column(db.DateTime, default=datetime.utcnow, onupdate=datetime.utcnow)
    
    def __repr__(self):
        """String representation of the Goal object"""
        return f'<Goal {self.title} - {self.current_value}/{self.target_value} {self.unit}>'
    
    def to_dict(self):
        """Convert goal to dictionary for JSON serialization"""
        return {
            'id': self.id,
            'title': self.title,
            'goal_type': self.goal_type,
            'target_value': self.target_value,
            'current_value': self.current_value,
            'unit': self.unit,
            'timeframe': self.timeframe,
            'start_date': self.start_date.strftime('%Y-%m-%d'),
            'end_date': self.end_date.strftime('%Y-%m-%d') if self.end_date else None,
            'is_active': self.is_active,
            'is_completed': self.is_completed,
            'progress_percentage': self.get_progress_percentage()
        }
    
    def get_progress_percentage(self):
        """Calculate progress percentage towards the goal"""
        if self.target_value == 0:
            return 0
        percentage = (self.current_value / self.target_value) * 100
        return min(percentage, 100)  # Cap at 100%
    
    def update_progress(self, new_value):
        """Update the current progress value"""
        self.current_value = new_value
        
        # Check if goal is completed
        if self.current_value >= self.target_value and not self.is_completed:
            self.is_completed = True
            self.is_active = False
    
    @staticmethod
    def get_goal_types():
        """Get available goal types"""
        return ['calories', 'workouts', 'weight', 'distance', 'duration']
    
    @staticmethod
    def get_timeframes():
        """Get available timeframes"""
        return ['daily', 'weekly', 'monthly']
    
    @staticmethod
    def get_units():
        """Get available units for different goal types"""
        return {
            'calories': 'kcal',
            'workouts': 'sessions',
            'weight': 'lbs',
            'distance': 'miles',
            'duration': 'minutes'
        } 