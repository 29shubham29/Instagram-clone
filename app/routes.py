import secrets
from PIL import Image
import os
from app import app,db
from flask import request
from app.forms import UpdateForm, PostForm
from flask import render_template, url_for, flash, redirect, request
from flask_login import current_user, login_user, logout_user, login_required
from app.models import User, Post


# @app.route("/index")
# def index():
#     return render_template('landing.html',posts=posts)

