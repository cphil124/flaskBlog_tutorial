from flaskBlog.models import User, Post
from flaskBlog import app, db, bcrypt
from flask import render_template, url_for, flash, redirect
from flaskBlog.forms import RegistrationForm, LoginForm

posts = [
    {
        'author': 'Corey Schafer',
        'title':'Blog Post 1',
        'content': 'First post content',
        'date_posted':'April 18, 2018'
    },
    {
        'author': 'Cameron Phillips',
        'title':'Form Post 1',
        'content': 'First Survey Questions',
        'date_posted':'March 29, 2020'
    }
]

@app.route("/")
@app.route("/home")
def home():
    return render_template('home.html', posts=posts)

@app.route("/about")
def about():
    return render_template('about.html', title='About')

@app.route('/register', methods=['GET','POST'])
def register():
    form = RegistrationForm()
    if form.validate_on_submit():
        hashed_password = bcrypt.generate_password_hash(form.password.data).decode('utf-8')
        user = User(username=form.username.data, email=form.email.data, password=hashed_password)
        db.session.add(user)
        db.session.commit()
        flash(f'Your account has been created! You are now able to log in', 'success')
        return redirect(url_for('login'))
    return render_template('register.html', title='Register', form=form)

@app.route('/login', methods=['GET','POST'])
def login():
    form = LoginForm()
    if form.validate_on_submit():
        if form.email.data == 'admin@blog.com' and form.password.data == 'password':
            flash('You have been logged in!', 'success')
            return redirect(url_for('home'))
        else:
            flash('Login Unsuccessful. Please check username and password', 'danger')
    return render_template('login.html', title='Login', form=form)
