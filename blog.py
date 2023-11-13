from flask import Flask, redirect, url_for, render_template
from flask_wtf import FlaskForm
from wtforms import StringField, SubmitField
from wtforms.validators import DataRequired

# Create a Flask instance.
app = Flask(__name__)
app.config['SECRET_KEY'] = "my secret key for now"

# create a Form Class
class NamerForm(FlaskForm):
    name = StringField("What's Your Name", validators=[DataRequired()])
    submit = SubmitField("Submit")

# Create route decorators

# localhost/
@app.route('/')
def index():
    return render_template("index.html")

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


# Custom Error Pages
# Invalid URL
@app.errorhandler(404)
def page_not_found(e):
    return render_template("404.html"), 404

# Internal Server Error
@app.errorhandler(500)
def internal_server_error(e):
    return render_template("500.html"), 500

#Name Page
@app.route('/name', methods=['GET', 'POST'])
def name():
    name = None
    form = NamerForm()

    #validate form
    if form.validate_on_submit():
        name = form.name.data
        form.name.data = ''

    return render_template("name.html", name=name, form=form)

