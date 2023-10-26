from flask import Flask, redirect, url_for
app = Flask(__name__)

@app.route('/index')
def index():
    return 'Default root'