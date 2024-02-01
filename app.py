from flask import Flask, render_template, request, redirect, url_for
from flask_sqlalchemy import SQLAlchemy


app = Flask(__name__)
app.config['SQLALCHEMY_DATABASE_URI'] = 'sqlite:///employees.db'
db = SQLAlchemy(app)


class Employee(db.Model):
    id = db.Column(db.Integer, primary_key=True)
    name = db.Column(db.String(100))
    position = db.Column(db.String(100))
    salary = db.Column(db.Float)
    department = db.Column(db.String(100))


@app.route('/')
@app.route('/home')
def index():
    return render_template("index.html")


if __name__ == '__main__':
    app.run(debug=True)