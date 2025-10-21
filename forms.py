from flask_wtf import FlaskForm
from wtforms import StringField, PasswordField, SubmitField, SelectField
from wtforms.validators import DataRequired, Email, EqualTo, ValidationError, Length, Regexp
from models import User
from datetime import date

class LoginForm(FlaskForm):
    email = StringField('Email', validators=[DataRequired(), Email()])
    password = PasswordField('Password', validators=[DataRequired()])
    submit = SubmitField('Log In')

class RegistrationForm(FlaskForm):
    email = StringField('Email', validators=[DataRequired(), Email()])
    full_name = StringField('Full name', validators=[DataRequired(), Length(min=2, max=100)])
    password = PasswordField('Password', validators=[DataRequired()])
    password2 = PasswordField('Repeat password', validators=[DataRequired(), EqualTo('password', message='Passwords must match')])
    submit = SubmitField('Register')

    def validate_email(self, email):
        user = User.query.filter_by(email=email.data).first()
        if user is not None:
            raise ValidationError('This email address is already registered.')

class PaymentForm(FlaskForm):
    card_number = StringField('Card Number', validators=[DataRequired(), Length(min=2, max=20), Regexp(r'^\d+$')])
    cvv_number = StringField('CVV', validators=[DataRequired(), Length(min=3), Regexp(r'^\d+$')])

    current_year = date.today().year
    expiry_month = SelectField('Month', choices=[(str(i).zfill(2), str(i).zfill(2)) for i in range(1, 13)], validators=[DataRequired()])
    expiry_year = SelectField('Year', choices=[(str(i), str(i)) for i in range(current_year, current_year + 10)], validators=[DataRequired()])
    
    full_name = StringField('Name on Card', validators=[DataRequired(), Length(min=2, max=100)])
    submit = SubmitField('Pay')
