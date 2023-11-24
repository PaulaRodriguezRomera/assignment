from flask import Flask, redirect, url_for, render_template, flash, request
from flask_wtf import FlaskForm
from wtforms import StringField, SubmitField
from wtforms.validators import DataRequired
from flask_sqlalchemy import SQLAlchemy
from datetime import datetime

# Create a Flask instance.
app = Flask(__name__)
app.app_context().push()

# add databases

# old SQLITE DB
#app.config['SQLALCHEMY_DATABASE_URI'] = 'sqlite:///users.db'

# new MYSQL DB
app.config['SQLALCHEMY_DATABASE_URI'] = 'mysql+pymysql://our_user:password123@localhost/our_user'

# secret key
app.config['SECRET_KEY'] = "my secret key for now"
# initialise the database
db = SQLAlchemy(app)

# create model
class Users(db.Model):
    id = db.Column(db.Integer, primary_key=True)
    name = db.Column(db.String(120), nullable=False)
    email = db.Column(db.String(120), nullable=False, unique=True)
    date_added = db.Column(db.DateTime, default=datetime.utcnow)

    # create a string
    def __repr__(self):
        return '<Name %r>' % self.name

# create a Form Class
class UserForm(FlaskForm):
    name = StringField("Name", validators=[DataRequired()])
    email = StringField("Email", validators=[DataRequired()])
    submit = SubmitField("Submit")

# update database record
@app.route('/update/<int:id>', methods=['GET', 'POST'])
def update(id):
    form = UserForm()
    name_to_update = Users.query.get_or_404(id)
    if request.method == "POST":
        name_to_update.name = request.form['name']
        name_to_update.email = request.form['email']
        try:
            db.session.commit()
            flash("User updated successfully!")
            return render_template("update.html", form=form, name_to_update=name_to_update)
        except:
            db.session.commit()
            flash("Error, looks like there was a problem. Try again!")
            return render_template("update.html", form=form, name_to_update=name_to_update)
    else:
        return render_template("update.html", form=form, name_to_update=name_to_update)


# create a Form Class
class NamerForm(FlaskForm):
    name = StringField("What's Your Name", validators=[DataRequired()])
    submit = SubmitField("Submit")

# Create route decorators

# localhost/
@app.route('/')
def index():
    return render_template("index.html")

# localhost/login
@app.route('/login')
def login():
    return render_template("login.html")

# localhost/logout
@app.route('/logout')
def logout():
    return render_template("logout.html")

# localhost/user/name
@app.route('/user/<name>')
def user(name):
    return render_template("user.html", user_name=name)

# localhost/aboutus
@app.route('/aboutus')
def aboutus():
    return render_template("aboutus.html")

# localhost/contact
@app.route('/contact')
def contact():
    return render_template("contact.html")

# localhost/profile
@app.route('/profile')
def profile():
    return render_template("profile.html")

# localhost/article
@app.route('/article')
def article():
    return render_template("article.html")

# localhost/register
@app.route('/register')
def register():
    return render_template("register.html")

# Custom Error Pages
# Invalid URL
@app.errorhandler(404)
def page_not_found(e):
    return render_template("404.html"), 404

# Internal Server Error
@app.errorhandler(500)
def internal_server_error(e):
    return render_template("500.html"), 500

# Name Page
@app.route('/name', methods=['GET', 'POST'])
def name():
    name = None
    form = NamerForm()

    #validate form
    if form.validate_on_submit():
        name = form.name.data
        form.name.data = ''
        flash("Form Submitted Successfully!")

    return render_template("name.html", name=name, form=form)

# user page
@app.route('/user/add', methods=['GET', 'POST'])
def add_user():
    name = None
    form = UserForm()
    if form.validate_on_submit():
        user = Users.query.filter_by(email=form.email.data).first()
        if user is None:
            id = 1
            user = Users(name=form.name.data, email=form.email.data)
            db.session.add(user)
            db.session.commit()
        name = form.name.data
        form.name.data = ''
        form.email.data = ''
        flash("User Added Successfully!")
    our_users = Users.query.order_by(Users.date_added)
    return render_template("add_user.html", form=form, name=name, our_users=our_users)
