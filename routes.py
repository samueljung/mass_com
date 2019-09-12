from flask import render_template, url_for, flash, redirect, request
from flaskblog import app, db, bcrypt
from flaskblog.forms import RegistrationForm, LoginForm
from flaskblog.models import User, Post
from flask_login import login_user, current_user, logout_user, login_required

import os
BRANDLOGO_FOLDER = os.path.join('static', 'images')
ALLOWED_EXTENSIONS = set(['txt', 'pdf', 'png', 'jpg', 'jpeg', 'gif'])
app.config['UPLOAD_FOLDER'] = BRANDLOGO_FOLDER

posts = [
    {
        'author': 'Sam Jung',
        'title': 'Blog Post 1',
        'content': 'First Post Content. This is the first runway that I have found to be quite exciting. Standngin in front of a wide audience was quite exhilarating.',
        'date_posted': 'May 22, 2019'
    },
    {
        'author': 'Zang Sang',
        'title': 'Blog Post 2',
        'content': 'Second Post Content',
        'date_posted': 'May 22, 2019'
    }
]



@app.route("/")
@app.route("/home")
def home():
    full_filename = os.path.join(BRANDLOGO_FOLDER, 'image-2019-06-07.jpg')
    return render_template('home.html', title='Home', image=full_filename)

@app.route("/blog")
def blog():
    full_filename1 = os.path.join(BRANDLOGO_FOLDER, 'Brunello_Runway.jpg')
    return render_template('blog.html', posts=posts, image=full_filename1)

@app.route("/music")
def music():
    return render_template('music.html', title='Music')

@app.route("/art")
def art():
    return render_template('art.html', title='Art')

@app.route("/register", methods=['GET', 'POST'])
def register():
    if current_user.is_authenticated:
        return redirect(url_for('blog'))
    form = RegistrationForm()
    if form.validate_on_submit():
        hashed_password = bcrypt.generate_password_hash(form.password.data).decode('utf-8')
        user = User(username=form.username.data, email=form.email.data, password=hashed_password)
        db.session.add(user)
        db.session.commit()
        flash(f'Your account has been created! You are now able to log in', 'success')
        return redirect(url_for('login'))
    return render_template('register.html', title = 'Register', form=form)

@app.route("/login", methods=['GET', 'POST'])
def login():
    if current_user.is_authenticated:
        return redirect(url_for('blog'))
    form = RegistrationForm()
    form = LoginForm()
    if form.validate_on_submit():
        user = User.query.filter_by(email=form.email.data).first()
        if user and bcrypt.check_password_hash(user.password, form.password.data):
            login_user(user, remember=form.remember.data)
            next_page = request.args.get('next')
            return redirect(next_page) if next_page else redirect(url_for('blog'))
        else:
            flash('Login Unsuccessful. Plese check email and password', 'danger')
    return render_template('login.html', title = 'Login', form=form)


@app.route("/logout")
def logout():
    logout_user()
    return redirect(url_for('blog'))

@app.route("/account")
@login_required
def account():
    return render_template('account.html', title = 'Account')
