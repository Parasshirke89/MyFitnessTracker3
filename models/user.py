from flask_sqlalchemy import SQLAlchemy
from flask_login import UserMixin
from werkzeug.security import generate_password_hash, check_password_hash
from datetime import datetime

# Initialize SQLAlchemy instance (will be configured in app.py)
db = SQLAlchemy()

class User(UserMixin, db.Model):
    """User model for authentication and user management"""
    
    # Database table name
    __tablename__ = 'users'
    
    # Primary key - unique identifier for each user
    id = db.Column(db.Integer, primary_key=True)
    
    # User credentials and information
    username = db.Column(db.String(80), unique=True, nullable=False)
    email = db.Column(db.String(120), unique=True, nullable=False)
    password_hash = db.Column(db.String(255), nullable=False)
    
    # Profile information
    first_name = db.Column(db.String(50), nullable=True)
    last_name = db.Column(db.String(50), nullable=True)
    age = db.Column(db.Integer, nullable=True)
    weight = db.Column(db.Float, nullable=True)  # in kg
    height = db.Column(db.Float, nullable=True)  # in cm
    gender = db.Column(db.String(20), nullable=True)
    activity_level = db.Column(db.String(50), nullable=True)
    
    # Timestamps for user creation and updates
    created_at = db.Column(db.DateTime, default=datetime.utcnow)
    updated_at = db.Column(db.DateTime, default=datetime.utcnow, onupdate=datetime.utcnow)
    
    # Relationship to other models (one-to-many)
    workouts = db.relationship('Workout', backref='user', lazy=True, cascade='all, delete-orphan')
    meals = db.relationship('Meal', backref='user', lazy=True, cascade='all, delete-orphan')
    goals = db.relationship('Goal', backref='user', lazy=True, cascade='all, delete-orphan')
    
    def __repr__(self):
        """String representation of the User object"""
        return f'<User {self.username}>'
    
    def set_password(self, password):
        """Hash and set the user's password"""
        # Generate a secure hash of the password
        self.password_hash = generate_password_hash(password)
    
    def check_password(self, password):
        """Check if the provided password matches the stored hash"""
        return check_password_hash(self.password_hash, password)
    
    def get_full_name(self):
        """Get the user's full name"""
        if self.first_name and self.last_name:
            return f"{self.first_name} {self.last_name}"
        elif self.first_name:
            return self.first_name
        else:
            return self.username
    
    def get_bmi(self):
        """Calculate BMI if height and weight are available"""
        if self.height and self.weight and self.height > 0:
            height_m = self.height / 100  # Convert cm to meters
            return round(self.weight / (height_m ** 2), 1)
        return None
    
    def get_bmi_category(self):
        """Get BMI category"""
        bmi = self.get_bmi()
        if bmi is None:
            return "Not available"
        elif bmi < 18.5:
            return "Underweight"
        elif bmi < 25:
            return "Normal weight"
        elif bmi < 30:
            return "Overweight"
        else:
            return "Obese"
    
    def get_total_workouts(self):
        """Get the total number of workouts for this user"""
        return len(self.workouts)
    
    def get_calories_burned_this_week(self):
        """Calculate total calories burned in the current week"""
        from datetime import datetime, timedelta
        
        # Get the start of the current week (Monday)
        today = datetime.now()
        start_of_week = today - timedelta(days=today.weekday())
        start_of_week = start_of_week.replace(hour=0, minute=0, second=0, microsecond=0)
        
        # Filter workouts from this week and sum calories
        weekly_workouts = [w for w in self.workouts if w.date >= start_of_week]
        return sum(w.calories for w in weekly_workouts)
    
    def get_calories_burned_this_month(self):
        """Calculate total calories burned in the current month"""
        from datetime import datetime
        
        # Get the start of the current month
        today = datetime.now()
        start_of_month = today.replace(day=1, hour=0, minute=0, second=0, microsecond=0)
        
        # Filter workouts from this month and sum calories
        monthly_workouts = [w for w in self.workouts if w.date >= start_of_month]
        return sum(w.calories for w in monthly_workouts) 