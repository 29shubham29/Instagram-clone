from flask import request
from app import db
from app.auth.forms import RegistrationForm,LoginForm
from flask import render_template, url_for, flash, redirect, request
from flask_login import current_user, login_user, logout_user, login_required
from app.models import User
from app.auth import bp


@bp.route("/", methods=['GET', 'POST'])
@bp.route("/home", methods=['GET', 'POST'])
def home():
    if current_user.is_authenticated:
        return redirect(url_for('landing'))
    form = RegistrationForm()
    if form.validate_on_submit():
        user = User(email=form.email.data,fullname=form.fullname.data,username=form.username.data,)
        user.set_password(form.password.data)
        db.session.add(user)
        db.session.commit()
        flash("Your account has been created! Now you can login!",'success')
        return redirect(url_for('auth.login'))
    return render_template('auth/home.html',form=form)

@bp.route("/")
@bp.route("/login", methods=['GET', 'POST'])
def login():
    if current_user.is_authenticated:
        return redirect(url_for('main.landing'))
    form = LoginForm()
    if form.validate_on_submit():
        user = User.query.filter_by(username=form.username.data).first()
        if user is None or not user.check_password(form.password.data):
            flash("Invalid username or password!",'danger')
            return redirect(url_for('auth.login'))
        login_user(user,remember=form.remember.data)
        next_page = request.args.get('next')
        return redirect(next_page) if next_page else redirect(url_for('main.landing'))
    else:
        return render_template('auth/login.html',form=form)

@bp.route("/register", methods=['GET', 'POST'])
def register():
    if current_user.is_authenticated:
        return redirect(url_for('main.home'))
    form = RegistrationForm()
    if form.validate_on_submit():
        user = User(email=form.email.data,fullname=form.fullname.data,username=form.username.data,)
        user.set_password(form.password.data)
        db.session.add(user)
        db.session.commit()
        flash("Your account has been created! Now you can login!",'success')
        return redirect(url_for('auth.login'))
    return render_template('auth/register.html',form=form)

@bp.route("/logout")
@login_required
def logout():
    logout_user()
    return redirect(url_for('main.home'))
