from flask import Flask, render_template
from flask_bs4 import Bootstrap
from flask_wtf import FlaskForm
from wtforms import StringField, SubmitField, PasswordField
from wtforms.validators import DataRequired

app = Flask(__name__)
bootstrap = Bootstrap(app)
app.config['SECRET_KEY'] = 'downfield#)HRO){fe09fu3fhf){J(@{)o[ds9jhd;dw'  # example


class LoginForm(FlaskForm):
    """
    Login form
    """
    userLogin = StringField('Username', validators=[DataRequired()])
    userPass = PasswordField('Password', validators=[DataRequired()])
    submit = SubmitField('Login')


users = {
    'username': 'admin',
    'userpass': 'admin',
    'firstname': 'Admin',
    'lastname': 'Admin'
}


@app.route('/')
def index():
    return render_template('index.html', title="Home")


@app.route('/login', methods=['POST', 'GET'])
def log_in():
    login = LoginForm()
    return render_template('login.html', title='Login', login=login)


if __name__ == "__main__":
    app.run(debug=True)
