from flask import Flask, render_template, redirect, session
from flask_bs4 import Bootstrap
from flask_wtf import FlaskForm
from wtforms import StringField, SubmitField, PasswordField
from wtforms.validators import DataRequired

app = Flask(__name__)
bootstrap = Bootstrap(app)
app.config['SECRET_KEY'] = 'downfield#)HRO){fe09fu3fhf){J(@{)o[ds9jhd;dw'  # example


users = {
    'username': 'admin',
    'userpass': 'admin',
    'firstname': 'Admin',
    'lastname': 'Admin'
}


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
    if login.validate_on_submit():
        username = login.userLogin.data
        userpass = login.userPass.data
        if username == users['username'] and userpass == users['userpass']:
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
    return redirect('/login')


# noinspection PyUnusedLocal
@app.errorhandler(500)
def internal_server_error(e):
    return render_template('500.html', title='Internal server error'), 500


@app.route('/dashboard')
def dashboard():
    return render_template('dashboard.html', title='Dashboard', username=session.get('username'))


if __name__ == "__main__":
    app.run(debug=True)
