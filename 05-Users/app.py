from flask import Flask, render_template, redirect, url_for, flash, request
from flask_sqlalchemy import SQLAlchemy
from flask_login import LoginManager, UserMixin, login_user, logout_user, login_required, current_user
from flask_wtf import FlaskForm
from wtforms import StringField, PasswordField, EmailField, SubmitField
from wtforms.fields.choices import SelectField
from wtforms.validators import DataRequired, Length
from flask_bcrypt import Bcrypt
from flask_bs4 import Bootstrap
import os

# konfiguracja aplikacji
app = Flask(__name__)
bootstrap = Bootstrap(app)
app.config['SECRET_KEY'] = 'lkjh6789&^&*(OKJHG&*(*&YHJ'
bcrypt = Bcrypt(app)

# konfiguracja bazy danych
basedir = os.path.abspath(os.path.dirname(__file__))
app.config['SQLALCHEMY_DATABASE_URI'] = 'sqlite:///' + os.path.join(basedir, 'data/users.sqlite')
db = SQLAlchemy(app)

# tabela w bazie danych


class Users(db.Model, UserMixin):
    id = db.Column(db.Integer, primary_key=True)
    firstName = db.Column(db.String(20))
    lastName = db.Column(db.String(30))
    userMail = db.Column(db.String(50), unique=True)
    userPass = db.Column(db.String(50))
    userRole = db.Column(db.String(20), default='user')

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


class Add(FlaskForm):
    """formularz dodawania nowego użytkownika"""
    firstName = StringField('Imię', validators=[DataRequired()], render_kw={"placeholder": "Imię"})
    lastName = StringField('Nazwisko', validators=[DataRequired()], render_kw={"placeholder": "Nazwisko"})
    userMail = EmailField('Mail', validators=[DataRequired()], render_kw={"placeholder": "Mail"})
    userPass = PasswordField('Hasło', validators=[DataRequired()], render_kw={"placeholder": "Hasło"})
    userRole = SelectField('Uprawnienia', validators=[DataRequired()], choices=[('user', 'Użytkownik'),
                                                                                ('admin', 'Administrator')])
    submit = SubmitField('Dodaj')


class Edit(FlaskForm):
    """formularz edycji użytkownika"""
    firstName = StringField('Imię', validators=[DataRequired()], render_kw={"placeholder": "Imię"})
    lastName = StringField('Nazwisko', validators=[DataRequired()],
                           render_kw={"placeholder": "Nazwisko"})
    userMail = EmailField('Mail', validators=[DataRequired()], render_kw={"placeholder": "Mail"})
    userRole = SelectField('Uprawnienia', validators=[DataRequired()],
                           choices=[('user', 'Użytkownik'), ('admin', 'Administrator')])
    submit = SubmitField('Edytuj')


# class Password(FlaskForm):
#     """formularz zmiany hasła użytkownika"""
#     userMail = EmailField('Mail', validators=[DataRequired()], render_kw={"placeholder": "Mail"})
#     userPass = PasswordField('Hasło', validators=[DataRequired()], render_kw={"placeholder": "Hasło"})
#     submit = SubmitField('Zmień')


class ChangeLoggedUser(FlaskForm):
    """formularz zmiany hasła zalogowanego użytkownika"""
    userEmail = EmailField('Mail', validators=[DataRequired()], render_kw={"placeholder": "Mail"})
    userPass = PasswordField('Hasło', validators=[DataRequired(), Length(min=8, max=20)],
                             render_kw={"placeholder": "Hasło"})
    userNewPass = PasswordField('Nowe hasło', validators=[DataRequired(), Length(min=8, max=20)],
                                render_kw={"placeholder": "Nowe hasło"})
    submit = SubmitField('Zmień')

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
                    return redirect(url_for('dashboard'))
    return render_template('login.html', title='Logowanie', headline='Logowanie', loginForm=loginForm)


