from flask import Flask, render_template, session, redirect
from flask_bs4 import Bootstrap
from flask_wtf import FlaskForm
from wtforms import StringField, PasswordField, SubmitField, RadioField, SelectField
from wtforms.validators import DataRequired
from flask_moment import Moment
from datetime import datetime
import json
import requests

app = Flask(__name__)
bootstrap = Bootstrap(app)
app.config['SECRET_KEY'] = 'ghjghj^&*GHJ%^&*567867899iuyhgfgu%^&*IJHN'
moment = Moment(app)
date = datetime.now()


class LoginForm(FlaskForm):
    """
    Formularz logowania
    """
    userLogin = StringField('Nazwa użytkownika:', validators=[DataRequired()])
    userPass = PasswordField('Hasło:', validators=[DataRequired()])
    submit = SubmitField('Zaloguj')


class Grade(FlaskForm):
    subject = StringField('Nazwa przedmiotu:', validators=[DataRequired()])
    term = RadioField("Wybierz semestr", choices=[("term1", "Semestr 1"), ("term2", "Semestr 2")])
    category = SelectField('Kategoria:',
                           choices=[('answer', 'Odpowiedź'), ('quiz', 'Kartkówka'), ('test', 'Sprawdzian')])
    grade = SelectField('Ocena:',
                        choices=[(6, "Celujący"), (5, "Bardzo dobry"), (4, "Dobry"),
                                 (3, "Dostateczny"), (2, "Dopuszczający"), (1, "Niedostateczny")])
    submit = SubmitField('Dodaj')


def count_average(subject_value, term_value):
    """funkcja obliczająca średnie ocen"""
    with open('data/grades.json') as gradesFile:
        grades = json.load(gradesFile)
        gradesFile.close()
    sum_grades = 0
    lenght = 0
    if subject_value == "" and term_value == "":
        for subject, terms in grades.items():
            for term, categories in terms.items():
                for category, grades in categories.items():
                    if category == 'answer' or category == 'quiz' or category == 'test':
                        for grade in grades:
                            sum_grades += grade
                            lenght += 1
    else:
        for subject, terms in grades.items():
            if subject == subject_value:
                for term, categories in terms.items():
                    if term == term_value:
                        for category, grades in categories.items():
                            if category == 'answer' or category == 'quiz' or category == 'test':
                                for grade in grades:
                                    sum_grades += grade
                                    lenght += 1
    if lenght != 0:
        return round(sum_grades / lenght, 2)


totalAverage = {}


def yearly_average(subject_value, term_value):
    with open('data/grades.json', encoding='utf-8') as gradesFile:
        grades = json.load(gradesFile)
        gradesFile.close()
    sum_grades = 0
    lenght = 0
    if term_value == '':
        for subject, terms in grades.items():
            if subject == subject_value:
                for term, categories in terms.items():
                    for category, grades in categories.items():
                        if category == 'answer' or category == 'quiz' or category == 'test':
                            for grade in grades:
                                sum_grades += grade
                                lenght += 1
                                totalAverage[subject] = round(sum_grades / lenght, 2)
    if lenght != 0:
        return round(sum_grades / lenght, 2)


@app.route('/')
def index():
    return render_template('index.html', title='Home')


@app.route('/logIn', methods=['POST', 'GET'])
def log_in():
    login = LoginForm()
    with open('data/users.json') as usersFile:
        users = json.load(usersFile)
        usersFile.close()
    if login.validate_on_submit():
        user_login = login.userLogin.data
        user_pass = login.userPass.data
        if user_login == users['userLogin'] and user_pass == users['userPass']:
            session['userLogin'] = user_login
            session['firstName'] = users['firstName']
            return redirect('dashboard')
    return render_template('login.html', title='Logowanie', login=login)


@app.route('/logOut')
def log_out():
    session.pop('userLogin')
    session.pop('firstName')
    return redirect('log_in')


@app.route('/dashboard')
def dashboard():
    with open('data/grades.json') as gradesFile:
        grades = json.load(gradesFile)
        gradesFile.close()
    weather_source = requests.get('https://danepubliczne.imgw.pl/api/data/synop/station/krakow')
    weather = json.loads(weather_source.content)
    air_quality_source = requests.get('https://api.gios.gov.pl/pjp-api/rest/aqindex/getIndex/400')
    air_quality = json.loads(air_quality_source.content)
    return render_template('dashboard.html', title='Dashboard', userLogin=session.get('userLogin'),
                           firstName=session.get('firstName'), date=date, grades=grades, countAverage=count_average,
                           yearlyAverage=yearly_average, weather=weather, airQuality=air_quality)


@app.errorhandler(404)
def page_not_found():
    return render_template('404.html', title='Page not found'), 404


@app.errorhandler(500)
def server_error():
    return render_template('500.html', title='Wewnętrzny błąd serwera :('), 500


if __name__ == '__main__':
    app.run(debug=True)
