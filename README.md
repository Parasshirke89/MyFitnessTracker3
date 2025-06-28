# Fitness Tracker - Web Application

A professional-grade, web-based fitness and nutrition tracker built with Python Flask, SQLite, Bootstrap 5, and Chart.js.

## 🚀 Features

### Core Functionality
- **User Authentication**: Secure registration and login system with password hashing
- **Dashboard**: Comprehensive overview with statistics and charts
- **Workout Tracking**: Log exercises with type, duration, intensity, and calories burned
- **Nutrition Tracking**: Record meals with detailed macronutrient information
- **Goal Setting**: Create and track progress toward fitness goals
- **Data Export**: Export workouts and meals as CSV files

### Dashboard Features
- Welcome message with user's name
- Statistics cards showing total workouts, calories burned (week/month)
- Interactive charts using Chart.js
- Recent activity feeds
- Quick action buttons

### Workout Module
- Add, edit, and delete workouts
- Filter by date range and exercise type
- Track exercise type, duration, intensity, calories, and notes
- Export workout data to CSV

### Nutrition Module
- Add, edit, and delete meals
- Track calories, protein, carbs, and fats
- Daily meal log view
- Weekly nutritional summary
- Export meal data to CSV

### Goals & Progress
- Set fitness goals (calories, workouts, weight, distance, duration)
- Track progress with visual progress bars
- Support for daily, weekly, and monthly timeframes
- Goal completion notifications

## 🛠️ Technology Stack

- **Backend**: Python Flask
- **Database**: SQLite with SQLAlchemy ORM
- **Frontend**: HTML5, CSS3, Bootstrap 5
- **Charts**: Chart.js
- **Authentication**: Flask-Login
- **Forms**: Flask-WTF with validation
- **Icons**: Bootstrap Icons

## 📋 Prerequisites

- Python 3.7 or higher
- pip (Python package installer)

## 🚀 Installation & Setup

### 1. Clone or Download the Project
```bash
# If using git
git clone <repository-url>
cd MyFitnessTracker3

# Or simply download and extract the project files
```

### 2. Create a Virtual Environment (Recommended)
```bash
# On Windows
python -m venv venv
venv\Scripts\activate

# On macOS/Linux
python3 -m venv venv
source venv/bin/activate
```

### 3. Install Dependencies
```bash
pip install -r requirements.txt
```

### 4. Run the Application
```bash
python app.py
```

The application will start on `http://localhost:5000`

### 5. Access the Application
- Open your web browser
- Navigate to `http://localhost:5000`
- Register a new account or log in if you already have one

## 📁 Project Structure

```
MyFitnessTracker3/
├── app.py                 # Main Flask application
├── config.py              # Configuration settings
├── forms.py               # Flask-WTF forms
├── requirements.txt       # Python dependencies
├── README.md             # This file
├── models/               # Database models
│   ├── __init__.py
│   ├── user.py          # User model
│   ├── workout.py       # Workout model
│   ├── meal.py          # Meal model
│   └── goal.py          # Goal model
├── blueprints/           # Flask blueprints
│   ├── __init__.py
│   ├── auth.py          # Authentication routes
│   ├── dashboard.py     # Dashboard routes
│   ├── workout.py       # Workout routes
│   ├── meal.py          # Meal routes
│   └── goal.py          # Goal routes
└── templates/            # HTML templates
    ├── base.html         # Base template
    ├── auth/             # Authentication templates
    ├── dashboard/        # Dashboard templates
    ├── workout/          # Workout templates
    ├── meal/             # Meal templates
    └── goal/             # Goal templates
```

## 🎯 Usage Guide

### Getting Started
1. **Register an Account**: Click "Register" and create your account
2. **Login**: Use your credentials to access the dashboard
3. **Explore the Dashboard**: View your statistics and recent activity

### Adding Workouts
1. Navigate to "Workouts" in the navigation
2. Click "Add Workout"
3. Fill in the workout details:
   - Exercise type (running, weight training, etc.)
   - Duration in minutes
   - Intensity level (Low, Medium, High)
   - Calories burned
   - Optional notes
   - Date
4. Click "Save Workout"

### Adding Meals
1. Navigate to "Meals" in the navigation
2. Click "Add Meal"
3. Fill in the meal details:
   - Food name
   - Calories
   - Protein (grams)
   - Carbohydrates (grams)
   - Fats (grams)
   - Meal type (Breakfast, Lunch, Dinner, Snack)
   - Date
4. Click "Save Meal"

### Setting Goals
1. Navigate to "Goals" in the navigation
2. Click "Create Goal"
3. Fill in the goal details:
   - Goal title
   - Goal type (calories, workouts, weight, etc.)
   - Target value
   - Timeframe (daily, weekly, monthly)
4. Click "Save Goal"

### Viewing Progress
- **Dashboard**: Overview of all statistics and recent activity
- **Daily Log**: View meals for a specific day
- **Weekly Summary**: Nutritional breakdown for the current week
- **Charts**: Visual representation of calories burned vs consumed

## 🔧 Configuration

### Environment Variables
Create a `.env` file in the project root (optional):
```
SECRET_KEY=your-super-secret-key-change-this-in-production
FLASK_APP=app.py
FLASK_ENV=development
DATABASE_URL=sqlite:///fitness_tracker.db
```

### Database
The application uses SQLite by default. The database file (`fitness_tracker.db`) will be created automatically when you first run the application.

## 🎨 Customization

### Styling
- Modify `templates/base.html` to change the overall look
- Update CSS variables in the `<style>` section for color schemes
- Add custom CSS files in the `static/` directory

### Adding New Exercise Types
Edit `models/workout.py` and add new exercise types to the `get_exercise_types()` method.

### Adding New Goal Types
Edit `models/goal.py` and add new goal types to the `get_goal_types()` method.

## 🔒 Security Features

- Password hashing using Werkzeug
- CSRF protection with Flask-WTF
- Session-based authentication
- Input validation and sanitization
- SQL injection protection through SQLAlchemy

## 📊 Data Export

### Exporting Workouts
1. Navigate to the Workouts page
2. Click "Export to CSV"
3. Download the CSV file with all your workout data

### Exporting Meals
1. Navigate to the Meals page
2. Click "Export to CSV"
3. Download the CSV file with all your meal data

## 🐛 Troubleshooting

### Common Issues

**Import Errors**
- Make sure all dependencies are installed: `pip install -r requirements.txt`
- Verify you're using the correct Python version (3.7+)

**Database Errors**
- Delete the `fitness_tracker.db` file and restart the application
- The database will be recreated automatically

**Port Already in Use**
- Change the port in `app.py`: `app.run(debug=True, host='0.0.0.0', port=5001)`

**Template Errors**
- Ensure all template files are in the correct directories
- Check for proper Jinja2 syntax in templates

## 🤝 Contributing

1. Fork the repository
2. Create a feature branch
3. Make your changes
4. Test thoroughly
5. Submit a pull request

## 📝 License

This project is open source and available under the [MIT License](LICENSE).

## 🙏 Acknowledgments

- Flask community for the excellent web framework
- Bootstrap team for the responsive CSS framework
- Chart.js for the interactive charts
- All contributors and users of this application

## 📞 Support

If you encounter any issues or have questions:
1. Check the troubleshooting section above
2. Review the code comments for guidance
3. Create an issue in the repository

---

**Happy Fitness Tracking! 💪** 