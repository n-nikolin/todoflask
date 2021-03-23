# SLOW AND JANKY BUT IT WORKS AS INTENDED
from datetime import datetime, timedelta

from flask import Flask, render_template, request, redirect, url_for
from flask_sqlalchemy import SQLAlchemy

from query_db import get_timedelta


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
    # was useful for testing, but not anymore
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
    tasks = [task.id for task in complete]
    deltas = [get_timedelta(task.id) for task in complete]
    delta_tasks = dict(zip(complete, deltas))
    for k, v in delta_tasks.items():
        print(k.id, v)
    return render_template('index.html', incomplete=incomplete, complete=delta_tasks.items())


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