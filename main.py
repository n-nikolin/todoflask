# TODO: I did it in the most retareded way possible.
# This is truly pitiful and i am quite annoyed that i can't output shit
# from the console to the web page
# this is truly retarded
# will try to use psycopg2 tomorrow to query the timedelta of each todo_item
# but using psycopg2 seems to be a bit of an overkill
# almost certain there is a nice and tidy way of going about it
# this got a bit too messy

# TODO: hust fuck around with psycopg2 in neighbor file
# and import it into main.py

from datetime import datetime, timedelta

from flask import Flask, render_template, request, redirect, url_for
from flask_sqlalchemy import SQLAlchemy


app = Flask(__name__)

# CHANGE TO 'prod' when deploying
ENV = 'dev'

if ENV == 'dev':
    app.debug = True
    app.config['SQLALCHEMY_DATABASE_URI'] = 'postgresql://postgres:1234@localhost/todo_app'
else:
    app.debug = False
    app.config['SQLALCHEMY_DATABASE_URI'] = ''

app.config['SQLALCHEMY_TRACK_MODIFICATIONS'] = False

db = SQLAlchemy(app)


class Todo(db.Model):
    __tablename__ = 'todo_list'
    id = db.Column(db.Integer, primary_key=True)
    text = db.Column(db.String(200))
    complete = db.Column(db.Boolean)
    # Added started and finished tables
    started = db.Column(db.DateTime, default=datetime.utcnow)
    finished = db.Column(db.DateTime, default=datetime.utcnow)
    # the dumbest and easiest way to get timedelta
    time_spent = db.Column(db.Interval)

    def __init__(self, text, complete, started, finished, time_spent):
        self.text = text
        self.complete = complete
        self.started = started
        self.finished = finished
        self.time_spent = time_spent

    def t_spent(self):
        return self.finished - self.complete


@app.route('/')
def index():
    incomplete = Todo.query.filter_by(complete=False).all()
    complete = Todo.query.filter_by(complete=True).all()
    return render_template('index.html', incomplete=incomplete, complete=complete)


@app.route('/add', methods=['POST'])
def add():
    started = datetime.now()
    finished = None
    time_spent = None
    todo = Todo(text=request.form['todoitem'], complete=False,
                started=started, finished=finished, time_spent=time_spent)
    db.session.add(todo)
    db.session.commit()

    return redirect(url_for('index'))


@app.route('/complete/<id>')
def complete(id):
    todo = Todo.query.filter_by(id=int(id)).first()
    todo.finished = datetime.now()
    todo.complete = True
    todo.time_spent = todo.finished - todo.started
    db.session.commit()

    return redirect(url_for('index'))


if __name__ == '__main__':
    app.run()
