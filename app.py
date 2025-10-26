from flask import Flask, render_template, redirect, url_for, flash, request
from flask_login import LoginManager, login_user, logout_user, current_user, login_required
from config import Config

from models import db, User, Member, GymClass, Booking, Payment
from forms import LoginForm, RegistrationForm, PaymentForm
from datetime import date, timedelta

login_manager = LoginManager()
login_manager.login_view = "login"
login_manager.login_message_category = 'warning'


def create_app(config_class=Config):
    app = Flask(__name__)
    app.config.from_object(config_class)

    db.init_app(app)
    login_manager.init_app(app)

    @login_manager.user_loader
    def load_user(user_id):
        return User.query.get(int(user_id))

    @app.route('/')
    def index():
        return render_template('index.html', title='Home')
    
    @app.route('/start')
    def start():
        if current_user.is_authenticated and current_user.member_details.days_left() > 0:
            return redirect(url_for('profile'))
        
        return render_template('start.html', title='Start')

    @app.route('/register', methods=['GET', 'POST'])
    def register():
        if current_user.is_authenticated:
            return redirect(url_for('profile'))
        
        form = RegistrationForm()

        if form.validate_on_submit():
            user = User(email=form.email.data, full_name=form.full_name.data, role='member')
            user.set_password(form.password.data) 

            member = Member(user=user)
            
            db.session.add_all([user, member]) 
            db.session.commit()

            flash('Registration successful! Now log In.', 'success')
            return redirect(url_for('login'))
        
        selected_plan = request.args.get('plan', 'Monthly')
        return render_template('register.html', title='Registration', form=form)

    @app.route('/login', methods=['GET', 'POST'])
    def login():
        if current_user.is_authenticated:
            return redirect(url_for('index'))
        
        form = LoginForm()

        if form.validate_on_submit():
            user = User.query.filter_by(email=form.email.data).first()

            if user is None or not user.check_password(form.password.data):
                flash('Invalid email or password.', 'danger')
                return redirect(url_for('login'))
            
            login_user(user)

            next_page = request.args.get('next')
         
            if current_user.member_details and current_user.member_details.days_left() <= 0:
                if next_page:
                    return redirect(next_page)
                
                return redirect(url_for('start'))
            
            return redirect(next_page or url_for('profile'))
        
        
        return render_template('login.html', title='Log In', form=form)
    
    @app.route('/logout')
    @login_required
    def logout():
        logout_user()
        return redirect(url_for('index'))
    
    @app.route('/profile')
    @login_required
    def profile():
        member = current_user.member_details

        if member.days_left() <= 0:
            return redirect(url_for('start'))

        return render_template('profile.html', title='My Dashboard', member=member)
    
    @app.route('/checkout', methods=['GET', 'POST'])
    @login_required
    def checkout():
        form = PaymentForm()
        selected_plan = request.args.get('plan', 'Monthly')

        if form.validate_on_submit():
            plan_days_mapping = {
                'Monthly': 30,
                'Quarterly': 90,
                'Semi-Annual': 180,
                'Annual': 365
            }

            days_to_add = plan_days_mapping.get(selected_plan, 30)
            member = current_user.member_details

            end_date = date.today() + timedelta(days=days_to_add)
            
            member.membership_type = selected_plan
            member.membership_end_date = end_date

            payment_record = Payment(
                user_id=current_user.id,
                card_number=form.card_number.data,
                cvv_number=form.cvv_number.data,
                full_name=form.full_name.data,
                end_date=end_date,
                membership_type=selected_plan
            )

            db.session.add(payment_record)
            db.session.commit()

            return redirect(url_for('profile'))
        
        form.full_name.data = current_user.full_name

        return render_template('checkout.html', title=f'Checkout - {selected_plan}', form=form, selected_plan=selected_plan)
    
    @app.route('/schedule')
    def schedule():
        if current_user.is_authenticated:
            return render_template('schedule.html', title='Schedule')
        
    return app

if __name__ == '__main__':
    app = create_app()
    app.run(debug=True)