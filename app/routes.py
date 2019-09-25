import secrets
from PIL import Image
import os
from app import app,db
from flask import request
from app.forms import RegistrationForm,LoginForm, UpdateForm, PostForm
from flask import render_template, url_for, flash, redirect, request
from flask_login import current_user, login_user, logout_user, login_required
from app.models import User


@app.route("/index")
def index():
    posts = [
        {
            'author':'shubham.pandey',
            'title':'First',
            'content':'hey this is my first blog post'
        },
        {
            'author':'shubham.pandey',
            'title':'First',
            'content':'hey this is my first blog post'
        }
    ]
    image_file = url_for('static',filename=f'profile_pics/{current_user.image_file}')
    return render_template('landing.html',posts=posts,image_file=image_file)
@app.route("/", methods=['GET', 'POST'])
@app.route("/home", methods=['GET', 'POST'])
def home():
    if current_user.is_authenticated:
        return redirect(url_for('index'))
    form = RegistrationForm()
    if form.validate_on_submit():
        user = User(email=form.email.data,fullname=form.fullname.data,username=form.username.data,)
        user.set_password(form.password.data)
        db.session.add(user)
        db.session.commit()
        flash("Your account has been created! Now you can login!",'success')
        return redirect(url_for('login'))
    return render_template('home.html',form=form)

@app.route("/logout")
@login_required
def logout():
    logout_user()
    return redirect(url_for('index'))

@app.route("/main")
def landing():
    return render_template('landing.html')

@app.route("/")
@app.route("/login", methods=['GET', 'POST'])
def login():
    posts = [
        {
            'author':'shubham.pandey',
            'title':'First',
            'content':'hey this is my first blog post'
        },
        {
            'author':'shubham.pandey',
            'title':'First',
            'content':'hey this is my first blog post'
        }
    ]
    if current_user.is_authenticated:
        return redirect(url_for('landing'),posts=posts)
    form = LoginForm()
    # if form.validate_on_submit():
    if request.method == 'POST' and form.validate():
        print(request.form,request)
        user = User.query.filter_by(username=form.username.data).first()
        if user is None or not user.check_password(form.password.data):
            flash("Invalid username or password!",'danger')
            return redirect(url_for('login'))
        login_user(user,remember=form.remember.data)
        next_page = request.args.get('next')
        return redirect(next_page) if next_page else redirect(url_for('landing'))
    else:
        return render_template('login.html',form=form)

@app.route("/register", methods=['GET', 'POST'])
def register():
    if current_user.is_authenticated:
        return redirect(url_for('home'))
    form = RegistrationForm()
    if form.validate_on_submit():
        user = User(email=form.email.data,fullname=form.fullname.data,username=form.username.data,)
        user.set_password(form.password.data)
        db.session.add(user)
        db.session.commit()
        flash("Your account has been created! Now you can login!",'success')
        return redirect(url_for('login'))
    return render_template('register.html',form=form)

def save_picture(form_picture):
    random_hex=secrets.token_hex(8)
    _,f_ext=os.path.splitext(form_picture.filename)
    picture_fn = random_hex+f_ext
    picture_path = os.path.join(app.root_path,'static/profile_pics', picture_fn)

    output_size = (125,125)
    i = Image.open(form_picture)
    i.thumbnail(output_size)

    i.save(picture_path)

    return picture_fn


@app.route("/account",methods = ['GET','POST'])
@login_required
def account():
    form = UpdateForm()
    if form.validate_on_submit():
        if form.image_file.data:
            picture_file = save_picture(form.image_file.data)
            current_user.image_file= picture_file
        current_user.username = form.username.data
        current_user.about_me = form.about_me.data
        db.session.commit()
        flash("Your account has been created",'success')
        return redirect(url_for('account'))
    elif request.method == 'GET':
        form.username.data = current_user.username
        form.about_me.data = current_user.about_me
    image_file = url_for('static',filename=f'profile_pics/{current_user.image_file}')
    posts = [
        {
            'author':'shubham.pandey',
            'title':'First',
            'content':'hey this is my first blog post'
        },
        {
            'author':'shubham.pandey',
            'title':'First',
            'content':'hey this is my first blog post'
        }
    ]
    return render_template('account.html',title="Account",image_file=image_file,posts=posts, form=form)

#user template
@app.route("/user/<username>")
def user(username):
    user = User.query.filter_by(username=username).first_or_404()
    posts = [
            {'author': user, 'body': 'Test post #1'},
            {'author': user, 'body': 'Test post #2'}
        ]
    image_file = url_for('static',filename=f'profile_pics/{user.image_file}')
    return render_template('user.html',user=user,posts=posts,image_file=image_file)

@app.route('/follow/<username>')
@login_required
def follow(username):
    user = User.query.filter_by(username=username).first()
    image_file = url_for('static',filename=f'profile_pics/{user.image_file}')
    if user is None:
        flash('User {} not found.'.format(username))
        return redirect(url_for('landing'))
    if user == current_user:
        flash('You cannot follow yourself!')
        return redirect(url_for('user', username=username))
    current_user.follow(user)
    db.session.commit()
    flash('You are following {}!'.format(username),'success')
    return redirect(url_for('user', username=username,image_file=image_file))

@app.route('/unfollow/<username>')
@login_required
def unfollow(username):
    user = User.query.filter_by(username=username).first()
    image_file = url_for('static',filename=f'profile_pics/{user.image_file}')
    if user is None:
        flash('User {} not found.'.format(username))
        return redirect(url_for('landing'))
    if user == current_user:
        flash('You cannot unfollow yourself!','danger')
        return redirect(url_for('user', username=username))
    current_user.unfollow(user)
    db.session.commit()
    flash('You are not following {}.'.format(username),'info')
    return redirect(url_for('user', username=username,image_file=image_file))


@app.route("/post/new",methods = ['GET','POST'])
@login_required
def new_post():
    image_file = url_for('static',filename=f'profile_pics/{current_user.image_file}')
    form = PostForm()
    if form.validate_on_submit():
        flash('Message sucessful')
        return redirect(url_for('index'))
    return render_template('create_post.html',title='New Post',form=form,image_file=image_file)