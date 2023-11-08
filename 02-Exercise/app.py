# flask app definition
import json
import math

from flask import Flask, render_template
from flask_wtf import FlaskForm
from wtforms import StringField, SubmitField
from wtforms.validators import DataRequired
from flask_bs4 import Bootstrap


app = Flask(__name__)
app.config['SECRET_KEY'] = 'downfield#)HRO){fe09fu3fhf){J(@{)o[ds9jhd;dw'  # example
bootstrap = Bootstrap(app)

#Napisz program, który wczyta dane z z pliku salary.json i wyświetli je w postaci tabeli na stronie internetowej. Następnie napisz odpowiednie funkcje: wyznaczanie wartości maksymalnej i minimalnej wynagrodzenia oraz funkcję obliczającą średnie wynagrodzenie. Dodaj do strony opcję wyszukiwania danych według: nazwiska.

class SearchForm(FlaskForm):
    a = StringField('a', validators=[DataRequired()])
    submit = SubmitField('Search')

@app.route('/', methods=['GET', 'POST'])
def index():
    form = SearchForm()
    if form.validate_on_submit():
        data = json.load(open('data/salary.json'))
        dataformated = []
        for i in data:
            dataformated.append(data[i].split(";"))
        dataformated = [i for i in dataformated if form.a.data in i[1]]
        maxsalary = 0
        for i in dataformated:
            if float(i[3]) > maxsalary:
                maxsalary = float(i[3])

        # find min salary using data from dataformated
        minsalary = maxsalary
        for i in dataformated:
            if float(i[3]) < minsalary:
                minsalary = float(i[3])

        # find avg salary using data from dataformated
        avgsalary = 0
        for i in dataformated:
            avgsalary += float(i[3])
        avgsalary = avgsalary / len(dataformated)
        avgsalary = round(avgsalary, 2)
        return render_template('index.html', form=form, dataformated=dataformated, maxsalary=maxsalary, minsalary=minsalary, avgsalary=avgsalary)
    data = json.load(open('data/salary.json'))
    #display data in table
    dataformated = []
    #data is a dictionary with key like "0", "1", "2" etc. and data in value separated with semi-colon ";" like "ID";"Surname";"Name";"Salary";
    for i in data:
        dataformated.append(data[i].split(";"))


    #find max salary using data from dataformated
    maxsalary = 0
    for i in dataformated:
        if float(i[3]) > maxsalary:
            maxsalary = float(i[3])

    #find min salary using data from dataformated
    minsalary = maxsalary
    for i in dataformated:
        if float(i[3]) < minsalary:
            minsalary = float(i[3])

    #find avg salary using data from dataformated
    avgsalary = 0
    for i in dataformated:
        avgsalary += float(i[3])
    avgsalary = avgsalary / len(dataformated)
    avgsalary = round(avgsalary, 2)
    return render_template('index.html', form=form, dataformated=dataformated, maxsalary=maxsalary, minsalary=minsalary, avgsalary=avgsalary)


app.run(debug=True)