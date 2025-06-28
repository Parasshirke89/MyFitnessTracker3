import os
from dotenv import load_dotenv

# Load environment variables from .env file
load_dotenv()

class Config:
    """Configuration class for the Flask application"""
    # Secret key for session management and CSRF protection
    SECRET_KEY = os.environ.get('SECRET_KEY') or 'your-super-secret-key-change-this-in-production'
    
    # Database configuration
    SQLALCHEMY_DATABASE_URI = os.environ.get('DATABASE_URL') or 'sqlite:///fitness_tracker.db'
    SQLALCHEMY_TRACK_MODIFICATIONS = False
    
    # Flask-WTF configuration
    WTF_CSRF_ENABLED = True 