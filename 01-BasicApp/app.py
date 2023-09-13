from flask import Flask, render_template

app = Flask(__name__)

@app.route('/')
def index():
    return  '<h2>Hello</h2>'

@app.route('/template')
def template():
    return render_template('template.html', title='Template')

@app.route('/user/<userName>')
def user(userName):
    return  render_template('user.html', userName=userName, title='User')

if __name__ == "__main__":
    app.run(debug=True)