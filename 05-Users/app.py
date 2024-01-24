from flask import Flask, render_template, redirect, url_for, flash
from flask_sqlalchemy import SQLAlchemy
from flask_login import LoginManager, UserMixin, login_user, logout_user, login_required, current_user
from flask_wtf import FlaskForm
from wtforms import StringField, PasswordField, EmailField, SubmitField
from wtforms.validators import DataRequired, Length
from flask_bcrypt import Bcrypt
from flask_bs4 import Bootstrap
import os

# konfiguracja aplikacji
app = Flask(__name__)
bootstrap = Bootstrap(app)
app.config['SECRET_KEY'] = 'lkjh6789&^&*(OKJHG&*(*&YHJ'

# konfiguracja bazy danych
basedir = os.path.abspath(os.path.dirname(__file__))
app.config['SQLALCHEMY_DATABASE_URI'] = 'sqlite:///' + os.path.join(basedir, 'data/users.sqlite')
db = SQLAlchemy(app)
bcrypt = Bcrypt(app)
# tabela w bazie danych
class Users(db.Model, UserMixin):
    id = db.Column(db.Integer, primary_key=True)
    firstName = db.Column(db.String(20))
    lastName = db.Column(db.String(30))
    userMail = db.Column(db.String(50), unique=True)
    userPass = db.Column(db.String(50))

    def is_authenticated(self):
        return True

# konfiguracja Flask-Login
loginManager = LoginManager()
loginManager.init_app(app)
loginManager.login_view = 'login'
loginManager.login_message = 'Nie jesteś zalogowany'
loginManager.login_message_category = 'warning'

@loginManager.user_loader
def loadUser(id):
    return Users.query.filter_by(id=id).first()

# formularze
class Login(FlaskForm):
    """formularz logowania"""
    userMail = EmailField('Mail', validators=[DataRequired()], render_kw={"placeholder": "Mail"})
    userPass = PasswordField('Hasło', validators=[DataRequired()], render_kw={"placeholder": "Hasło"})
    submit = SubmitField('Zaloguj')

class Register(FlaskForm):
    """formularz rejestracji"""
    firstName = StringField('Imię', validators=[DataRequired()], render_kw={"placeholder": "Imię"})
    lastName = StringField('Nazwisko', validators=[DataRequired()], render_kw={"placeholder": "Nazwisko"})
    userMail = EmailField('Mail', validators=[DataRequired()], render_kw={"placeholder": "Mail"})
    userPass = PasswordField('Hasło', validators=[DataRequired()], render_kw={"placeholder": "Hasło"})
    submit = SubmitField('Rejestruj')

# główna aplikacja
@app.route('/')
def index():
    return render_template('index.html', title='Home', headline='Zarządzanie użytkownikami')

@app.route('/login', methods=['GET', 'POST'])
def login():
    user = Users.query.all()
    if not user:
        return redirect(url_for('register'))
    else:
        loginForm = Login()
        if loginForm.validate_on_submit():
            user = Users.query.filter_by(userMail=loginForm.userMail.data).first()
            if user:
                if bcrypt.check_password_hash(user.userPass, loginForm.userPass.data):
                    login_user(user)
                    flash('Zostałeś zalogowany', 'success')
                    return redirect(url_for('dashboard'))
    return render_template('login.html', title='Logowanie', headline='Logowanie', loginForm=loginForm)

@app.route('/register', methods=['GET', 'POST'])
def register():
    registerForm = Register()
    if registerForm.validate_on_submit():
        try:
            hash_pass = bcrypt.generate_password_hash(registerForm.userPass.data)
            new_user = Users(userMail=registerForm.userMail.data, userPass=hash_pass, firstName=registerForm.firstName.data, lastName=registerForm.lastName.data)
            db.session.add(new_user)
            db.session.commit()
            flash('Zostałeś zarejestrowany', 'success')
            return redirect(url_for('login'))
        except Exception:
            flash('Błąd rejestracji, ten email jest już zarejestrowany', 'danger')
            return redirect(url_for('register'))
    return render_template('register.html', title='Rejestracja', headline='Rejestracja', registerForm=registerForm)


@app.route('/logout')
@login_required
def logout():
    logout_user()
    flash('Zostałeś wylogowany', 'success')
    return redirect(url_for('login'))

@app.route('/dashboard')
@login_required
def dashboard():
    users = Users.query.all()
    return render_template('dashboard.html', title='Dashboard', users=users)


if __name__ == '__main__':
    with app.app_context():
        db.create_all()
    app.run(debug=True)