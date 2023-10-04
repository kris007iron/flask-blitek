# flask app definition
import math

from flask import Flask, render_template
from flask_wtf import FlaskForm
from wtforms import StringField, SubmitField
from wtforms.validators import DataRequired
from flask_bs4 import Bootstrap


app = Flask(__name__)
app.config['SECRET_KEY'] = 'downfield#)HRO){fe09fu3fhf){J(@{)o[ds9jhd;dw'  # example
bootstrap = Bootstrap(app)


class CountForm(FlaskForm):
    """
    Count form
    """
    a = StringField('a', validators=[DataRequired()])
    b = StringField('b', validators=[DataRequired()])
    c = StringField('c', validators=[DataRequired()])
    submit = SubmitField('Count zero points')


@app.route('/', methods=['POST', 'GET'])
def index():
    form = CountForm()
    roots = "no values"
    if form.validate_on_submit():
        if form.a.data == "0":
            roots = 'a cannot be zero'
        else:
            a = float(form.a.data)
            b = float(form.b.data)
            c = float(form.c.data)
            d = b**2 - 4*a*c
            if d < 0:
                roots = 'No roots'
            elif d == 0:
                x = -b / (2*a)
                roots = ["delta: " + str(d), "x1: " + str(x)]
            else:
                x1 = (-b + math.sqrt(d)) / (2*a)
                x2 = (-b - math.sqrt(d)) / (2*a)
                roots = ["delta: " + str(d), "x1: " + str(x1), "x2: " + str(x2)]
        return render_template('index.html', form=form, roots=roots)
    return render_template('index.html', form=form, roots=roots)
