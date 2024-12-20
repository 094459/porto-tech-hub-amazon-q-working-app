from flask import render_template, redirect, url_for, flash, request, current_app
from flask_login import login_user, logout_user, login_required
from models import User
from models.database import db
from forms import RegisterForm
from . import auth_bp
import traceback
from datetime import datetime

# @auth_bp.route('/register', methods=['GET', 'POST'])
# def register():
#     form = RegisterForm()
#     if form.validate_on_submit():
#         user = User.query.filter_by(email=form.email.data).first()
#         if user:
#             flash('Email already registered', 'error')
#             return redirect(url_for('auth.register'))
        
#         new_user = User(email=form.email.data)
#         new_user.set_password(form.password.data)
#         db.session.add(new_user)
#         db.session.commit()
        
#         flash('Registration successful! Please login.', 'success')
#         return redirect(url_for('auth.login'))
#     return render_template('auth/register.html', form=form)

@auth_bp.route('/register', methods=['GET', 'POST'])
def register():
    if request.method == 'POST':
        email = request.form.get('email')
        password = request.form.get('password')
        
        # Check if user already exists
        user = User.query.filter_by(email=email).first()
        if user:
            flash('Email address already exists')
            return redirect(url_for('auth.register'))
        
        # Create new user
        new_user = User(
            email=email
        )
        new_user.set_password(password)
        
        try:
            db.session.add(new_user)
            db.session.commit()
            flash('Registration successful! Please login.')
            return redirect(url_for('auth.login'))
        except Exception as e:
            db.session.rollback()
            flash('An error occurred. Please try again.')
            return redirect(url_for('auth.register'))
            
    # If GET request, display registration form
    return render_template('auth/register.html')

@auth_bp.route('/login', methods=['GET', 'POST'])
def login():
    if request.method == 'POST':
        email = request.form.get('email')
        password = request.form.get('password')
        
        user = User.query.filter_by(email=email).first()
        
        if user and user.check_password(password):
            login_user(user)
            user.last_login = datetime.utcnow()
            db.session.commit()
            
            # Redirect to the main index page instead of 'survey.list'
            return redirect(url_for('main.index'))
        else:
            flash('Please check your login details and try again.')
            return redirect(url_for('auth.login'))
    
    return render_template('auth/login.html')


@auth_bp.route('/logout')
@login_required
def logout():
    logout_user()
    flash('You have been logged out.', 'info')
    return redirect(url_for('main.index'))