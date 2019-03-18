#coding=utf-8
from flask import Flask, render_template, url_for

app = Flask(__name__,static_url_path='',root_path='/Users/octopolugal/Desktop/civil_graph/d3js_flask')

@app.route('/demo')
def index(name=None):
    return render_template('index.html', name=name)

if __name__ == '__main__':
    app.run(debug=True)
