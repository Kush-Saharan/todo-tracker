from app.main import db
from datetime import date

class Tasks(db.Model):
    id=db.Column(db.Integer, primary_key=True)
    task_name=db.Column(db.String(200), nullable=False)

    def __repr__(self)->str:
        return f"{self.id} - {self.task}"
    

class Day(db.Model):
    id = db.Column(db.Integer, primary_key=True)
    date = db.Column(db.Date, nullable=False, default=date.today)



class TaskStatus(db.Model):
    id = db.Column(db.Integer, primary_key=True)
    task_id = db.Column(db.Integer, db.ForeignKey('tasks.id'), nullable=False)
    date = db.Column(db.Integer, db.ForeignKey('day.date'), nullable=False)
    completed = db.Column(db.Boolean, default=False)

    task = db.relationship('Tasks', backref='statuses')
    day = db.relationship('Day', backref='statuses')