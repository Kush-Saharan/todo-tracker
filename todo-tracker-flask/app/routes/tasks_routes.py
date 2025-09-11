from flask import Blueprint,render_template,request,redirect
from app.models.tasks import Tasks,db,Day
from datetime import date,datetime

tasks_bp = Blueprint('tasks', __name__)


def get_number_of_days():
    first_day = Day.query.order_by(Day.date.asc()).first()
    last_day = Day.query.order_by(Day.date.desc()).first()
    if first_day and last_day:
        return (last_day.date - first_day.date).days + 1
    return 0

@tasks_bp.route('/')
def home():
    tasks = Tasks.query.all()
    today = date.today()

    existing = Day.query.filter_by(date=today).first()
    if not existing:
        date_today = Day(date=today)
        db.session.add(date_today)
        db.session.commit()


    number_of_days = get_number_of_days() 

    return render_template("index.html", tasks=tasks, number_of_days=number_of_days)


@tasks_bp.route('/task/add',methods=['POST'])
def add_task():

    task_add=request.form['task']
    existing_task = Tasks.query.filter(Tasks.task_name.ilike(task_add)).first()
    if(existing_task):
        message="This task already exists in tasks!"
    else:
        new_task=Tasks(task_name=task_add)
        db.session.add(new_task)
        db.session.commit()
        message="Task added successfully!"
    number_of_days = get_number_of_days()

    tasks=Tasks.query.all()
    return render_template('index.html',tasks=tasks, message=message,number_of_days=number_of_days)
    

@tasks_bp.route('/task/update')
def update_task():
    pass

@tasks_bp.route('/task/save',methods=['POST'])
def save_task():
    pass

