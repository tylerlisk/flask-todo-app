from flask import Blueprint, render_template, redirect, request, flash, url_for
from flask_login import login_user, logout_user, login_required, current_user
from .models import db, User
from .extensions import login_manager, bcrypt

auth = Blueprint('auth', __name__)

@login_manager.user_loader
def load_user(user_id):
    return User.query.get(user_id)

@auth.route('/register', methods=['GET', 'POST'])
def register():
    if request.method == 'POST':
        username = request.form.get('username')
        password = request.form.get('password')
        new_user = User(username=username, password=bcrypt.generate_password_hash(password))

        db.session.add(new_user)
        db.session.commit()

        flash('Account registered, you may now login.', 'success')
        return redirect(url_for(".login"))
    
    return render_template('register.html')

@auth.route('/login', methods=['GET', 'POST'])
def login():
    if request.method == 'POST':
        username = request.form.get('username')
        password = request.form.get('password')

        user = User.query.filter_by(username=username).first()

        if user and bcrypt.check_password_hash(user.password, password):
            login_user(user)
            flash('You are logged in!', 'success')
            return redirect(url_for("main.home"))
        else:
            flash('Invalid credentials. Please try again', 'danger')
    
    return render_template('login.html')

@auth.route("/logout")
@login_required
def logout():
    logout_user()
    return redirect(url_for(".login"))
