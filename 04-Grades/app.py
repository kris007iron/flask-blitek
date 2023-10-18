import json

from flask import Flask, render_template, redirect, session
from flask_bs4 import Bootstrap
from flask_wtf import FlaskForm
from wtforms import StringField, SubmitField, PasswordField
from wtforms.validators import DataRequired
from flask_moment import Moment
from datetime import datetime

app = Flask(__name__)
bootstrap = Bootstrap(app)
app.config['SECRET_KEY'] = 'downfield#)HRO){fe09fu3fhf){J(@{)o[ds9jhd;dw'  # example
moment = Moment(app)
date = datetime.now()


class LoginForm(FlaskForm):
    """
    Login form
    """
    userLogin = StringField('Username', validators=[DataRequired()])
    userPass = PasswordField('Password', validators=[DataRequired()])
    submit = SubmitField('Login')


# app route main page
@app.route('/')
def index():
    return render_template('index.html', title="Home")


@app.route('/login', methods=['POST', 'GET'])
def log_in():
    login = LoginForm()
    with open("data/users.json") as users_file:
        users = json.load(users_file)
        users_file.close()
    if login.validate_on_submit():
        username = login.userLogin.data
        userpass = login.userPass.data
        if username == users['username'] and userpass == users['userpass']:
            session['firstname'] = users['firstname']
            session['username'] = username
            return redirect('/dashboard')
    return render_template('login.html', title='Login', login=login)


# noinspection PyUnusedLocal
@app.errorhandler(404)
def page_not_found(e):
    return render_template('404.html', title='Page not found'), 404


@app.route('/logout')
def log_out():
    session.pop('username')
    session.pop('firstname')
    return redirect('/login')


# noinspection PyUnusedLocal
@app.errorhandler(500)
def internal_server_error(e):
    return render_template('500.html', title='Internal server error'), 500


def calc_mean(grades):
    mean = []
    for key, value in grades.items():
        for k, v in value.items():
            if k != 'yearly':
                summed = 0
                counted = 0
                for k2, v2 in v.items():
                    if k2 != 'interim':
                        for el in v2:
                            summed += el
                            counted += 1
                mean.append(round(summed / counted, 2))
    mean.append((mean[0]+mean[1]) / 2)
    return mean


def return_finals(means):
    finals = []
    for mean_o in means:
        if mean_o < 2:
            finals.append("niedostateczny")
        elif mean_o < 2.75:
            finals.append("dopuszczający")
        elif mean_o < 3.75:
            finals.append("dostateczny")
        elif mean_o < 4.75:
            finals.append("dobry")
        elif mean_o <= 5:
            finals.append("bardzo dobry")
        else:
            finals.append("celujący")
    return finals


@app.route('/dashboard')
def dashboard():
    with open("data/grades.json") as grades_file:
        grades = json.load(grades_file)
        grades_file.close()
    mean = calc_mean(grades)
    return render_template('dashboard.html', title='Dashboard', username=session.get('username'),
                           firstname=session.get('firstname'), date=date, grades=grades, mean=mean,
                           finals=return_finals(mean))


if __name__ == "__main__":
    app.run(debug=True)
