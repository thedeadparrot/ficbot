from flask import Flask, render_template
from flask_bootstrap import Bootstrap
from generator import generate_text

app = Flask(__name__)
Bootstrap(app)


@app.route('/generate_text')
def generated_text():
    return generate_text()


@app.route('/')
def index():
    return render_template('index.html')

if __name__ == '__main__':
    # TODO: REMOVE ON DEPLOY. I MEAN IT.
    app.debug = True
    app.run()
