from flask import Flask, redirect, render_template, request, abort, jsonify
from flask import make_response


app = Flask(__name__)


@app.route('/authorization')
def authorization():
    return render_template('authorization.html')


@app.route('/')
@app.route('/index')
def home():
    return render_template('index.html', title='Главная')


if __name__ == '__main__':
    app.run()