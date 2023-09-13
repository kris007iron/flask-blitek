from flask import Flask, render_template
from flask_bs4 import Bootstrap

app = Flask(__name__)
bootstrap = Bootstrap(app)


@app.route('/')
def index():
    return render_template('index.html')


# noinspection PyUnusedLocal
@app.errorhandler(404)
def page_not_found(e):
    return render_template('404.html', title='Page not found'), 404


# noinspection PyUnusedLocal
@app.errorhandler(500)
def internal_server_error(e):
    return render_template('500.html', title='Internal server error'), 500


if __name__ == "__main__":
    app.run(debug=True)
