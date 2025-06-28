from flask import Flask, render_template, redirect, url_for
from flask_login import LoginManager, current_user
from config import Config
from models.user import db, User
from blueprints.auth import auth
from blueprints.dashboard import dashboard
from blueprints.workout import workout
from blueprints.meal import meal
from blueprints.goal import goal

def create_app(config_class=Config):
    """Application factory function to create and configure the Flask app"""
    
    # Create Flask application instance
    app = Flask(__name__)
    
    # Load configuration
    app.config.from_object(config_class)
    
    # Initialize extensions
    db.init_app(app)
    
    # Initialize Flask-Login
    login_manager = LoginManager()
    login_manager.init_app(app)
    login_manager.login_view = 'auth.login'
    login_manager.login_message = 'Please log in to access this page.'
    login_manager.login_message_category = 'info'
    
    @login_manager.user_loader
    def load_user(user_id):
        """Load user by ID for Flask-Login"""
        return User.query.get(int(user_id))
    
    # Register blueprints
    app.register_blueprint(auth, url_prefix='/auth')
    app.register_blueprint(dashboard)
    app.register_blueprint(workout)
    app.register_blueprint(meal)
    app.register_blueprint(goal)
    
    # Root route
    @app.route('/')
    def index():
        """Landing page - redirect to dashboard if logged in, otherwise show welcome page"""
        if current_user.is_authenticated:
            return redirect(url_for('dashboard.index'))
        return render_template('index.html')
    
    # Error handlers
    @app.errorhandler(404)
    def not_found_error(error):
        """Handle 404 errors"""
        return render_template('errors/404.html'), 404
    
    @app.errorhandler(500)
    def internal_error(error):
        """Handle 500 errors"""
        db.session.rollback()
        return render_template('errors/500.html'), 500
    
    # Context processor to make current_user available in all templates
    @app.context_processor
    def inject_user():
        """Inject current_user into template context"""
        return dict(current_user=current_user)
    
    return app

# Create the application instance
app = create_app()

if __name__ == '__main__':
    # Create database tables
    with app.app_context():
        db.create_all()
        print("Database tables created successfully!")
    
    # Run the application in development mode
    app.run(debug=True, host='0.0.0.0', port=5000) 