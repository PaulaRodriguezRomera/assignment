from flask import Flask, redirect, url_for, render_template, flash, request
from flask_wtf import FlaskForm
from wtforms import StringField, SubmitField
from wtforms.validators import DataRequired
from flask_sqlalchemy import SQLAlchemy
from datetime import datetime
from wtforms.widgets import TextArea
from flask_migrate import Migrate
from flask_ckeditor import CKEditor
from sqlalchemy.dialects import postgresql



# Create a Flask instance.
app = Flask(__name__)
app.app_context().push()

#Adds CKEditor
ckeditor = CKEditor(app)

# add databases

# old SQLITE DB
#app.config['SQLALCHEMY_DATABASE_URI'] = 'sqlite:///users.db'

# new MYSQL DB
app.config['SQLALCHEMY_DATABASE_URI'] = 'postgres://u5n2qh0kc48564:pb58f4334c16f031a56822fc5581bddec20c08c0c40146cb6c1ef3e5c17e1e01f@ec2-54-236-100-37.compute-1.amazonaws.com:5432/dd7t5adp6mulsk'

# secret key
app.config['SECRET_KEY'] = "my secret key for now"
# initialise the database
db = SQLAlchemy(app)
migrate = Migrate(app, db)

#Creates a Blog Post model
class Posts(db.Model):
    id = db.Column(db.Integer, primary_key=True)
    title = db.Column(db.String(255))
    content = db.Column(db.Text)
    author = db.Column(db.String())
    date_posted = db.Column(db.DateTime, default=datetime.utcnow)
    slug = db.Column(db.String(256))

#Creates a Posts form
class PostForm(FlaskForm):
    title = StringField("Title", validators=[DataRequired()])
    content = StringField("Content", validators=[DataRequired()], widget=TextArea())
    author = StringField("Author", validators=[DataRequired()])
    slug = StringField("Slug", validators=[DataRequired()])
    submit = SubmitField("Submit")

#Edits posts
@app.route('/posts/edit/<int:id>', methods=['GET', 'POST'])
def edit_post(id):
    post = Posts.query.get_or_404(id)
    form = PostForm()
    if form.validate_on_submit():
        post.title = form.title.data
        post.author = form.author.data
        post.slug = form.slug.data
        post.content = form.content.data

        #updates database
        db.session.add(post)
        db.session.commit()
        flash("Post has been updated!")
        return redirect(url_for('posts', id=post.id))
    form.title.data = post.title
    form.author.data = post.author
    form.slug.data = post.slug
    form.content.data = post.content
    return render_template('edit_post.html', form=form)

#Deletes posts
@app.route('/posts/delete/<int:id>')
def delete_post(id):
    post_to_delete = Posts.query.get_or_404(id)

    try:
        db.session.delete(post_to_delete)
        db.session.commit()

        # Returns a message
        flash("Blog Post was deleted!")

        # Grab all the posts from the database
        posts = Posts.query.order_by(Posts.date_posted)
        return render_template("posts.html", posts=posts)

    except:
        # Returns an error message
        flash("There was a problem, please try again!")
        # Grab all the posts from the database
        posts = Posts.query.order_by(Posts.date_posted)
        return render_template("posts.html", posts=posts)

#Adds a page with posts
@app.route('/posts')
def posts():
    #Grabs all the posts from the database
    posts = Posts.query.order_by(Posts.date_posted)
    return render_template("posts.html", posts=posts)

#Adds a Post Page
@app.route('/add_post', methods=['GET', 'POST'])
def add_post():
    form = PostForm()

    if form.validate_on_submit():
        post = Posts(title=form.title.data, content=form.content.data, author=form.author.data, slug=form.slug.data)
        # Clear the form
        form.title.data = ''
        form.content.data = ''
        form.author.data = ''
        form.slug.data = ''

        # Adds post data to database
        db.session.add(post)
        db.session.commit()
        #Returns a message
        flash("Blog Post Submitted Successfully!")

    #Redirect to the webpage
    return render_template("add_post.html", form=form)

#creates User model
class Users(db.Model):
    id = db.Column(db.Integer, primary_key=True)
    name = db.Column(db.String(120), nullable=False)
    email = db.Column(db.String(120), nullable=False, unique=True)
    date_added = db.Column(db.DateTime, default=datetime.utcnow)

    # create a string
    def __repr__(self):
        return '<Name %r>' % self.name

# creates a Form Class
class UserForm(FlaskForm):
    name = StringField("Name", validators=[DataRequired()])
    email = StringField("Email", validators=[DataRequired()])
    submit = SubmitField("Submit")

# updates database record
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


# creates a Form Class
class NamerForm(FlaskForm):
    name = StringField("What's Your Name", validators=[DataRequired()])
    submit = SubmitField("Submit")

# Creates route decorators

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
