from flask import Flask
from flask import render_template, url_for, request, redirect
app = Flask(__name__)

@app.route('/')
def index():
    return render_template('forms-controls.html')

if __name__ == '__main__':
    app.run()