from flask_sqlalchemy import SQLAlchemy
from flask_login import UserMixin
from werkzeug.security import generate_password_hash, check_password_hash
from datetime import date, timedelta, datetime

db = SQLAlchemy()

class User(db.Model, UserMixin):
    id = db.Column(db.Integer, primary_key=True)
    email = db.Column(db.String(120), unique=True, nullable=False)
    password_hash = db.Column(db.String(256))
    role = db.Column(db.String(20), default='member')
    full_name = db.Column(db.String(100))

    member_details = db.relationship('Member', backref='user', uselist=False, lazy=True)

    def set_password(self, password):
        self.password_hash = generate_password_hash(password)

    def check_password(self, password):
        return check_password_hash(self.password_hash, password)
    
class Member(db.Model):
    id = db.Column(db.Integer, primary_key=True)
    
    user_id = db.Column(db.Integer, db.ForeignKey('user.id'), unique=True, nullable=False)

    membership_type = db.Column(db.String(50), default='Monthly')
    membership_end_date = db.Column(db.Date, nullable=False, default=(date.today() + timedelta(days=30)))

    def days_left(self):
        data = self.membership_end_date - date.today()
        return max(0, data.days)
    
class GymClass(db.Model):
    id = db.Column(db.Integer, primary_key=True)
    name = db.Column(db.String(100))
    time = db.Column(db.DateTime)

class Booking(db.Model):
    id = db.Column(db.Integer, primary_key=True)
    member_id = db.Column(db.Integer, db.ForeignKey('member.id'), nullable=False)
    class_id = db.Column(db.Integer, db.ForeignKey('gym_class.id'), nullable=False)

class Payment(db.Model):
    id = db.Column(db.Integer, primary_key=True)
    user_id = db.Column(db.Integer, db.ForeignKey('user.id'), nullable=False)

    card_number = db.Column(db.String(20))
    cvv_number = db.Column(db.String(4))
    end_date = db.Column(db.Date)
    
    full_name = db.Column(db.String(100))
    
    membership_type = db.Column(db.String(50))