""" Simple Flask server for displaying generated text. """

import cPickle as pickle
from flask import Flask, render_template, request
from flask_bootstrap import Bootstrap
from generator import generate_text

app = Flask(__name__)
Bootstrap(app)

# load the cfd into memory so that we don't have to reload it on every request
with open('model.pkl', 'rb') as model_file:
    reader_cfd = pickle.load(model_file)


@app.route('/generate_text', methods=['POST', 'GET'])
def make_generated_text():
    DEFAULT_NUM_WORDS = 100
    if request.method == 'POST':
        # if no number of words has been passed in, default to 100
        num_words = request.form['num_words'] if 'num_words' in request.form else DEFAULT_NUM_WORDS
        try:
            num_words = int(request.form['num_words'])
        except ValueError:
            num_words = DEFAULT_NUM_WORDS

        return generate_text(reader_cfd=reader_cfd, num_words=num_words)

    return generate_text(reader_cfd=reader_cfd)


@app.route('/')
def index():
    return render_template('index.html', page="index")


@app.route('/about')
def about():
    return render_template('about.html', page="about")