@app.route('/register', methods=['GET', 'POST'])
def register():
    registerForm = Register()
    if registerForm.validate_on_submit():
        try:
            hashPass = bcrypt.generate_password_hash(registerForm.userPass.data)
            newUser = Users(userMail=registerForm.userMail.data, userPass=hashPass,
                            firstName=registerForm.firstName.data, lastName=registerForm.lastName.data)
            db.session.add(newUser)
            db.session.commit()
            flash('Konto utworzone poprawnie', 'success')
            return redirect(url_for('login'))
        except Exception:
            flash('Taki adres mail już istnieje, wpisz inny', 'danger')
            return redirect(url_for('register'))
    return render_template('register.html', title='Rejestracja', headline='Rejestracja', registerForm=registerForm)


@app.route('/logout')
@login_required
def logout():
    logout_user()
    return redirect(url_for('login'))


@app.route('/dashboard')
@login_required
def dashboard():
    users = Users.query.all()
    addUser = Register()
    editUser = Register()
    editUserPass = Register()
    return render_template('dashboard.html', title='Dashboard', users=users, addUser=addUser, editUser=editUser,
                           editUserPass=editUserPass)


@app.route('/add-user', methods=['GET', 'POST'])
@login_required
def addUser():
    addUser = Register()
    if addUser.validate_on_submit():
        try:
            hashPass = bcrypt.generate_password_hash(addUser.userPass.data)
            newUser = Users(userMail=addUser.userMail.data, userPass=hashPass, firstName=addUser.firstName.data,
                            lastName=addUser.lastName.data)
            db.session.add(newUser)
            db.session.commit()
            flash('Użytkownik dodany poprawnie', 'success')
            return redirect(url_for('dashboard'))
        except Exception:
            flash('Taki adres mail już istnieje, wpisz inny', 'danger')
            return redirect(url_for('dashboard'))


@app.route('/edit-user<int:id>', methods=['GET', 'POST'])
@login_required
def editUser(id):
    editUser = Register()
    user = Users.query.get_or_404(id)
    if editUser.validate_on_submit():
        user.firstName = editUser.firstName.data
        user.lastName = editUser.lastName.data
        user.userMail = editUser.userMail.data
        user.userPass = bcrypt.generate_password_hash(editUser.userPass.data)
        db.session.commit()
        flash('Dane zapisane poprawnie', 'success')
        return redirect(url_for('dashboard'))


@app.route('/delete-user', methods=['GET', 'POST'])
@login_required
def deleteUser():
    if request.method == 'GET':
        id = request.args.get('id')
        user = Users.query.filter_by(id=id).one()
        db.session.delete(user)
        db.session.commit()
        flash('Użytkownik usunięty poprawnie', 'success')
        return redirect(url_for('dashboard'))


@app.route('/edit-user-pass', methods=['GET', 'POST'])
@login_required
def editUserPass():
    editUserPass = Register()
    user = Users.query.filter_by(userMail=editUserPass.userMail.data).first()
    if editUserPass.validate_on_submit():
        user.userPass = bcrypt.generate_password_hash(editUserPass.userPass.data)
        db.session.commit()
        flash('Hasło zmienione poprawnie', 'success')
        return redirect(url_for('dashboard'))


@app.route('/change', methods=['GET', 'POST'])
@login_required
def change():
    changeLoggedUser = ChangeLoggedUser()
    if changeLoggedUser.validate_on_submit():
        user = Users.query.filter_by(userMail=changeLoggedUser.userEmail.data).first()
        if user and user == current_user:
            if bcrypt.check_password_hash(user.userPass, changeLoggedUser.userPass.data):
                user.userPass = bcrypt.generate_password_hash(changeLoggedUser.userNewPass.data)
                db.session.commit()
                flash('Hasło zmienione poprawnie', 'success')
                return redirect(url_for('dashboard'))
    return render_template('change.html', changeLoggedUser=changeLoggedUser)


if __name__ == '__main__':
    with app.app_context():
        db.create_all()
    app.run(debug=True)
