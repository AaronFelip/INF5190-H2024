from flask import Flask, render_template

app = Flask(__name__)


@app.route('/')
def flex_box():
    return render_template('index.html')
