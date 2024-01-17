import os

from flask import Flask, render_template, redirect, url_for, flash
from flask_bs4 import Bootstrap
from flask_login import UserMixin, LoginManager
from flask_sqlalchemy import SQLAlchemy
from flask_wtf import FlaskForm
from wtforms.fields.simple import EmailField, PasswordField, SubmitField
from wtforms.validators import DataRequired, Email

app = Flask(__name__)
bootstrap = Bootstrap(app)
app.config['SECRET_KEY'] = 'j4bng34limit89h(PHO#RP(H*f043hgo;b43n4o83r'

basedir = os.path.abspath(os.path.dirname(__file__))
app.config['SQLALCHEMY_DATABASE_URI'] = 'sqlite:///' + os.path.join(basedir, 'data/users.sqlite')
db = SQLAlchemy(app)


class Users(db.Model, UserMixin):
    id = db.Column(db.Integer, primary_key=True)
    user_name = db.Column(db.String(64))
    user_lastname = db.Column(db.String(64))
    user_email = db.Column(db.String(120), unique=True)
    user_pass = db.Column(db.String(128))

    def is_authenticated(self):
        return True


loginManager = LoginManager()
loginManager.init_app(app)
loginManager.login_view = 'login'
loginManager.login_message = 'Please login to access this page.'
loginManager.login_message_category = 'warning'


@loginManager.user_loader
def load_user(user_id):
    return Users.query.filter_by(id=user_id).first()

class LoginForm(FlaskForm):
    user_email = EmailField('Email', validators=[DataRequired(), Email()])
    user_pass = PasswordField('Password', validators=[DataRequired()])
    submit = SubmitField('Login')


class RegisterForm(FlaskForm):
    user_name = EmailField('Name', validators=[DataRequired()])
    user_lastname = EmailField('Last Name', validators=[DataRequired()], render_kw={'placeholder': 'Last Name'})
    user_email = EmailField('Email', validators=[DataRequired(), Email()])
    user_pass = PasswordField('Password', validators=[DataRequired()])
    submit = SubmitField('Login')


@app.route('/')
def index():
    return render_template('index.html', title='Home', headline='User Management')


@app.route('/login', methods=['GET', 'POST'])
def login():
    login_form = LoginForm()
    return render_template('login.html', title='Sign In', login_form=login_form)


@app.route('/register', methods=['GET', 'POST'])
def register():
    register_form = RegisterForm()
    return render_template('register.html', title='Register', register_form=register_form)


if __name__ == '__main__':
    with app.app_context():
        db.create_all()
    app.run(debug=True)
