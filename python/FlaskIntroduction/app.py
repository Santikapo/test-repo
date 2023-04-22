from flask import Flask, render_template, url_for
#from forms import RegistrationForm, LoginForm
from flask_sqlalchemy import SQLAlchemy
from sqlalchemy import Column
from datetime import datetime


app = Flask(__name__)
app.config['SQLALCHEMY_DATABASE_URI'] = 'sqlite:///friends.db'
app.config['SECRET_KEY'] = '7728f2db76465724aa8976c6580e2a9f'
# initialize the data
db = SQLAlchemy(app)





@app.route('/')
def home():
    return render_template('home.html', title='Home')
"""
@app.route('/register')
def register():
    form = RegistrationForm()
    return render_template('register.html', title='Register', form=form)

@app.route('/login')
def login():
    form = LoginForm()
    return render_template('login.html', title='Login', form=form)

"""


if __name__ == "__main__":
    app.run(debug=True)