import secrets
from PIL import Image
import os
from app import db
from flask import request
from app.main.forms import UpdateForm, PostForm
from flask import render_template, url_for, flash, redirect, request
from flask_login import current_user, login_user, logout_user, login_required
from app.models import User, Post
from app.main import bp

@bp.route("/main")
@login_required
def landing():
    posts = current_user.followed_posts().all()
    print(posts)
    return render_template('landing.html', title = "Home", posts=posts)

def save_picture(form_picture):
    random_hex=secrets.token_hex(8)
    _,f_ext=os.path.splitext(form_picture.filename)
    picture_fn = random_hex+f_ext
    picture_path = os.path.join(app.root_path,'static/pictures', picture_fn)
    output_size = (300,300)
    i = Image.open(form_picture)
    i.thumbnail(output_size)
    i.save(picture_path)


    return picture_fn


@bp.route("/account",methods = ['GET','POST'])
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
    image_file = url_for('static',filename=f'pictures/{current_user.image_file}')
    posts = Post.query.filter_by(user_id=current_user.id)
    return render_template('account.html',title="Account",image_file=image_file,posts=posts, form=form)

#user template
@bp.route("/user/<username>")
def user(username):
    user = User.query.filter_by(username=username).first_or_404()
    posts = [
            {'author': user, 'body': 'Test post #1'},
            {'author': user, 'body': 'Test post #2'}
        ]
    image_file = url_for('static',filename=f'pictures/{user.image_file}')
    return render_template('user.html',user=user,posts=posts,image_file=image_file)

@bp.route('/follow/<username>')
@login_required
def follow(username):
    user = User.query.filter_by(username=username).first()
    image_file = url_for('static',filename=f'pictures/{user.image_file}')
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

@bp.route('/unfollow/<username>')
@login_required
def unfollow(username):
    user = User.query.filter_by(username=username).first()
    image_file = url_for('static',filename=f'pictures/{user.image_file}')
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


@bp.route("/post/new",methods = ['GET','POST'])
@login_required
def new_post():
    image_file = url_for('static',filename=f'pictures/{current_user.image_file}')
    form = PostForm()
    if form.validate_on_submit():
        picture_file = save_picture(form.image_file.data)
        post = Post(image_file=picture_file,caption=form.caption.data,user_id=current_user.id)
        db.session.add(post)
        db.session.commit()
        flash('Hurray you posted something new!!','success')
        return redirect(url_for('landing'))
    return render_template('create_post.html',title='New Post',form=form,image_file=image_file)

@bp.route('/like/<int:post_id>/<action>')
@login_required
def like_action(post_id, action):
    post = Post.query.filter_by(id=post_id).first_or_404()
    if action == 'like':
        current_user.like_post(post)
        db.session.commit()
    if action == 'unlike':
        current_user.unlike_post(post)
        db.session.commit()
    return redirect(request.referrer)


