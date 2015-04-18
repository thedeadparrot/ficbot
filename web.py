""" Simple Flask server for displaying generated text. """

import pickle
from flask import Flask, render_template, url_for
from flask_bootstrap import Bootstrap
from generator import generate_text

app = Flask(__name__)
Bootstrap(app)

# load the cfd into memory so that we don't have to reload it on every request
with open('model.pkl', 'rb') as model_file:
    reader_cfd = pickle.load(model_file)


@app.route('/generate_text')
def generated_text():
    return generate_text(reader_cfd=reader_cfd)


@app.route('/')
def index():
    return render_template('index.html', page="index")


@app.route('/about')
def about():
    return render_template('about.html', page="about")
