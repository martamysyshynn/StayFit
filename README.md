# StayFit

A web application for gym membership and workout scheduling, built with Python (Flask) and SQLAlchemy. It supports user registration, authentication, secure password hashing, membership and booking management, and real-time schedule tracking.

## Features

- **User Authentication**: Secure registration and login system
- **Membership Management**: Multiple subscription plans (Monthly, Quarterly, Semi-Annual, Annual)
- **Payment Processing**: Secure checkout with card validation
- **User Dashboard**: Membership status tracking with visual progress indicators
- **Responsive Design**: Bootstrap-based UI with dark theme

## Tech Stack

- **Backend**: Flask, Flask-Login, Flask-SQLAlchemy, Flask-WTF
- **Frontend**: Bootstrap 5, HTML/CSS, Jinja2 templates
- **Database**: SQLAlchemy ORM with SQLite
- **Security**: Password hashing, form validation, user sessions
  
## Installation

1. **Clone the repository**
   ```bash
   git clone <repository-url>
   cd repository_name

2. **Create virtual environment**
   ```bash
   python -m venv venv
   source venv/bin/activate  # On Windows: venv\Scripts\activate
   ```
3. **Install dependencies**
   ```bash
   pip install -r requirements.txt
   ```


4. **Edit config.py.example**
   ``` ini
   SECRET_KEY = os.environ.get('SECRET_KEY') or 'SET_YOUR_SECRET_KEY'
   ```

5. **Initialize database**
   Open a Python shell inside your virtual environment:
   ```bash
    from app import create_app
    from models import db, User, Member, GymClass, Booking, Payment


    app = create_app()
    app.app_context().push() 


    db.create_all() 

    exit()
    ```

6. **Run the app**
   ```bash
   python app.py
   ```

## Author
Marta Mysyshyn

GitHub: martamysyshynn
