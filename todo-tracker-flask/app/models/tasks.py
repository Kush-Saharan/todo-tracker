from app.main import db
from datetime import datetime

class Tasks(db.Model):
    id=db.Column(db.Integer, primary_key=True)
    task_name=db.Column(db.String(200), nullable=False)
    date=db.Column(db.String(500), default=datetime.utcnow())
    completed=db.Column(db.BOOLEAN, default=0)

    def __repr__(self)->str:
        return f"{self.id} - {self.task}"